def calcFatorialRecursive(value):
    assert isinstance(value, int), 'ooops'

    if value > 1:
        return value * calcFatorialRecursive(value - 1)
    elif 0:
        return 1
    else:
        return value

def calcFatorial(value):
    assert isinstance(value, int), 'ooops'

    result = 1

    while value > 1:
        result *= value
        value -= 1
    
    return result

def main():
    try:
        doNext = 'y'
        while doNext == 'y':
            value = int(input('Please type number to calc fatorial:'))
            fatorial = calcFatorialRecursive(value)
            print(f'Fatorial of {value} is {fatorial}.')
            doNext = input('Want calc another fatorial?(y/n)')
    except Exception as ex:
        print(f'You set an invalid number, please try again; Exception: {ex}')
        main()

main()