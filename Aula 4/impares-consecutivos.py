def calcTriangular(value):
    return value * (value + 1) / 2

def getFirstImpar(value):
    return 2 * calcTriangular(value - 1) + 1

def main():
    try:
        doNext = 'y'
        while doNext == 'y':
            value = int(input('Insert a number:'))
            impares = [int(getFirstImpar(value))]
            print(f'{value}^3 = {impares[0]}', end='')

            for i in range(0,value-1):
                impares.append(impares[i]+2)
                print(f' + {impares[i+1]}', end='')
                
            doNext = input('\nWant calc another number?(y/n)')

    except Exception as ex:
        print(f'You set an invalid number, please try again; Exception: {ex}')
        main()

main()