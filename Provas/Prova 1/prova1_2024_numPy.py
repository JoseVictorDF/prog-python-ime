import csv
import numpy as np


def calcular_media_cambio(valores_cambio_mensal_np):
    """
    Calcula a média dos valores de câmbio mensais usando NumPy.
    Recebe um array NumPy como entrada.
    """
    # A função np.mean() do NumPy calcula a média de forma eficiente.
    return np.mean(valores_cambio_mensal_np)


def processar_dados_com_numpy():
    """
    Processa os dados de câmbio utilizando a biblioteca NumPy para os cálculos.
    """
    dados_moeda_por_ano = {}
    dados_agencias_por_ano_e_nome = {}

    # 1. Ler o arquivo moeda.csv [cite: 6]
    # O tratamento de erro na abertura de arquivos é mantido [cite: 16]
    try:
        with open('moeda.csv', mode='r', newline='', encoding='utf-8') as file_moeda:
            leitor_csv_moeda = csv.reader(file_moeda)
            for linha in leitor_csv_moeda:
                if not linha or not linha[0].strip().isdigit():
                    continue
                ano = linha[0].strip()
                # Converte a lista de cotações para um array NumPy
                cotacoes_mensais = [float(c.strip()) for c in linha[1:] if c.strip()]
                dados_moeda_por_ano[ano] = np.array(cotacoes_mensais, dtype=float)
    except FileNotFoundError:
        print("Erro: Arquivo 'moeda.csv' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler 'moeda.csv': {e}")
        return

    # 2. Ler o arquivo agencias.csv [cite: 3]
    try:
        with open('agencias.csv', mode='r', newline='', encoding='utf-8') as file_agencias:
            leitor_csv_agencias = csv.reader(file_agencias)
            for linha in leitor_csv_agencias:
                if not linha or not linha[1].strip().isdigit():
                    continue
                nome_agencia = linha[0].strip()
                ano_referencia = linha[1].strip()
                # Converte a lista de taxas para um array NumPy
                taxas_mensais = [float(t.strip()) for t in linha[2:] if t.strip()]

                if ano_referencia not in dados_agencias_por_ano_e_nome:
                    dados_agencias_por_ano_e_nome[ano_referencia] = {}
                dados_agencias_por_ano_e_nome[ano_referencia][nome_agencia] = np.array(taxas_mensais, dtype=float)
    except FileNotFoundError:
        print("Erro: Arquivo 'agencias.csv' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler 'agencias.csv': {e}")
        return

    # 3. Processar e gerar um arquivo de saída para cada ano [cite: 10]
    anos_com_dados_agencia = False
    for ano, cotacoes_do_ano_np in dados_moeda_por_ano.items():
        if ano in dados_agencias_por_ano_e_nome:
            anos_com_dados_agencia = True
            agencias_do_ano = dados_agencias_por_ano_e_nome[ano]

            # Ordenar agências em ordem alfabética [cite: 12]
            nomes_agencias_ordenados = sorted(agencias_do_ano.keys())

            nome_arquivo_saida = f'resultado_numpy_{ano}.csv'
            try:
                with open(nome_arquivo_saida, mode='w', newline='', encoding='utf-8') as file_out:
                    escritor_csv = csv.writer(file_out)

                    for nome_agencia in nomes_agencias_ordenados:
                        taxas_da_agencia_np = agencias_do_ano[nome_agencia]

                        # Garante que os arrays tenham o mesmo tamanho para a operação
                        num_meses = min(len(cotacoes_do_ano_np), len(taxas_da_agencia_np))
                        cotacoes_slice = cotacoes_do_ano_np[:num_meses]
                        taxas_slice = taxas_da_agencia_np[:num_meses]

                        # Cálculo do câmbio de forma vetorizada
                        # Fórmula: valor_cambio = cotacao * (100 + taxa)% [cite: 9]
                        valores_cambio_mensal_np = cotacoes_slice * (1 + taxas_slice / 100)

                        # Cálculo da média usando a função dedicada [cite: 13]
                        media_cambio = calcular_media_cambio(valores_cambio_mensal_np)

                        # Preparar linha para o arquivo CSV de saída [cite: 11]
                        linha_saida = [nome_agencia]
                        # Formata cada valor do câmbio com quatro casas decimais [cite: 11]
                        linha_saida.extend([f"{valor:.4f}" for valor in valores_cambio_mensal_np])
                        linha_saida.append(f"{media_cambio:.4f}")

                        escritor_csv.writerow(linha_saida)

                print(f"Arquivo '{nome_arquivo_saida}' gerado com sucesso.")
            except Exception as e:
                print(f"Erro ao escrever o arquivo '{nome_arquivo_saida}': {e}")
        else:
            # Caso não haja dados de agências para o ano, informa o usuário [cite: 14, 15]
            print(f"Não foram encontrados dados de agências para o ano {ano}. Nenhum arquivo foi gerado para este ano.")

    if not dados_moeda_por_ano:
        print("Nenhum dado encontrado em 'moeda.csv'. Nenhum arquivo de saída será gerado.")


# Garante que o script seja executado apenas quando chamado diretamente
if __name__ == "__main__":
    processar_dados_com_numpy()