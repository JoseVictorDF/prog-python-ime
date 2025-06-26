import numpy as np

# Cria um array 2D (5x4) com valores de ponto flutuante aleatórios entre 0 e 100
array_aleatorio = np.random.uniform(low=0.0, high=100.0, size=(5, 4))
print("Array Aleatório Original:")
print(array_aleatorio)
print("-" * 30)

# a) Valor máximo, sua posição e valor médio do array completo
valor_maximo_total = np.max(array_aleatorio)
posicao_maximo_flat = np.argmax(array_aleatorio)
# Converte o índice "achatado" (flat) para coordenadas de linha e coluna
posicao_maximo_2d = np.unravel_index(posicao_maximo_flat, array_aleatorio.shape)
valor_medio_total = np.mean(array_aleatorio)

print(f"a) Análise do Array Completo:")
print(f"   - Valor Máximo: {valor_maximo_total:.2f}")
print(f"   - Posição (linha, coluna): {posicao_maximo_2d}")
print(f"   - Valor Médio: {valor_medio_total:.2f}")
print("-" * 30)

# b) Valor mínimo na linha que contém o valor máximo
linha_maximo = posicao_maximo_2d[0]
valor_minimo_na_linha = np.min(array_aleatorio[linha_maximo, :])

print(f"b) Análise da Linha com Valor Máximo:")
print(f"   - Valor Mínimo na Linha {linha_maximo}: {valor_minimo_na_linha:.2f}")
print("-" * 30)

# c) Valor máximo e médio por linha e coluna
max_por_coluna = np.max(array_aleatorio, axis=0)
media_por_coluna = np.mean(array_aleatorio, axis=0)
max_por_linha = np.max(array_aleatorio, axis=1)
media_por_linha = np.mean(array_aleatorio, axis=1)

print("c) Análise por Linha e Coluna:")
for i, val in enumerate(max_por_coluna):
    print(f"   - Coluna {i}: Máximo={val:.2f}, Média={media_por_coluna[i]:.2f}")

for i, val in enumerate(max_por_linha):
    print(f"   - Linha {i}: Máximo={val:.2f}, Média={media_por_linha[i]:.2f}")
print("-" * 30)

# Salvar o array em um arquivo de texto com valores separados por espaço
np.savetxt('array_ex1.txt', array_aleatorio, fmt='%.8f', delimiter=' ')
print("Array salvo com sucesso no arquivo 'array_ex1.txt'.")