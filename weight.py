import pprint
import time
from random import randint, random
from random import seed
from tabulate import tabulate

seed(randint(1, 100))
size = 1000
rndList = [randint(1,100) * random() for x in range(size)]
adict = {1:[], 2:[0 for x in range(size)]}
adict[1] = rndList
num = randint(1,100)
ignoreIndx = []
weights = [ x / size for x in range(size) ]
checks = [False for x in range(size)]

def diff(x,y):
    if x >= y:
        return abs((x - y) / x)

    return abs((y - x) / y)

# visted -> list of visted indexs (pass [] when called)
# items  -> list of items we need to assign weights to (pass rndList)
# weights -> list of weights (pass [x / size for x in range(size)] when called)
# closest -> closest val to num (pass rndList[0] when called)
# curr    -> curr value in the list (pass the first element when called)
# indx    -> indx of curr value in the list (pass 0 when called)
def weightAlg3(items: list, visted: list, weights: list, closest, curr, indx):
    global size
    global adict
    global num

    if(len(weights) == 0):
        return True

    if(diff(num, curr) <= diff(num, closest)) and indx < size:
        weightAlg3(items, visted, weights, curr, items[indx + 1], indx + 1)
    elif indx < size:
        weightAlg3(items,visted,weights,closest,items[indx + 1], indx + 1)



def weightAlg2(size: int):
    # 1: The rand nums, 2: weights for rand nums
    global adict
    global rndList
    global num
    global ignoreIndx
    global checks

    adict[1] = rndList
    i = 0
    ourNum = num
    # assume the first element is the closest
    closest = rndList[0]
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
    global weights
    global checks


    # 1: The rand nums, 2: weights for rand nums

    # pprint.pp(rndList)


    # pprint.pp(adict[1])
    # print(f'num is {num}: Alg1')

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
    weightAlg1(size)
    # print(tabulate(adict, headers='keys', tablefmt='fancy_grid'))

if __name__ == '__main__':
    startTime = time.time()
    main()
    elapsedTime = time.time() - startTime
    print(elapsedTime)
