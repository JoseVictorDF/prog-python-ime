def reverseNumbersList(numbersList):
    reversedNumbersList = []
    for i in range(len(numbersList), 0, -1):
        reversedNumbersList.append(numbersList[i-1])
    return reversedNumbersList


def main():
    numbersList = [1,2,3,4,5]
    reversedNumbersList = reverseNumbersList(numbersList)
    print(f'The reverse of list {numbersList} is {reversedNumbersList};')

main()