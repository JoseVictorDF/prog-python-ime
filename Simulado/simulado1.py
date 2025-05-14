CODE_LENGTH = 4

def checkUserCode(code):
    if len(code) == CODE_LENGTH and int(code) >= 1 and int(code) <= 9999:
        return True
    return False

def checkUserAge(age):
    if int(age) >= 18:
        return True
    return False

def addUserLengthToGroupsDictionary(lengthGroupDict, length):
    if isinstance(length, float):
        if length >= 1.95:
            lengthGroupDict["E"].append(length)
        elif length >= 1.75:
            lengthGroupDict["D"].append(length)
        elif length >= 1.55:
            lengthGroupDict["C"].append(length)
        elif length >= 1.35:
            lengthGroupDict["B"].append(length)
        else:
            lengthGroupDict["A"].append(length)

def main():
    try:
        lengthGroupsDictionary = {"A":[], "B":[], "C":[], "D":[], "E":[]}
        lengthsList = []
        userCode = 0
        while userCode != "-1":
            userCode = input("Digite um código de 4 números ou -1 para terminar:")
            while userCode != "-1" and not checkUserCode(userCode):
                print("Código inválido, tente novamente;")
                userCode = input("Digite um código de 4 números ou -1 para terminar:")
            if userCode == "-1":
                break

            userAge = input("Informe sua idade:")
            if not checkUserAge(userAge):
                print("Idade inválida, precisa ter 18 anos ou mais;")
                break
            
            userLength = input("Digite sua altura em metros:")
            userLength = float(str.replace(userLength, ",", "."))
            while userLength < 1:
                print("Altura inválida, tente novamente:")
                userLength = input("Digite sua altura em metros:")
                userLength = float(str.replace(userLength, ",", "."))
            lengthsList.append(userLength)
            addUserLengthToGroupsDictionary(lengthGroupsDictionary, userLength)
        lengthsSum = 0
        print(lengthsList)
        lengthsCount = len(lengthsList)
        print(lengthGroupsDictionary.items())
        for length in lengthsList:
            lengthsSum += length
        print(f"A média das alturas é {lengthsSum / lengthsCount}")
        print("Faixa --- Percentual")
        print(f"A --- {(len(lengthGroupsDictionary['A']) * 100.0) / lengthsCount}%")
        print(f"B --- {(len(lengthGroupsDictionary['B']) * 100.0) / lengthsCount}%")
        print(f"C --- {(len(lengthGroupsDictionary['C']) * 100.0) / lengthsCount}%")
        print(f"D --- {(len(lengthGroupsDictionary['D']) * 100.0) / lengthsCount}%")
        print(f"E --- {(len(lengthGroupsDictionary['E']) * 100.0) / lengthsCount}%")

    except Exception as ex:
        print(f"Ocorreu um erro, tente novamente: Erro: {ex}")
        main()

main()