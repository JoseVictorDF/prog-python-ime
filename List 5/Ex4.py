import numpy as np

# Nome dos arquivos
arquivo_principal = 'tabela_exemplo.txt'
arquivo_soma_linhas = 'soma_linhas_ex4.txt'
arquivo_coluna_mse = 'coluna_mse_ex4.txt'

try:
    # Carregar dados do arquivo principal (separado por tabulação)
    dados = np.loadtxt(arquivo_principal, delimiter='\t')
    print(f"Dados carregados de '{arquivo_principal}' com formato {dados.shape}")
    print("-" * 40)

    # a) Estatísticas por coluna
    print("a) Estatísticas Descritivas por Coluna:")
    num_colunas = dados.shape[1]
    for i in range(num_colunas):
        coluna = dados[:, i]
        media = np.mean(coluna)
        mediana = np.median(coluna)
        desvio_padrao = np.std(coluna)
        minimo = np.min(coluna)
        maximo = np.max(coluna)
        print(f"  Coluna {i+1}:")
        print(f"    - Média: {media:.2f}")
        print(f"    - Mediana: {mediana:.2f}")
        print(f"    - Desvio Padrão: {desvio_padrao:.2f}")
        print(f"    - Mínimo: {minimo:.2f}")
        print(f"    - Máximo: {maximo:.2f}")
    print("-" * 40)

    # b) Salvar a soma das colunas para cada linha
    soma_linhas = np.sum(dados, axis=1)
    np.savetxt(arquivo_soma_linhas, soma_linhas, fmt='%.4f')
    print(f"b) A soma de cada linha foi salva em '{arquivo_soma_linhas}'.")
    print("-" * 40)
    
    # c) Verificar linhas com valores repetidos
    print("c) Verificação de Valores Repetidos nas Linhas:")
    encontrou_repetido = False
    for i, linha in enumerate(dados):
        # Se o número de elementos únicos for menor que o total, há repetição
        if len(np.unique(linha)) < len(linha):
            print(f"  [ALERTA] Valores repetidos encontrados na linha {i+1}: {linha}")
            encontrou_repetido = True
    if not encontrou_repetido:
        print("  - Nenhuma linha com valores repetidos foi encontrada.")
    print("-" * 40)
    
    # d) Erro Médio Quadrático (MSE)
    print("d) Cálculo do Erro Médio Quadrático (MSE):")
    # Gerar um segundo arquivo com uma coluna de dados aleatórios
    num_linhas_mse = dados.shape[0] - 50 # Número diferente de linhas, para teste
    coluna_aleatoria = np.random.rand(num_linhas_mse, 1) * 10000 
    np.savetxt(arquivo_coluna_mse, coluna_aleatoria, fmt='%.4f')
    print(f"  - Arquivo '{arquivo_coluna_mse}' com dados aleatórios foi gerado.")

    # Carregar dados para o cálculo do MSE
    coluna1 = dados[:, 0]
    coluna2 = np.loadtxt(arquivo_coluna_mse)

    # O cálculo deve ser feito no menor número de elementos entre as duas colunas
    n = min(len(coluna1), len(coluna2))
    
    # Fórmula do MSE: (1/n) * sum((y_true - y_pred)^2)
    erro_medio_quadratico = np.mean((coluna1[:n] - coluna2[:n])**2)
    print(f"  - O Erro Médio Quadrático entre a coluna 1 e o novo arquivo é: {erro_medio_quadratico:.2f}")

except FileNotFoundError:
    print(f"Erro: O arquivo '{arquivo_principal}' não foi encontrado.")
except Exception as e:
    print(f"Ocorreu um erro: {e}")