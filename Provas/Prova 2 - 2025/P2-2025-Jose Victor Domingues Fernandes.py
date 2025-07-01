import numpy as np

def ler_arquivo_taxas(arquivo_taxas: str):
    try:
        print(f"Lendo o arquivo de taxas: '{arquivo_taxas}'...")
        taxas_array = np.loadtxt(arquivo_taxas)
        return taxas_array
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_taxas}' não foi encontrado.")
        exit()
    except Exception as ex:
        print(f"Erro: Erro no acesso ao arquivo: '{arquivo_taxas}': {ex}.")
        exit()

def ler_arquivo_cotacoes(arquivo_cotacoes: str):
    cotacoes_array = []

    try:
        with open(arquivo_cotacoes, 'r') as f_in:
            print(f"Lendo o arquivo de cotacoes: '{arquivo_cotacoes}'...")
            for linha in f_in:
                cotacao = linha.strip().split(',')
                cotacoes_array.append(cotacao)

        f_in.close()
        return cotacoes_array
    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_cotacoes}' não foi encontrado.")
        exit()
    except Exception as ex:
        print(f"Erro: Erro no acesso ao arquivo: '{arquivo_cotacoes}': {ex}.")
        exit()

def calcular_cambio(cotacao, taxa):
    return cotacao * (1 + (taxa/100))

def gerar_cotacoes(arquivo_cotacoes: str, arquivo_taxas: str):
    taxas_array = ler_arquivo_taxas(arquivo_taxas)
    cotacoes_array = ler_arquivo_cotacoes(arquivo_cotacoes)

    POS_MES = 1
    POS_VALOR_COMPRA = 3
    POS_VALOR_VENDA = 4

    media_compra = 0
    media_venda = 0

    nome_arquivo_saida = 'cotacoes_calculadas.csv'

    try:
        with open(nome_arquivo_saida, mode='w') as arquivo_saida:
            for cotacao in cotacoes_array:
                mes = taxas_array[int(cotacao[POS_MES]) - 1]
                valor_compra = float(cotacao[POS_VALOR_COMPRA])
                valor_venda = float(cotacao[POS_VALOR_VENDA])

                cambio_compra = calcular_cambio(valor_compra, mes)
                cambio_venda = calcular_cambio(valor_venda, mes)

                if media_compra != 0:
                    media_compra = (media_compra + cambio_compra) / 2
                else:
                    media_compra = cambio_compra

                if media_venda != 0:
                    media_venda = (media_venda + cambio_venda) / 2
                else:
                    media_venda = cambio_venda

                arquivo_saida.write(str('%.6f' % cambio_compra) + ',' + str('%.6f' % cambio_venda) + '\n')

        arquivo_saida.close()

    except Exception as ex:
        print(f"Erro: Erro ao gerar o arquivo: '{nome_arquivo_saida}': {ex}.")
        exit()

    print(f"O Valor de câmbio de compra médio foi: {str('%.6f' % media_compra)}.")
    print(f"O Valor de câmbio de venda médio foi: {str('%.6f' % media_venda)}.")

if __name__ == "__main__":
    ARQUIVO_COTACOES_CSV = 'cotacoes.csv'
    ARQUIVO_TAXAS_TXT = 'taxas.txt'
    gerar_cotacoes(ARQUIVO_COTACOES_CSV, ARQUIVO_TAXAS_TXT)