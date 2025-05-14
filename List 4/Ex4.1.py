import random

def gerar_matriz(linhas, colunas, min_valor=0, max_valor=100):
    return [[random.randint(min_valor, max_valor) for _ in range(colunas)] for _ in range(linhas)]

def encontrar_minimax(matriz):
    maior = float('-inf')
    linha_maior = 0
    for i, linha in enumerate(matriz):
        for valor in linha:
            if valor > maior:
                maior = valor
                linha_maior = i

    linha_alvo = matriz[linha_maior]
    minimax = min(linha_alvo)
    coluna_minimax = linha_alvo.index(minimax)

    return minimax, (linha_maior, coluna_minimax)

def imprimir_matriz(matriz):
    print("\nMatriz gerada:")
    for linha in matriz:
        print(linha)

def main():
    try:
        linhas = int(input("Digite o número de linhas da matriz: "))
        colunas = int(input("Digite o número de colunas da matriz: "))
        if linhas <= 0 or colunas <= 0:
            raise ValueError("Dimensões da matriz devem ser positivas.")

        matriz = gerar_matriz(linhas, colunas)
        imprimir_matriz(matriz)

        minimax, posicao = encontrar_minimax(matriz)
        print(f"\nElemento minimax: {minimax}")
        print(f"Posição: linha {posicao[0]}, coluna {posicao[1]}")

    except ValueError as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()