import random

def simular_lancamentos(quantidade):
    return [random.randint(1, 6) for _ in range(quantidade)]

def main():
    try:
        n = int(input("Quantos lançamentos de dado deseja simular? "))
        if n <= 0:
            raise ValueError("A quantidade deve ser maior que zero.")
        
        resultados = simular_lancamentos(n)
        print("Resultados dos lançamentos:", resultados)

    except ValueError as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()
