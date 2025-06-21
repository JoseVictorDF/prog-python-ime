import csv

def calcular_media_cambio(valores_cambio_mensal):
    """
    Calcula a média dos valores de câmbio mensais disponíveis.
    """
    # Implementar a lógica para calcular a média
    # Lembre-se de tratar casos onde a lista de valores pode estar vazia
    # ou conter valores não numéricos se não houver tratamento prévio.
    validos = [v for v in valores_cambio_mensal if isinstance(v, (int, float))]
    if not validos:
        return 0.0
    return sum(validos) / len(validos)

def processar_dados():
    dados_moeda_por_ano = {}
    dados_agencias_por_ano_e_nome = {}

    # 1. Ler o arquivo moeda.csv
    try:
        with open('moeda.csv', mode='r', newline='', encoding='utf-8') as file_moeda:
            leitor_csv_moeda = csv.reader(file_moeda)
            for linha in leitor_csv_moeda:
                # Ignorar linhas vazias ou cabeçalhos se houver
                if not linha or not linha[0].strip().isdigit():
                    continue
                ano = linha[0].strip()
                cotacoes_mensais = [float(c.strip()) for c in linha[1:] if c.strip()]
                dados_moeda_por_ano[ano] = cotacoes_mensais
    except FileNotFoundError:
        print("Erro: Arquivo 'moeda.csv' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler 'moeda.csv': {e}")
        return

    # 2. Ler o arquivo agencias.csv
    try:
        with open('agencias.csv', mode='r', newline='', encoding='utf-8') as file_agencias:
            leitor_csv_agencias = csv.reader(file_agencias)
            for linha in leitor_csv_agencias:
                # Ignorar linhas vazias ou cabeçalhos se houver
                if not linha or not linha[1].strip().isdigit(): # Checa se o segundo elemento (ano) é um dígito
                    continue
                nome_agencia = linha[0].strip()
                ano_referencia = linha[1].strip()
                taxas_mensais = [float(t.strip()) for t in linha[2:] if t.strip()]

                if ano_referencia not in dados_agencias_por_ano_e_nome:
                    dados_agencias_por_ano_e_nome[ano_referencia] = {}
                dados_agencias_por_ano_e_nome[ano_referencia][nome_agencia] = taxas_mensais
    except FileNotFoundError:
        print("Erro: Arquivo 'agencias.csv' não encontrado.")
        return
    except Exception as e:
        print(f"Erro ao ler 'agencias.csv': {e}")
        return

    # 3. Processar e gerar arquivos de saída
    anos_com_dados_agencia = False
    for ano, cotacoes_do_ano in dados_moeda_por_ano.items():
        if ano in dados_agencias_por_ano_e_nome:
            anos_com_dados_agencia = True
            agencias_do_ano = dados_agencias_por_ano_e_nome[ano]
            
            # Ordenar agências alfabeticamente
            nomes_agencias_ordenados = sorted(agencias_do_ano.keys())

            nome_arquivo_saida = f'resultado_{ano}.csv'
            try:
                with open(nome_arquivo_saida, mode='w', newline='', encoding='utf-8') as file_out:
                    escritor_csv = csv.writer(file_out)
                    
                    for nome_agencia in nomes_agencias_ordenados:
                        taxas_da_agencia = agencias_do_ano[nome_agencia]
                        valores_cambio_mensal = []
                        
                        # Garantir que temos o mesmo número de meses para cotações e taxas
                        # O problema implica que os dados mensais começam em janeiro e seguem em ordem.
                        num_meses = min(len(cotacoes_do_ano), len(taxas_da_agencia))
                        
                        for i in range(num_meses):
                            cotacao = cotacoes_do_ano[i]
                            taxa_percentual = taxas_da_agencia[i]
                            # valor_cambio = cotacao * (100 + taxa_percentual) / 100  [cite: 9]
                            valor_cambio = cotacao * (1 + taxa_percentual / 100)
                            valores_cambio_mensal.append(valor_cambio)
                        
                        media_cambio = calcular_media_cambio(valores_cambio_mensal)
                        
                        linha_saida = [nome_agencia]
                        linha_saida.extend([f"{valor:.4f}" for valor in valores_cambio_mensal])
                        # Adicionar placeholders se houver menos de 12 meses de dados para manter a estrutura
                        for _ in range(len(valores_cambio_mensal), 12):
                            linha_saida.append("") # Ou algum outro placeholder como 'N/A'

                        linha_saida.append(f"{media_cambio:.4f}")
                        escritor_csv.writerow(linha_saida)
                print(f"Arquivo '{nome_arquivo_saida}' gerado com sucesso.")
            except Exception as e:
                print(f"Erro ao escrever o arquivo '{nome_arquivo_saida}': {e}")
        else:
            print(f"Não foram encontrados dados de agências para o ano {ano} no arquivo 'agencias.csv'. Nenhum arquivo será gerado para este ano.") # [cite: 15]

    if not dados_moeda_por_ano:
        print("Nenhum dado encontrado em 'moeda.csv'. Nenhum arquivo de saída será gerado.")
    elif not anos_com_dados_agencia and dados_moeda_por_ano:
         # Esta condição pode ser redundante se a mensagem por ano já foi impressa.
         # Ajustar conforme a granularidade da mensagem desejada.
         pass


if __name__ == "__main__":
    processar_dados()