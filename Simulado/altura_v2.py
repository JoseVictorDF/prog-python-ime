N_CODIGO = 4
def verificarCodigo(cod):
    try:
        if len(cod)==N_CODIGO and int(cod)>=1 and int(cod)<=9999:
            return True
        else:
            return False
    except: 
        return False
    
def verificarIdade(idade):
    try:
        if int(idade)>17:
            return True
        else:
            return False
    except: 
        return False
    
def media(lista):
    return sum(lista)/len(lista)

print("Bem vindo!")
lista_alturas = []
registros = dict.fromkeys({"A","B","C","D","E"},0)
continua = True
while(continua):
    codigo = input("Digite o código: ")
    if codigo=="-1":
        break
    while (not verificarCodigo(codigo)):
        print("CARTAO INVALIDO. TENTE NOVAMENTE.")
        codigo = input("Digite o código: ")
        if codigo=="-1":
            continua = False
            break
    if continua:
        if not verificarIdade(input("Digite a idade: ")):
            print("IDADE FORA DA FAIXA.")
        else:
            try:
                altura = float(input("Digite a altura: "))                
                while (altura<1):
                    print("ALTURA INVÁLIDA. TENTE NOVAMENTE.")
                    altura = float(input("Digite a altura: "))
                lista_alturas += [altura]
                if altura<1.35:
                    faixa = "A"
                elif altura<1.55:
                    faixa = "B"
                elif altura<1.75:
                    faixa = "C"
                else:
                    faixa = "E"
                registros[faixa] += 1
            except:
                print("ERRO DE DIGITAÇÃO. TENTE NOVAMENTE.")
if len(lista_alturas)>0:
    print(f"\n\nAltura média: {media(lista_alturas):.2f} m")
    print(registros)
    print("\nFaixa --- Percentual")
    for k in registros:
        print(f"{k} --- {(registros[k]/len(lista_alturas))*100}%")
print("\nPrograma encerrado.")