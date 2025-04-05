def reverseNumbersList(numbersList):
    reversedNumbersList = []
    for i in range(len(numbersList), 0, -1):
        reversedNumbersList.append(numbersList[i-1])
    return reversedNumbersList

def convertNumberToBase(number, base, baseToConvert):
    decimalNum = 0
    if base != 10:
    # Convert to decimal base
        for digit in number:
            decimalNum = decimalNum * base + int(digit)
    else:
        decimalNum = int(number)
    
    if base != baseToConvert:
    # Convert from decimal base to baseToConvert
        digits = []
        while decimalNum > 0:
            digits.append(str(decimalNum % baseToConvert))
            decimalNum = decimalNum // baseToConvert
        # Reverse the digits and join them into a string
        return ''.join(reverseNumbersList(digits))
    else:
        return number


def main():
    try:
        doNext = 'y'
        while doNext == 'y':
            strNumber = input('Please insert a number:')
            base = int(input('Please insert the base of your number:'))
            baseToConvert = int(input('Please insert the base you want to convert your number:'))
            convertedNumber = convertNumberToBase(strNumber, base, baseToConvert)
            print(f'The number {strNumber} in base {baseToConvert} is {convertedNumber};')    
            doNext = input('\nWant to calc another number?(y/n)')
    except Exception as ex:
        print(f'An Exception occurred, please try again; Exception: {ex}')
        main()

main()