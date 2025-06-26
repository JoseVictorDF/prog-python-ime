import numpy as np

arquivo_entrada_notas = 'notas.csv'
arquivo_saida_classificacao = 'classificacao_final.csv'

try:
    # Definir a estrutura de dados (dtype) para o array estruturado
    # 'U50' significa uma ‘string’ Unicode de até 50 caracteres
    dtype_alunos = [
        ('codigo_aluno', int), 
        ('nome', 'U50'), 
        ('codigo_turma', int), 
        ('nome_turma', 'U50'), 
        ('media', float)
    ]

    # Carregar os dados do CSV usando genfromtxt, que é ótimo para dados mistos
    dados_alunos = np.genfromtxt(
        arquivo_entrada_notas, 
        delimiter=',', 
        dtype=dtype_alunos
    )

    print("Dados Originais:")
    print(dados_alunos)
    print("-" * 50)
    
    # Ordenar o array com múltiplos critérios.
    # A ordem no parâmetro 'order' é importante para o desempate.
    # A ordenação padrão é crescente.
    dados_ordenados = np.sort(dados_alunos, order=['media', 'nome_turma', 'nome'])
    
    # Como a ordenação por média deve ser decrescente, invertemos o array
    dados_ordenados = dados_ordenados[::-1]

    print("Classificação Final (Ordenada):")
    print(dados_ordenados)
    print("-" * 50)
    
    # Formato para salvar o arquivo de saída, mantendo o padrão original
    formato_saida = '%d,%s,%d,%s,%.1f'
    
    # Salvar o array ordenado no arquivo de saída
    np.savetxt(
        arquivo_saida_classificacao, 
        dados_ordenados, 
        fmt=formato_saida,
        delimiter=','
    )
    
    print(f"Arquivo '{arquivo_saida_classificacao}' gerado com sucesso!")

except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_entrada_notas}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")