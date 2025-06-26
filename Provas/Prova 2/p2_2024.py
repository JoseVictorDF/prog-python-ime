import numpy as np
import sys


def verifica_repetidos_np(coluna: np.ndarray) -> bool:
    """
    Verifica se existem valores repetidos em um array NumPy (coluna).

    Args:
        coluna: Um array NumPy de 1 dimensão.

    Returns:
        True se houver valores repetidos, False caso contrário.
    """
    # np.unique retorna apenas os elementos únicos do array.
    # Se o tamanho do array de elementos únicos for menor que o original,
    # significa que havia elementos duplicados.
    return np.unique(coluna).size < coluna.size


def processar_arquivos_numpy():
    """
    Função principal que orquestra a leitura, processamento e escrita dos arquivos
    utilizando a biblioteca NumPy.
    """
    # Nomes dos arquivos
    ARQUIVO_DADOS = 'dados.txt'
    ARQUIVO_MODELO = 'modelo.txt'
    ARQUIVO_DADOS_ORDENADOS = 'dados_ordenados.txt'
    ARQUIVO_SAIDA = 'saida.txt'

    # --- Leitura dos arquivos diretamente para arrays NumPy ---
    try:
        # np.loadtxt lê o arquivo de texto e o converte diretamente em um array NumPy
        dados_array = np.loadtxt(ARQUIVO_DADOS)
        # Garante que seja um array 2D mesmo que tenha apenas uma linha
        if dados_array.ndim == 1:
            dados_array = dados_array.reshape(1, -1)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{ARQUIVO_DADOS}' não foi encontrado.")
        sys.exit(1)
    except ValueError:
        print(f"Erro: O arquivo '{ARQUIVO_DADOS}' contém dados em formato inválido.")
        sys.exit(1)

    try:
        modelo_array = np.loadtxt(ARQUIVO_MODELO)
        # Garante que seja um array 1D mesmo que tenha apenas um valor
        if modelo_array.ndim == 0:
            modelo_array = modelo_array.reshape(1)

    except FileNotFoundError:
        print(f"Erro: O arquivo '{ARQUIVO_MODELO}' não foi encontrado.")
        sys.exit(1)
    except ValueError:
        print(f"Erro: O arquivo '{ARQUIVO_MODELO}' contém dados em formato inválido.")
        sys.exit(1)

    # a) Verificar se há valores repetidos em alguma coluna
    # O .T transpõe o array (linhas viram colunas e vice-versa)
    for i, coluna in enumerate(dados_array.T):
        if verifica_repetidos_np(coluna):
            print(f"Alerta: Valores repetidos encontrados na coluna {i + 1} do arquivo '{ARQUIVO_DADOS}'.")

    # b) Ordenar as colunas do array
    # O axis=0 especifica que a ordenação deve ser feita ao longo das colunas
    dados_ordenados_array = np.sort(dados_array, axis=0)

    # Salvar o resultado no arquivo 'dados_ordenados.txt'
    # O fmt define o formato de escrita dos números
    try:
        np.savetxt(ARQUIVO_DADOS_ORDENADOS, dados_ordenados_array, fmt='%g', delimiter=' ')
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{ARQUIVO_DADOS_ORDENADOS}': {e}")
        sys.exit(1)

    # c) Gerar o arquivo 'saida.txt'
    # Define n como o menor número de linhas
    n = min(dados_ordenados_array.shape[0], modelo_array.shape[0])

    # Utiliza apenas as primeiras 'n' linhas dos arrays
    dados_para_media = dados_ordenados_array[:n]
    modelo_para_erro = modelo_array[:n]

    # i) Calcula a média de cada linha de forma vetorizada (tudo de uma vez)
    # O axis=1 especifica que a média deve ser calculada ao longo das linhas
    medias = dados_para_media.mean(axis=1)

    # ii) Calcula o erro de forma vetorizada
    # Evita o aviso de "division by zero" tratando o caso onde a média é 0
    # np.where(condição, valor_se_verdadeiro, valor_se_falso)
    erros = np.where(
        medias != 0,
        np.abs(medias - modelo_para_erro) / np.abs(medias),
        0.0  # Define erro como 0 se a média for 0
    )

    # Junta as colunas de médias e erros em um único array para salvar
    saida_array = np.column_stack((medias, erros))

    try:
        # Salva o resultado final com 6 casas decimais
        np.savetxt(ARQUIVO_SAIDA, saida_array, fmt='%.6f', delimiter=' ')
    except IOError as e:
        print(f"Erro ao escrever no arquivo '{ARQUIVO_SAIDA}': {e}")
        sys.exit(1)

    print(f"Processamento com NumPy concluído com sucesso!")
    print(f"Arquivos gerados: '{ARQUIVO_DADOS_ORDENADOS}' e '{ARQUIVO_SAIDA}'.")


# --- Execução do Programa ---
if __name__ == "__main__":
    # Certifique-se de ter o NumPy instalado:
    # pip install numpy

    # Use os mesmos arquivos 'dados.txt' e 'modelo.txt' do exemplo anterior
    processar_arquivos_numpy()