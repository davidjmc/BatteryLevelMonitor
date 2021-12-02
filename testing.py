def xfrange(start, stop=None, step=None):
    if stop is None:
        stop = float(start)
        start = 0.0

    if step is None:
        step = 1.0

    cur = float(start)

    while cur < stop:
        yield cur
        cur += step

def main():
    r = range(0, 0.5, 0.1)
    number = float(input('Enter a number : '))

    if number in r:
        print(number, 'is present in the range.')
    else :
        print(number, 'is not present in the range.')


while True:
    main()

