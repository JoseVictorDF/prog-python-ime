def gerar_lista_unica_ordenada(lista1, lista2):
    # Converte para conjuntos para remover duplicados e faz a união
    conjunto = set(lista1) | set(lista2)
    return sorted(conjunto)

def main():
    try:
        entrada1 = input("Digite os números da primeira lista separados por espaço: ")
        entrada2 = input("Digite os números da segunda lista separados por espaço: ")

        lista1 = list(map(float, entrada1.strip().split()))
        lista2 = list(map(float, entrada2.strip().split()))

        resultado = gerar_lista_unica_ordenada(lista1, lista2)

        print("Lista resultante ordenada e sem repetição:", resultado)

    except ValueError:
        print("Erro: certifique-se de digitar apenas números separados por espaço.")

if __name__ == "__main__":
    main()