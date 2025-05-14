def verificar_progressao(seq):
    if len(seq) < 2:
        return 0  # Não é possível determinar PA ou PG

    # Verificação de PA
    razao_pa = seq[1] - seq[0]
    eh_pa = all(seq[i + 1] - seq[i] == razao_pa for i in range(len(seq) - 1))

    # Verificação de PG
    if seq[0] == 0:
        eh_pg = False
    else:
        try:
            razao_pg = seq[1] / seq[0]
            eh_pg = all(seq[i] != 0 and seq[i + 1] / seq[i] == razao_pg for i in range(len(seq) - 1))
        except ZeroDivisionError:
            eh_pg = False

    if eh_pa:
        return 1
    elif eh_pg:
        return 2
    else:
        return 0

def main():
    try:
        entrada = input("Digite os números da sequência separados por espaço: ")
        numeros = list(map(float, entrada.strip().split()))

        if len(numeros) < 2:
            raise ValueError("A sequência deve conter pelo menos dois números.")

        resultado = verificar_progressao(numeros)

        if resultado == 1:
            print("A sequência é uma PA.")
        elif resultado == 2:
            print("A sequência é uma PG.")
        else:
            print("A sequência não é PA nem PG.")

    except ValueError as e:
        print("Erro:", e)

if __name__ == "__main__":
    main()