import pandas as pd
import pika
import json
import time

# --- Configurações do RabbitMQ ---
RABBITMQ_HOST = 'localhost'
FILA_NORMAL = 'fila_normal'
FILA_ATENCAO = 'fila_atencao'
FILA_ALERTA_CRITICO = 'fila_alerta_critico'


def classificar_ponto_de_dado(batimento, estado, idade):
    """
    Classifica um único ponto de dado (uma linha) em Normal, Atenção ou Crítico.
    Esta função espelha a lógica usada para gerar os dados.
    """
    # Simplificação da lógica da tabela para a função de análise
    faixa_critica_min, faixa_critica_max = 0, 0
    faixa_atencao_min, faixa_atencao_max = 0, 0

    if estado == 'Repouso':
        faixa_atencao_min, faixa_atencao_max = 101, 120
        faixa_critica_min, faixa_critica_max = 121, 999
    elif estado == 'Atividade Leve':
        faixa_atencao_min, faixa_atencao_max = 121, 140
        faixa_critica_min, faixa_critica_max = 141, 999
    elif estado == 'Atividade Moderada':
        faixa_atencao_min, faixa_atencao_max = 151, 170
        faixa_critica_min, faixa_critica_max = 171, 999

    if idade > 65:  # Ajuste para idosos
        faixa_atencao_min -= 10
        faixa_atencao_max -= 10
        faixa_critica_min -= 10
        faixa_critica_max -= 10

    if faixa_critica_min <= batimento <= faixa_critica_max:
        return "Alerta Crítico"
    if faixa_atencao_min <= batimento <= faixa_atencao_max:
        return "Atenção"

    return "Normal"


def analisar_dados_paciente(df_paciente):
    """
    Analisa os 10 minutos de dados de um paciente e retorna o nível de alerta final e um resumo.
    A lógica prioriza o evento mais grave ocorrido no período.
    """
    # Extrai dados estáticos do primeiro registro
    info_paciente = df_paciente.iloc[0]
    idade = info_paciente['idade']
    estado = info_paciente['estado']

    classificacoes = df_paciente['batimento_cardiaco'].apply(
        lambda bpm: classificar_ponto_de_dado(bpm, estado, idade)
    )

    # Lógica de prioridade: Se qualquer ponto for crítico, o alerta final é crítico.
    if "Alerta Crítico" in classificacoes.values:
        ponto_critico = df_paciente[classificacoes == "Alerta Crítico"].iloc[0]
        resumo = f"Pico de {ponto_critico['batimento_cardiaco']} BPM em {estado} no minuto {ponto_critico['minuto']}."
        return "Alerta Crítico", resumo

    # Se não houver crítico, mas houver atenção, o alerta final é atenção.
    if "Atenção" in classificacoes.values:
        ponto_atencao = df_paciente[classificacoes == "Atenção"].iloc[0]
        resumo = f"Registrou {ponto_atencao['batimento_cardiaco']} BPM em {estado}, indicando necessidade de acompanhamento."
        return "Atenção", resumo

    # Caso contrário, o paciente está normal.
    media_bpm = df_paciente['batimento_cardiaco'].mean()
    resumo = f"Paciente estável com média de {media_bpm:.1f} BPM em {estado}."
    return "Normal", resumo


def main():
    print("--- Iniciando Analisador de Pacientes e Publicador RabbitMQ ---")

    # --- 1. Conexão e Configuração do RabbitMQ ---
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        print("Conexão com RabbitMQ estabelecida com sucesso.")

        # Declara as filas como duráveis para que sobrevivam a reinicializações
        channel.queue_declare(queue=FILA_NORMAL, durable=True)
        channel.queue_declare(queue=FILA_ATENCAO, durable=True)
        channel.queue_declare(queue=FILA_ALERTA_CRITICO, durable=True)
        print("Filas 'fila_normal', 'fila_atencao' e 'fila_alerta_critico' estão prontas.")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"ERRO: Não foi possível conectar ao RabbitMQ em '{RABBITMQ_HOST}'.")
        print("Verifique se o RabbitMQ está rodando (ex: via Docker) e acessível.")
        return

    # --- 2. Leitura e Processamento dos Dados ---
    try:
        df_total = pd.read_csv("monitoramento_pacientes.csv")
        print(f"Arquivo 'monitoramento_pacientes.csv' lido. Total de {len(df_total)} registros.")
    except FileNotFoundError:
        print("ERRO: Arquivo 'monitoramento_pacientes.csv' não encontrado.")
        print("Por favor, execute o script gerador de dados primeiro.")
        connection.close()
        return

    # Agrupa o DataFrame por paciente_id
    pacientes_agrupados = df_total.groupby('paciente_id')

    print("\nIniciando análise para cada um dos 100 pacientes...")
    # Itera sobre cada paciente
    for paciente_id, df_paciente in pacientes_agrupados:

        # 3. Análise dos 10 minutos do paciente
        nivel_alerta_final, resumo_analise = analisar_dados_paciente(df_paciente)

        # Seleciona a fila de destino com base na análise
        if nivel_alerta_final == "Alerta Crítico":
            fila_destino = FILA_ALERTA_CRITICO
        elif nivel_alerta_final == "Atenção":
            fila_destino = FILA_ATENCAO
        else:
            fila_destino = FILA_NORMAL

        # 4. Criação e Publicação da Mensagem
        mensagem = {
            'paciente_id': int(paciente_id),
            'nivel_alerta': nivel_alerta_final,
            'timestamp_analise': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'resumo_analise': resumo_analise,
            'dados_paciente': df_paciente.iloc[0].to_dict()  # Envia perfil do paciente
        }

        corpo_mensagem = json.dumps(mensagem, indent=4)

        channel.basic_publish(
            exchange='',
            routing_key=fila_destino,
            body=corpo_mensagem,
            properties=pika.BasicProperties(
                delivery_mode=2,  # Torna a mensagem persistente
            ))

        print(
            f"  -> Paciente {paciente_id}: Nível '{nivel_alerta_final}'. Mensagem enviada para a fila '{fila_destino}'.")

    # --- 5. Finalização ---
    connection.close()
    print("\nAnálise concluída. Todas as mensagens foram publicadas.")
    print("Verifique a interface de gerenciamento do RabbitMQ para ver as filas.")


if __name__ == '__main__':
    main()