import pandas as pd
import pika
import json
import time
import os  # (NOVO) Importa a biblioteca os para manipulação de caminhos de arquivo

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
    info_paciente = df_paciente.iloc[0]
    idade = info_paciente['idade']
    estado = info_paciente['estado']

    classificacoes = df_paciente['batimento_cardiaco'].apply(
        lambda bpm: classificar_ponto_de_dado(bpm, estado, idade)
    )

    if "Alerta Crítico" in classificacoes.values:
        ponto_critico = df_paciente[classificacoes == "Alerta Crítico"].iloc[0]
        resumo = f"Pico de {ponto_critico['batimento_cardiaco']} BPM em {estado} no minuto {ponto_critico['minuto']}."
        return "Alerta Crítico", resumo

    if "Atenção" in classificacoes.values:
        ponto_atencao = df_paciente[classificacoes == "Atenção"].iloc[0]
        resumo = f"Registrou {ponto_atencao['batimento_cardiaco']} BPM em {estado}, indicando necessidade de acompanhamento."
        return "Atenção", resumo

    media_bpm = df_paciente['batimento_cardiaco'].mean()
    resumo = f"Paciente estável com média de {media_bpm:.1f} BPM em {estado}."
    return "Normal", resumo


def main():
    print("--- Iniciando Analisador de Pacientes e Publicador RabbitMQ ---")

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        channel = connection.channel()
        print("Conexão com RabbitMQ estabelecida com sucesso.")

        channel.queue_declare(queue=FILA_NORMAL, durable=True)
        channel.queue_declare(queue=FILA_ATENCAO, durable=True)
        channel.queue_declare(queue=FILA_ALERTA_CRITICO, durable=True)
        print("Filas 'fila_normal', 'fila_atencao' e 'fila_alerta_critico' estão prontas.")

    except pika.exceptions.AMQPConnectionError as e:
        print(f"ERRO: Não foi possível conectar ao RabbitMQ em '{RABBITMQ_HOST}'.")
        print("Verifique se o RabbitMQ está rodando (ex: via Docker) e acessível.")
        return

    try:
        df_total = pd.read_csv("monitoramento_pacientes.csv")
        print(f"Arquivo 'monitoramento_pacientes.csv' lido. Total de {len(df_total)} registros.")
    except FileNotFoundError:
        print("ERRO: Arquivo 'monitoramento_pacientes.csv' não encontrado.")
        print("Por favor, execute o script gerador de dados primeiro.")
        connection.close()
        return

    pacientes_agrupados = df_total.groupby('paciente_id')

    # (NOVO) Lista para guardar os resultados da auditoria
    registros_auditoria = []

    print("\nIniciando análise para cada um dos 100 pacientes...")
    for paciente_id, df_paciente in pacientes_agrupados:

        nivel_alerta_final, resumo_analise = analisar_dados_paciente(df_paciente)

        # (NOVO) Adiciona os dados de auditoria à lista
        info_paciente = df_paciente.iloc[0]
        registro_auditoria = {
            'paciente_id': int(paciente_id),
            'idade': info_paciente['idade'],
            'sexo': info_paciente['sexo'],
            'estado_permanente': info_paciente['estado'],
            'classificacao_final': nivel_alerta_final,
            'justificativa': resumo_analise
        }
        registros_auditoria.append(registro_auditoria)

        # Seleciona a fila de destino e publica a mensagem (lógica existente)
        if nivel_alerta_final == "Alerta Crítico":
            fila_destino = FILA_ALERTA_CRITICO
        elif nivel_alerta_final == "Atenção":
            fila_destino = FILA_ATENCAO
        else:
            fila_destino = FILA_NORMAL

        mensagem = {
            'paciente_id': int(paciente_id),
            'nivel_alerta': nivel_alerta_final,
            'timestamp_analise': time.strftime('%Y-%m-%dT%H:%M:%S'),
            'resumo_analise': resumo_analise,
            'dados_paciente': info_paciente.to_dict()
        }

        corpo_mensagem = json.dumps(mensagem, indent=4)

        channel.basic_publish(
            exchange='',
            routing_key=fila_destino,
            body=corpo_mensagem,
            properties=pika.BasicProperties(delivery_mode=2))

        print(
            f"  -> Paciente {paciente_id}: Nível '{nivel_alerta_final}'. Mensagem enviada para a fila '{fila_destino}'.")

    # (NOVO) Geração do CSV de Auditoria após o loop de processamento
    print("\nGerando CSV de auditoria...")
    df_auditoria = pd.DataFrame(registros_auditoria)

    nome_arquivo_auditoria = "log_auditoria_classificacao.csv"
    df_auditoria.to_csv(nome_arquivo_auditoria, index=False, encoding='utf-8-sig')

    caminho_auditoria = os.path.abspath(nome_arquivo_auditoria)
    print(f"Arquivo de auditoria salvo com sucesso em: '{caminho_auditoria}'")

    # Finalização
    connection.close()
    print("\nAnálise concluída. Todas as mensagens foram publicadas e o log de auditoria foi gerado.")
    print("Verifique a interface de gerenciamento do RabbitMQ e o novo arquivo CSV.")


if __name__ == '__main__':
    main()