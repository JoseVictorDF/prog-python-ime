def busca_binaria(lista_ordenada: list, alvo: any) -> int:
    """
    Realiza uma busca binária em uma lista ordenada para encontrar um alvo.

    Args:
        lista_ordenada: A lista onde a busca será realizada. Deve estar ordenada.
        alvo: O elemento a ser procurado na lista.

    Returns:
        O índice do alvo na lista se encontrado, caso contrário -1.
    """
    baixo = 0
    alto = len(lista_ordenada) - 1

    while baixo <= alto:
        meio = (baixo + alto) // 2  # Encontra o índice do meio (divisão inteira)

        # Verifica se o alvo está no meio
        if lista_ordenada[meio] == alvo:
            return meio
        # Se o alvo é maior, ignora a metade esquerda
        elif lista_ordenada[meio] < alvo:
            baixo = meio + 1
        # Se o alvo é menor, ignora a metade direita
        else:
            alto = meio - 1

    return -1 # Alvo não encontrado na lista

# Programa para testar a função busca_binaria
if __name__ == '__main__':
    print("Testando o algoritmo de Busca Binária:\n")

    # Caso de teste 1: Lista de números inteiros
    numeros = [2, 5, 7, 8, 11, 12, 15, 18, 22, 25, 30]
    print(f"Lista de números: {numeros}")
    alvos_numeros = [7, 25, 2, 30, 13, 0] # Alvos para testar (existentes e inexistentes)
    for alvo in alvos_numeros:
        indice = busca_binaria(numeros, alvo)
        if indice != -1:
            print(f"  Elemento {alvo} encontrado no índice {indice}.")
        else:
            print(f"  Elemento {alvo} não encontrado na lista.")
    print("-" * 30)

    # Caso de teste 2: Lista de strings (deve estar ordenada)
    palavras = ["abacaxi", "banana", "cereja", "damasco", "figo", "goiaba", "laranja"]
    print(f"Lista de palavras: {palavras}")
    alvos_palavras = ["banana", "laranja", "abacate", "uva"]
    for alvo in alvos_palavras:
        indice = busca_binaria(palavras, alvo)
        if indice != -1:
            print(f"  Elemento '{alvo}' encontrado no índice {indice}.")
        else:
            print(f"  Elemento '{alvo}' não encontrado na lista.")
    print("-" * 30)

    # Caso de teste 3: Lista vazia
    lista_vazia = []
    print(f"Lista vazia: {lista_vazia}")
    alvo_vazia = 5
    indice = busca_binaria(lista_vazia, alvo_vazia)
    if indice != -1:
        print(f"  Elemento {alvo_vazia} encontrado no índice {indice}.")
    else:
        print(f"  Elemento {alvo_vazia} não encontrado na lista.")
    print("-" * 30)

    # Caso de teste 4: Lista com um único elemento
    lista_um_elemento = [42]
    print(f"Lista com um elemento: {lista_um_elemento}")
    alvos_um_elemento = [42, 10]
    for alvo in alvos_um_elemento:
        indice = busca_binaria(lista_um_elemento, alvo)
        if indice != -1:
            print(f"  Elemento {alvo} encontrado no índice {indice}.")
        else:
            print(f"  Elemento {alvo} não encontrado na lista.")
    print("-" * 30)

    # Caso de teste 5: Elemento não encontrado (menor que todos)
    numeros2 = [10, 20, 30, 40, 50]
    print(f"Lista de números: {numeros2}")
    alvo_menor = 5
    indice = busca_binaria(numeros2, alvo_menor)
    if indice != -1:
        print(f"  Elemento {alvo_menor} encontrado no índice {indice}.")
    else:
        print(f"  Elemento {alvo_menor} não encontrado na lista.")
    print("-" * 30)

    # Caso de teste 6: Elemento não encontrado (maior que todos)
    print(f"Lista de números: {numeros2}") # Usando a mesma lista numeros2
    alvo_maior = 55
    indice = busca_binaria(numeros2, alvo_maior)
    if indice != -1:
        print(f"  Elemento {alvo_maior} encontrado no índice {indice}.")
    else:
        print(f"  Elemento {alvo_maior} não encontrado na lista.")
    print("-" * 30)