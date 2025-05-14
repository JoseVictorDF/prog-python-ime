def getMediaFromNumberList(numberList):
    return sum(numberList)/len(numberList)

def getSumMediaMinMaxFromNumberList(numberList):
    return (sum(numberList), getMediaFromNumberList(numberList), min(numberList), max(numberList))

def main():
    numberList = [1,2,3,4,5]
    mathTuple = getSumMediaMinMaxFromNumberList(numberList)
    print(f'Tuple values: {mathTuple}')

main()   