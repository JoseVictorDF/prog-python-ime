import numpy as np

# Nome do arquivo de entrada (gerado no exercício 1)
arquivo_entrada = 'array_ex1.txt'

try:
    # Carrega o array do arquivo, usando espaço como delimitador
    array_lido = np.loadtxt(arquivo_entrada, delimiter=' ')
    
    print(f"Array lido do arquivo '{arquivo_entrada}':")
    print(array_lido)
    print("-" * 30)

    # O restante do código é idêntico ao do Exercício 1,
    # demonstrando a generalização.

    # a) Valor máximo, sua posição e valor médio do array completo
    valor_maximo_total = np.max(array_lido)
    posicao_maximo_flat = np.argmax(array_lido)
    posicao_maximo_2d = np.unravel_index(posicao_maximo_flat, array_lido.shape)
    valor_medio_total = np.mean(array_lido)

    print(f"a) Análise do Array Completo:")
    print(f"   - Valor Máximo: {valor_maximo_total:.2f}")
    print(f"   - Posição (linha, coluna): {posicao_maximo_2d}")
    print(f"   - Valor Médio: {valor_medio_total:.2f}")
    print("-" * 30)

    # b) Valor mínimo na linha que contém o valor máximo
    linha_maximo = posicao_maximo_2d[0]
    valor_minimo_na_linha = np.min(array_lido[linha_maximo, :])

    print(f"b) Análise da Linha com Valor Máximo:")
    print(f"   - Valor Mínimo na Linha {linha_maximo}: {valor_minimo_na_linha:.2f}")
    print("-" * 30)

    # c) Valor máximo e médio por linha e coluna
    max_por_coluna = np.max(array_lido, axis=0)
    media_por_coluna = np.mean(array_lido, axis=0)
    max_por_linha = np.max(array_lido, axis=1)
    media_por_linha = np.mean(array_lido, axis=1)

    print("c) Análise por Linha e Coluna:")
    for i, val in enumerate(max_por_coluna):
        print(f"   - Coluna {i}: Máximo={val:.2f}, Média={media_por_coluna[i]:.2f}")

    for i, val in enumerate(max_por_linha):
        print(f"   - Linha {i}: Máximo={val:.2f}, Média={media_por_linha[i]:.2f}")

except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_entrada}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro ao processar o arquivo: {e}")