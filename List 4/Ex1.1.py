import time

def fibonacci_iterativo(n):
    sequencia = []
    a, b = 0, 1
    for _ in range(n):
        sequencia.append(a)
        a, b = b, a + b
    return sequencia

def fibonacci_recursivo(n):
    def fib(k):
        if k == 0:
            return 0
        elif k == 1:
            return 1
        else:
            return fib(k - 1) + fib(k - 2)

    return [fib(i) for i in range(n)]

def imprimir_resultados(nome, sequencia, tempo_execucao):
    soma = sum(sequencia)
    media = soma / len(sequencia) if sequencia else 0
    print(f"\nMétodo {nome}:")
    print("Série:", sequencia)
    print("Soma:", soma)
    print("Média:", media)
    print(f"Tempo de execução: {tempo_execucao:.6f} segundos")

def main():
    try:
        n = int(input("Digite o valor de n: "))
        if n < 0:
            raise ValueError("n deve ser um número inteiro não negativo.")

        inicio = time.time()
        seq_iter = fibonacci_iterativo(n)
        tempo_iter = time.time() - inicio
        imprimir_resultados("Iterativo", seq_iter, tempo_iter)

        inicio = time.time()
        seq_rec = fibonacci_recursivo(n)
        tempo_rec = time.time() - inicio
        imprimir_resultados("Recursivo", seq_rec, tempo_rec)

    except ValueError as e:
        print("Erro:", e)
    
    main()

if __name__ == "__main__":
    main()