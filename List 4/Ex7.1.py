def calcular_estatisticas_turma():
    """
    Recebe dados de alunos, calcula a média da turma e imprime
    alunos abaixo e acima/igual à média.
    """
    alunos_notas = {}
    MAX_ALUNOS = 30
    contador_alunos = 0

    print("Digite o número do aluno e a nota (separados por espaço).")
    print("Digite '0' para o número do aluno para encerrar a entrada.")

    while contador_alunos < MAX_ALUNOS:
        try:
            entrada = input(f"Aluno {contador_alunos + 1} (ou 0 para sair): ").strip()
            partes = entrada.split()

            if not partes:  # Entrada vazia
                print("Entrada inválida. Tente novamente.")
                continue

            numero_aluno_str = partes[0]
            numero_aluno = int(numero_aluno_str)

            if numero_aluno == 0:
                if contador_alunos == 0 and len(partes) > 1: # Caso digite "0 nota"
                    print("Número do aluno 0 não é permitido se houver nota. Entrada de dados encerrada.")
                elif len(partes) > 1 and numero_aluno == 0 : # Caso digite "0 nota" e não seja o primeiro
                     print("Número do aluno 0 encerra a leitura. Nenhuma nota será registrada para o aluno 0.")
                break

            if len(partes) < 2:
                print("Entrada incompleta. É necessário o número do aluno e a nota. Tente novamente.")
                continue

            nota_str = partes[1]
            nota = float(nota_str)

            if nota < 0 or nota > 10: # Supondo que a nota seja entre 0 e 10
                print("Nota inválida. A nota deve ser um valor entre 0 e 10. Tente novamente.")
                continue

            if numero_aluno in alunos_notas:
                print(f"O aluno com número {numero_aluno} já foi inserido. Tente novamente com um número diferente.")
                continue

            alunos_notas[numero_aluno] = nota
            contador_alunos += 1

        except ValueError:
            print("Entrada inválida. Certifique-se de que o número do aluno é um inteiro e a nota é um número real. Tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}. Tente novamente.")

    if not alunos_notas:
        print("\nNenhum dado de aluno foi inserido.")
        return

    # a) Armazenar os dados (já feito em alunos_notas)

    # b) Imprimir a média da turma
    soma_notas = sum(alunos_notas.values())
    media_turma = soma_notas / len(alunos_notas)
    print(f"\n--- Estatísticas da Turma ---")
    print(f"Número total de alunos: {len(alunos_notas)}")
    print(f"Média da turma: {media_turma:.2f}")

    # c) Imprimir os números dos alunos com nota abaixo da média
    alunos_abaixo_media = [aluno for aluno, nota in alunos_notas.items() if nota < media_turma]
    if alunos_abaixo_media:
        print("\nAlunos com nota ABAIXO da média:")
        for aluno in alunos_abaixo_media:
            print(f"  - Aluno número: {aluno} (Nota: {alunos_notas[aluno]:.2f})")
    else:
        print("\nNenhum aluno com nota abaixo da média.")

    # d) Imprimir os números dos alunos com nota acima ou na média
    alunos_acima_ou_na_media = [aluno for aluno, nota in alunos_notas.items() if nota >= media_turma]
    if alunos_acima_ou_na_media:
        print("\nAlunos com nota ACIMA ou IGUAL à média:")
        for aluno in alunos_acima_ou_na_media:
            print(f"  - Aluno número: {aluno} (Nota: {alunos_notas[aluno]:.2f})")
    else:
        print("\nNenhum aluno com nota acima ou igual à média.")

if __name__ == "__main__":
    calcular_estatisticas_turma()