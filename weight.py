import pprint
import time
from random import randint, random
from random import seed
from tabulate import tabulate

def diff(x,y):
    if x >= y:
        return abs((x - y) / x)

    return abs((y - x) / y)

def main():
    size = 100
    seed(randint(1, 100))
    weights = [ x / size for x in range(size) ]
    rndList = [randint(1,100) * random() for x in range(size)]
    # 1: The rand nums, 2: weights for rand nums
    adict = {1:[], 2:[0 for x in range(size)]}

    # pprint.pp(rndList)

    num = randint(1,100)
    adict[1] = rndList

    # pprint.pp(adict[1])
    # print(f'num is {num}')

    i = 0
    lst = []
    # find the ratio btwn lst nums and num
    while i < size:
       # lst.append(rndList[i] / num)
       lst.append(diff(num,rndList[i]))
       i += 1

    # pprint.pp(lst)

    # the highest ratio gets the highest weight
    i = 0
    while len(weights) > 0 and i < size:
        # print(f'sainity: {lst.index(min(lst))}')
        adict[2][lst.index(min(lst))] = weights.pop()
        lst[lst.index(min(lst))] = 999.999

    # print(tabulate(adict, headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    startTime = time.time()
    main()
    elapsedTime = time.time() - startTime
    print(f'It took {elapsedTime}s')
