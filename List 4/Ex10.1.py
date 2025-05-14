def bubble_sort(lista: list) -> None:
    """
    Ordena uma lista de elementos comparáveis utilizando o algoritmo Bubble Sort.
    A ordenação é feita in-place (a lista original é modificada).

    Args:
        lista: A lista a ser ordenada.
    """
    n = len(lista)
    # Itera por todos os elementos da lista
    for i in range(n):
        # Flag para otimizar: se nenhuma troca ocorrer nesta passagem, a lista já está ordenada.
        trocou = False
        # A última i elementos já estão no lugar certo
        for j in range(0, n - i - 1):
            # Compara elementos adjacentes
            if lista[j] > lista[j + 1]:
                # Troca os elementos se estiverem na ordem errada
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
                trocou = True
        # Se nenhuma troca foi feita nesta passagem, a lista está ordenada
        if not trocou:
            break

# Programa para testar a função bubble_sort
if __name__ == '__main__':
    print("Testando o algoritmo Bubble Sort:\n")

    # Caso de teste 1: Lista desordenada de números
    lista1 = [64, 34, 25, 12, 22, 11, 90]
    print(f"Lista original 1: {lista1}")
    bubble_sort(lista1)
    print(f"Lista ordenada 1: {lista1}\n")

    # Caso de teste 2: Lista já ordenada
    lista2 = [10, 20, 30, 40, 50]
    print(f"Lista original 2: {lista2}")
    bubble_sort(lista2)
    print(f"Lista ordenada 2: {lista2}\n")

    # Caso de teste 3: Lista em ordem inversa
    lista3 = [5, 4, 3, 2, 1]
    print(f"Lista original 3: {lista3}")
    bubble_sort(lista3)
    print(f"Lista ordenada 3: {lista3}\n")

    # Caso de teste 4: Lista com elementos duplicados
    lista4 = [5, 1, 4, 2, 8, 5, 1, 4]
    print(f"Lista original 4: {lista4}")
    bubble_sort(lista4)
    print(f"Lista ordenada 4: {lista4}\n")

    # Caso de teste 5: Lista vazia
    lista5 = []
    print(f"Lista original 5: {lista5}")
    bubble_sort(lista5)
    print(f"Lista ordenada 5: {lista5}\n")

    # Caso de teste 6: Lista com um único elemento
    lista6 = [42]
    print(f"Lista original 6: {lista6}")
    bubble_sort(lista6)
    print(f"Lista ordenada 6: {lista6}\n")

    # Caso de teste 7: Lista com números negativos e positivos
    lista7 = [-5, 10, -15, 0, 20, -25]
    print(f"Lista original 7: {lista7}")
    bubble_sort(lista7)
    print(f"Lista ordenada 7: {lista7}\n")

    # Caso de teste 8: Lista de strings (Bubble Sort também funciona)
    lista8 = ["banana", "abacaxi", "laranja", "maçã", "uva"]
    print(f"Lista original 8: {lista8}")
    bubble_sort(lista8)
    print(f"Lista ordenada 8: {lista8}\n")