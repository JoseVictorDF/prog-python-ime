# -*- coding: utf-8 -*-

"""
Este programa lê um arquivo CSV de produtos e preços, agrupa os dados por
supermercado e gera um arquivo de saída para cada um, contendo os produtos
em ordem alfabética e a média de seus preços históricos, UTILIZANDO NUMPY.
"""

# 1. IMPORTAÇÃO: Agora importamos a biblioteca NumPy
import numpy as np


def calcular_media_np(precos_array: np.ndarray) -> float:
    """
    Calcula o valor médio de um array de preços usando NumPy.

    Args:
        precos_array: Um array NumPy com os preços.

    Returns:
        O valor médio dos números no array. Retorna 0.0 se o array for vazio.
    """
    # A função np.mean() é a forma otimizada de calcular a média com NumPy
    if precos_array.size == 0:
        return 0.0
    return np.mean(precos_array)


def processar_dados_e_gerar_arquivos(arquivo_entrada: str):
    """
    Função principal que lê o arquivo de entrada, processa os dados
    e gera os arquivos de saída para cada supermercado.

    Args:
        arquivo_entrada: O nome do arquivo .csv a ser lido.
    """
    dados_por_supermercado = {}

    # --- Etapa 1: Ler o arquivo de entrada e agrupar os dados ---
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f_in:
            print(f"Lendo o arquivo de entrada: '{arquivo_entrada}'...")
            for linha in f_in:
                partes = linha.strip().split(';')

                nome_produto = partes[0]
                nome_supermercado = partes[-1]

                try:
                    # 2. CONVERSÃO PARA ARRAY NUMPY: Convertemos os preços diretamente para um array NumPy
                    precos_np = np.array([p.replace(',', '.') for p in partes[1:-1]], dtype=float)
                except ValueError:
                    print(f"Aviso: Linha com dados de preço inválidos ignorada: {linha.strip()}")
                    continue

                if nome_supermercado not in dados_por_supermercado:
                    dados_por_supermercado[nome_supermercado] = []

                # Adicionamos o nome do produto e o ARRAY de preços
                dados_por_supermercado[nome_supermercado].append([nome_produto, precos_np])

    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return

    # --- Etapa 2: Gerar um arquivo de saída para cada supermercado ---
    if not dados_por_supermercado:
        print("Nenhum dado válido foi processado. Nenhum arquivo de saída será gerado.")
        return

    print("\nIniciando a geração dos arquivos de saída...")
    for supermercado, produtos in dados_por_supermercado.items():

        produtos.sort(key=lambda item: item[0])

        nome_arquivo_saida = f"{supermercado.replace(' ', '_')}.csv"

        # --- Etapa 3: Escrever os dados processados no arquivo de saída ---
        try:
            with open(nome_arquivo_saida, 'w', encoding='utf-8', newline='') as f_out:
                for item in produtos:
                    nome_prod = item[0]
                    array_de_precos = item[1]  # Agora isso é um array NumPy

                    # 3. CÁLCULO COM NUMPY: Usamos a nova função para calcular a média
                    media_precos = calcular_media_np(array_de_precos)

                    linha_saida = f"{nome_prod};{media_precos:.2f}\n"
                    f_out.write(linha_saida.replace('.', ','))

                print(f"-> Arquivo '{nome_arquivo_saida}' gerado com sucesso!")

        except IOError as e:
            print(f"ERRO: Não foi possível escrever no arquivo '{nome_arquivo_saida}'. Motivo: {e}")
        except Exception as e:
            print(f"ERRO: Ocorreu um erro inesperado ao gerar o arquivo '{nome_arquivo_saida}': {e}")


# --- Início da Execução do Programa ---
if __name__ == "__main__":
    # Certifique-se de ter o NumPy instalado: pip install numpy
    ARQUIVO_ENTRADA_CSV = 'produtos_s2.csv'
    processar_dados_e_gerar_arquivos(ARQUIVO_ENTRADA_CSV)