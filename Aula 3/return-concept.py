def calcConceptByGrade(grade):
    assert isinstance(grade, float), 'ooops'

    if grade >= 9.0:
        return 'E'
    elif grade >= 8.0:
        return 'MR'
    elif grade >= 7.0:
        return 'B'
    elif grade >= 5.0:
        return 'R'
    else:
        return 'I'

def main():
    try:
        grade = input('Please type your final grade:')
        concept = calcConceptByGrade(grade)
        print(f'Your final concept is {concept}.')
    except Exception as ex:
        print(f'You set an invalid grade, please try again; Exception: {ex}')
        main()

main()