# Define o alfabeto para referência
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encrypt(text_to_encrypt: str, block_size_n: int) -> str:
    """
    Criptografa o texto de acordo com a regra especificada.
    Considera apenas letras, convertidas para maiúsculas.
    O alfabeto é circular (Z + 1 = A).
    """
    # 1. Filtrar apenas letras e converter para maiúsculas
    filtered_uppercase_chars = [char.upper() for char in text_to_encrypt if char.isalpha()]
    
    # Se não houver letras, retorna uma string vazia
    if not filtered_uppercase_chars:
        return ""

    encrypted_output_chars = []
    
    # 2. Processar o texto em blocos de tamanho block_size_n
    for i in range(0, len(filtered_uppercase_chars), block_size_n):
        current_block = filtered_uppercase_chars[i : i + block_size_n]
        
        # 3. Criptografar cada caractere no bloco atual
        for j, char_in_block in enumerate(current_block):
            # 'j' é o índice 0-based no bloco,
            # o deslocamento é (j + 1) conforme a regra (1ª letra +1, 2ª letra +2, etc.)
            shift_amount = j + 1
            
            try:
                original_char_index = ALPHABET.find(char_in_block)
                
                # Se o caractere não estiver no ALPHABET (não deveria acontecer após filtragem)
                if original_char_index == -1:
                    # Para robustez, embora a filtragem deva prevenir isso.
                    # Poderia adicionar o caractere original ou pular.
                    # Aqui, vamos assumir que a filtragem garante que está no ALPHABET.
                    pass # Ou raise um erro se isso for uma condição inesperada

                # Calcular o novo índice com o deslocamento, de forma circular
                new_char_index = (original_char_index + shift_amount) % len(ALPHABET)
                
                encrypted_output_chars.append(ALPHABET[new_char_index])
            
            except Exception as e:
                # Tratamento de erro genérico para uma falha inesperada no processamento do caractere
                print(f"Aviso: Erro ao processar o caractere '{char_in_block}': {e}")
                # Decide-se pular o caractere em caso de erro interno inesperado.
                # Para este problema, é improvável que ocorra com a lógica atual.
                pass
                
    # 4. Juntar todos os caracteres criptografados em uma única string
    return "".join(encrypted_output_chars)

def main():
    """
    Função principal para obter entradas do usuário e imprimir o resultado.
    """
    print("--- Programa de Criptografia Simples ---")
    
    try:
        phrase_input = input("Digite a frase a ser criptografada: ")
        n_input_str = input("Digite o valor de n (tamanho do bloco, ex: 5): ")
        
        # Validar e converter n para inteiro
        block_size = int(n_input_str) 
        
        if block_size <= 0:
            print("Erro: O valor de n (tamanho do bloco) deve ser um inteiro positivo.")
            return # Encerra a execução se n for inválido

        # Chamar a função de criptografia
        encrypted_message = encrypt(phrase_input, block_size)
        
        if not encrypted_message:
            # Se a frase original não continha letras
            print("Resultado: Nenhuma letra na frase fornecida para criptografar.")
        else:
            # Imprimir o resultado final
            print(f"Texto criptografado: {encrypted_message}")

    except ValueError:
        # Captura erro se int(n_input_str) falhar (ex: usuário digita texto)
        print("Erro: O valor de n deve ser um número inteiro válido.")
    except Exception as e:
        # Captura quaisquer outros erros inesperados durante a execução
        print(f"Ocorreu um erro inesperado no programa: {e}")

if __name__ == "__main__":
    main()