# -*- coding: utf-8 -*-

"""
Este programa lê um arquivo CSV de produtos e preços, agrupa os dados por
supermercado e gera um arquivo de saída para cada um, contendo os produtos
em ordem alfabética e a média de seus preços históricos.
"""


def calcular_media(precos: list) -> float:
    """
    Calcula o valor médio de uma lista de preços.

    Args:
        precos: Uma lista de números (floats ou ints).

    Returns:
        O valor médio dos números na lista. Retorna 0 se a lista for vazia.
    """
    if not precos:
        return 0.0
    return sum(precos) / len(precos)


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
                # Remove espaços em branco no início/fim e quebra a linha pelo ';'
                partes = linha.strip().split(';')

                # Extrai as informações da linha
                nome_produto = partes[0]
                nome_supermercado = partes[-1]

                # Converte os preços (strings) para float
                try:
                    precos = [float(p.replace(',', '.')) for p in partes[1:-1]]
                except ValueError:
                    print(f"Aviso: Linha com dados de preço inválidos ignorada: {linha.strip()}")
                    continue

                # Se o supermercado ainda não está no nosso dicionário, adiciona
                if nome_supermercado not in dados_por_supermercado:
                    dados_por_supermercado[nome_supermercado] = []

                # Adiciona o produto e seus preços à lista do supermercado
                dados_por_supermercado[nome_supermercado].append([nome_produto, precos])

    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return  # Encerra a execução se o arquivo não existe
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return

    # --- Etapa 2: Gerar um arquivo de saída para cada supermercado ---
    if not dados_por_supermercado:
        print("Nenhum dado válido foi processado. Nenhum arquivo de saída será gerado.")
        return

    print("\nIniciando a geração dos arquivos de saída...")
    for supermercado, produtos in dados_por_supermercado.items():

        # Ordena a lista de produtos em ordem alfabética pelo nome
        produtos.sort(key=lambda item: item[0])

        # Define o nome do arquivo de saída
        nome_arquivo_saida = f"{supermercado.replace(' ', '_')}.csv"

        # --- Etapa 3: Escrever os dados processados no arquivo de saída ---
        try:
            with open(nome_arquivo_saida, 'w', encoding='utf-8', newline='') as f_out:
                for item in produtos:
                    nome_prod = item[0]
                    lista_precos = item[1]

                    # Calcula a média usando a função definida
                    media_precos = calcular_media(lista_precos)

                    # Escreve a linha formatada no arquivo
                    linha_saida = f"{nome_prod};{media_precos:.2f}\n"
                    f_out.write(linha_saida.replace('.', ','))  # Escreve com vírgula decimal

                print(f"-> Arquivo '{nome_arquivo_saida}' gerado com sucesso!")

        except IOError as e:
            print(f"ERRO: Não foi possível escrever no arquivo '{nome_arquivo_saida}'. Motivo: {e}")
        except Exception as e:
            print(f"ERRO: Ocorreu um erro inesperado ao gerar o arquivo '{nome_arquivo_saida}': {e}")


# --- Início da Execução do Programa ---
if __name__ == "__main__":
    # Nome do arquivo de entrada (deve estar no mesmo diretório)
    ARQUIVO_ENTRADA_CSV = 'produtos_s2.csv'
    processar_dados_e_gerar_arquivos(ARQUIVO_ENTRADA_CSV)