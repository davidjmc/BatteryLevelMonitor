def main():
    r = range(0, 100, 5)
    number = float(input('Enter a number : '))

    if number in r:
        print(number, 'is present in the range.')
    else :
        print(number, 'is not present in the range.')


while True:
    main()