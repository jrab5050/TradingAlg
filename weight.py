import pprint
import time
from random import randint, random
from random import seed
from tabulate import tabulate

seed(randint(1, 100))
size = 10
rndList = [randint(1,100) * random() for x in range(size)]
adict = {1:[], 2:[0 for x in range(size)]}
num = randint(1,100)
ignoreIndx = []

def diff(x,y):
    if x >= y:
        return abs((x - y) / x)

    return abs((y - x) / y)

def weightAlg2(size: int):
    # 1: The rand nums, 2: weights for rand nums
    global adict
    global rndList
    global num
    global ignoreIndx

    weights = [ x / size for x in range(size) ]

    adict[1] = rndList
    i = 0
    ourNum = num
    # assume the first element is the closest
    closest = rndList[0]
    checks = [False for x in range(size)]
    done = False # we will be done when all checks are true
    currWeight = weights.pop()
    adict[2][0] = currWeight

    print(f'num is {num}: Alg2')


    while not done and len(weights) > 0:
        if diff(num,rndList[i]) < diff(ourNum,closest) and i not in ignoreIndx:
            # print('in if 1')
            adict[2][i] = currWeight
            # print(f'Adding weight to index {i}')
            closest = rndList[i]

        if i == size - 1:
            # print('in if 2')
            ignoreIndx.insert(0,adict[1].index(closest))
            # print(f'The index of the closest value {adict[1].index(closest)}')
            # print(tabulate({'num': [num], 'closest': [closest]}, headers='keys',tablefmt='fancy_grid'))
            checks[adict[1].index(closest)] = True
            currWeight = weights.pop()
            ourNum = closest 
            if adict[1].index(closest) not in ignoreIndx:
                closest = adict[1][adict[1].index(closest)]
            else:
                closest = adict[1][0]
            i = 0

        else:
            # print('in else')
            i += 1

        if False not in checks:
            # print('In if 3')
            done = True

        # print(f'i is {i}')

def weightAlg1(size: int):

    global adict
    global rndList
    global num

    weights = [ x / size for x in range(size) ]

    seed(randint(1, 100))
    weights = [ x / size for x in range(size) ]
    rndList = [randint(1,100) * random() for x in range(size)]
    # 1: The rand nums, 2: weights for rand nums
    adict = {1:[], 2:[0 for x in range(size)]}

    # pprint.pp(rndList)

    num = randint(1,100)
    adict[1] = rndList

    # pprint.pp(adict[1])
    print(f'num is {num}: Alg1')

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


def main():
    # weightAlg1(size)
    # print(tabulate(adict, headers='keys', tablefmt='fancy_grid'))
    weightAlg2(size)
    print(tabulate(adict, headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    startTime = time.time()
    main()
    elapsedTime = time.time() - startTime
