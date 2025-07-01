import pandas as pd
import numpy as np
import os


def definir_faixa_bpm(idade, estado, perfil):
    """
    Define a faixa de BPM (mín, máx) com base no perfil do paciente e no resultado desejado.
    Esta função é o "cérebro" que garante que os dados gerados correspondam ao perfil.
    """
    # Faixas para Adultos (18-65) - simplificado para o exemplo
    # ESTADO: 1=Repouso, 2=Atividade Leve, 3=Atividade Intensa
    faixas = {
        # (Estado, Perfil): (BPM_min, BPM_max)
        (1, "Normal"): (60, 95),
        (1, "Atenção"): (101, 119),  # Foco na taquicardia para simplificar
        (1, "Alerta Crítico"): (121, 140),

        (2, "Normal"): (90, 120),
        (2, "Atenção"): (121, 139),
        (2, "Alerta Crítico"): (141, 160),

        (3, "Normal"): (120, 150),
        (3, "Atenção"): (151, 169),
        (3, "Alerta Crítico"): (171, 190),
    }

    # Para idosos (+65), reduzimos um pouco a frequência cardíaca
    modificador_idade = -10 if idade > 65 else 0

    faixa = faixas.get((estado, perfil), (70, 80))  # Default caso algo falhe
    return (faixa[0] + modificador_idade, faixa[1] + modificador_idade)


def gerar_dataset_pacientes(num_pacientes=100, num_minutos=10):
    """
    Gera um dataset de monitoramento para N pacientes durante M minutos e salva em CSV.
    """
    print("Iniciando a geração do dataset...")

    # 1. Definir a distribuição de perfis
    num_normal = int(num_pacientes * 0.40)
    num_atencao = int(num_pacientes * 0.30)
    num_critico = num_pacientes - num_normal - num_atencao

    perfis = (["Normal"] * num_normal +
              ["Atenção"] * num_atencao +
              ["Alerta Crítico"] * num_critico)
    np.random.shuffle(perfis)

    # Lista para guardar todos os registros antes de criar o DataFrame
    todos_os_dados = []

    # 2. Loop para criar os dados de cada paciente
    for id_paciente in range(num_pacientes):
        perfil_paciente = perfis[id_paciente]

        # Gera características fixas para o paciente
        idade = np.random.randint(20, 81)
        sexo = np.random.choice(["M", "F"])
        # Estado de atividade é fixo para os 10 minutos
        estado_codigo = np.random.choice([1, 2, 3])  # 1=Repouso, 2=Leve, 3=Intensa
        map_estado = {1: "Repouso", 2: "Atividade Leve", 3: "Atividade Intensa"}
        estado_texto = map_estado[estado_codigo]

        # 3. Gerar a série temporal de BPM de acordo com o perfil
        bpm_min, bpm_max = definir_faixa_bpm(idade, estado_codigo, perfil_paciente)

        # Cria uma linha de base realista dentro da faixa e adiciona "ruído"
        linha_base_bpm = np.random.randint(bpm_min, bpm_max)
        # Gera os 10 minutos de BPM com pequenas variações
        serie_bpm = linha_base_bpm + np.random.randint(-3, 4, size=num_minutos)
        # Garante que nenhum valor saia da faixa definida
        serie_bpm = np.clip(serie_bpm, bpm_min, bpm_max)

        # 4. Adicionar os 10 registros do paciente à lista principal
        for minuto in range(num_minutos):
            registro = {
                "paciente_id": id_paciente,
                "minuto": minuto,
                "idade": idade,
                "sexo": sexo,
                "estado": estado_texto,
                "batimento_cardiaco": serie_bpm[minuto]
            }
            todos_os_dados.append(registro)

    print(f"Dados gerados para {num_pacientes} pacientes.")

    # 5. Criar o DataFrame e salvar em CSV
    df = pd.DataFrame(todos_os_dados)

    nome_arquivo = "monitoramento_pacientes.csv"
    df.to_csv(nome_arquivo, index=False, encoding='utf-8-sig')

    caminho_completo = os.path.abspath(nome_arquivo)
    print(f"\nDataset salvo com sucesso!")
    print(f"Arquivo: '{caminho_completo}'")

    # Verificação final (opcional)
    print("\n--- Verificação da Distribuição ---")
    # Para verificar, precisamos aplicar a lógica de classificação ao CSV gerado
    # Esta é uma simplificação para mostrar que os dados foram gerados corretamente
    pacientes_criticos = df[df['paciente_id'].isin(
        [i for i, p in enumerate(perfis) if p == 'Alerta Crítico']
    )]
    num_pacientes_criticos_verificados = pacientes_criticos['paciente_id'].nunique()
    print(
        f"Número de pacientes no perfil 'Alerta Crítico': {num_pacientes_criticos_verificados} (Esperado: {num_critico})")

    pacientes_atencao = df[df['paciente_id'].isin(
        [i for i, p in enumerate(perfis) if p == 'Atenção']
    )]
    num_pacientes_atencao_verificados = pacientes_atencao['paciente_id'].nunique()
    print(f"Número de pacientes no perfil 'Atenção': {num_pacientes_atencao_verificados} (Esperado: {num_atencao})")

    pacientes_normal = df[df['paciente_id'].isin(
        [i for i, p in enumerate(perfis) if p == 'Normal']
    )]
    num_pacientes_normal_verificados = pacientes_normal['paciente_id'].nunique()
    print(f"Número de pacientes no perfil 'Normal': {num_pacientes_normal_verificados} (Esperado: {num_normal})")


# --- Execução Principal ---
if __name__ == "__main__":
    gerar_dataset_pacientes()