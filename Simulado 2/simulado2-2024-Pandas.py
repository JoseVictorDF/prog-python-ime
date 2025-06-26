# -*- coding: utf-8 -*-

"""
Solução do exercício utilizando a biblioteca Pandas, a ferramenta
padrão da indústria para manipulação de dados em Python.
"""
import pandas as pd
import os


def processar_com_pandas(arquivo_entrada: str):
    """
    Lê os dados, processa e gera os arquivos de saída, tudo com o poder do Pandas.

    Args:
        arquivo_entrada: O nome do arquivo .csv a ser lido.
    """
    # --- Passo 1: Ler e transformar os dados para um formato "Tidy" ---
    # Como o formato do CSV é irregular (número variável de preços),
    # vamos lê-lo linha por linha e construir uma lista de registros.

    dados_para_df = []
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            print(f"Lendo e transformando o arquivo: '{arquivo_entrada}'...")
            for linha in f:
                partes = linha.strip().split(';')
                nome_produto = partes[0]
                supermercado = partes[-1]
                precos_str = partes[1:-1]

                # Para cada preço na linha, criamos um registro separado
                for preco in precos_str:
                    dados_para_df.append({
                        'supermercado': supermercado,
                        'produto': nome_produto,
                        'preco': float(preco.replace(',', '.'))
                    })

    except FileNotFoundError:
        print(f"ERRO: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado ao ler o arquivo: {e}")
        return

    # Cria o DataFrame a partir da nossa lista de registros
    df = pd.DataFrame(dados_para_df)

    # Se nenhum dado foi lido, encerra
    if df.empty:
        print("Nenhum dado válido encontrado para processar.")
        return

    # --- Passo 2: Agrupar, Calcular a Média e Ordenar ---
    # Esta é a "mágica" do Pandas. Com uma única linha, fazemos tudo:
    # 1. Agrupamos por 'supermercado' e depois por 'produto'
    # 2. Calculamos a média ('mean') da coluna 'preco' para cada grupo
    # 3. Arredondamos o resultado para 2 casas decimais
    print("Agrupando dados e calculando médias...")
    dados_agregados = df.groupby(['supermercado', 'produto'])['preco'].mean().round(2).reset_index()
    dados_agregados = dados_agregados.rename(columns={'preco': 'media_preco'})

    # --- Passo 3: Salvar um arquivo CSV para cada supermercado ---
    print("Gerando arquivos de saída...")
    supermercados_unicos = dados_agregados['supermercado'].unique()

    for mercado in supermercados_unicos:
        nome_arquivo_saida = f"{mercado.replace(' ', '_')}.csv"

        # Filtra o DataFrame para conter apenas os dados do supermercado atual
        df_mercado = dados_agregados[dados_agregados['supermercado'] == mercado]

        # Seleciona, ordena e prepara os dados finais para salvar
        df_final = df_mercado[['produto', 'media_preco']].sort_values(by='produto')

        try:
            # O método .to_csv() do Pandas cuida de toda a escrita do arquivo
            df_final.to_csv(
                nome_arquivo_saida,
                sep=';',  # Define o separador como ponto e vírgula
                index=False,  # Não salva o índice do DataFrame no arquivo
                header=False,  # Não escreve o cabeçalho ('produto';'media_preco')
                decimal=','  # Usa vírgula como separador decimal
            )
            print(f"-> Arquivo '{nome_arquivo_saida}' gerado com sucesso!")
        except IOError as e:
            print(f"ERRO: Não foi possível escrever no arquivo '{nome_arquivo_saida}'. Motivo: {e}")


# --- Início da Execução do Programa ---
if __name__ == "__main__":
    # Certifique-se de ter o Pandas instalado: pip install pandas
    ARQUIVO_ENTRADA_CSV = 'produtos_s2.csv'
    processar_com_pandas(ARQUIVO_ENTRADA_CSV)