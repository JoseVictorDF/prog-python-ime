def produto_escalar(vetor1, vetor2):
    return sum(a * b for a, b in zip(vetor1, vetor2))

def ler_vetor(numero):
    while True:
        try:
            entrada = input(f"Digite os 3 números reais do vetor {numero}, separados por espaço: ")
            vetor = list(map(float, entrada.strip().split()))
            if len(vetor) != 3:
                raise ValueError("O vetor deve ter exatamente 3 números.")
            return vetor
        except ValueError as e:
            print("Erro:", e)

def main():
    print("Cálculo do Produto Escalar entre dois vetores de 3 dimensões.")

    vetor1 = ler_vetor(1)
    vetor2 = ler_vetor(2)

    resultado = produto_escalar(vetor1, vetor2)
    print(f"Produto escalar: {resultado}")

if __name__ == "__main__":
    main()
