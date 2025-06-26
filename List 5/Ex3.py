import numpy as np

# Gerar dados de amostra e centróides aleatoriamente
num_amostras = 20
num_centroides = 3

amostras = np.random.randint(0, 100, size=(num_amostras, 2))
centroides = np.random.randint(20, 80, size=(num_centroides, 2))

print("Pontos da Amostra (x, y):")
print(amostras)
print("\nCentróides (x, y):")
print(centroides)
print("-" * 30)

# Usando broadcasting para calcular a distância euclidiana de forma eficiente.
# A diferença `amostras[:, np.newaxis, :] - centroides` resulta em um array de
# formato (num_amostras, num_centroides, 2), contendo a diferença vetorial
# de cada amostra para cada centróide.
diferencas = amostras[:, np.newaxis, :] - centroides
distancias_quadradas = np.sum(diferencas**2, axis=2)
distancias = np.sqrt(distancias_quadradas)

# Encontra o índice do centróide mais próximo para cada amostra
indices_centroide_proximo = np.argmin(distancias, axis=1)

# Exibir os resultados
for i in range(num_amostras):
    ponto = amostras[i]
    id_centroide = indices_centroide_proximo[i]
    centroide_prox = centroides[id_centroide]
    print(f"Ponto {ponto} é mais próximo do Centróide {id_centroide} em {centroide_prox}")