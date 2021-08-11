# Weight Alg

## Alg1 -- FAILED

[0.01,0.02,...,0.98,0.99] : weights

to hit is to assign a weight

46040.0 : current_price

[46033,...,46038,46040,46041,...] : asks

46033 - 46040.0 = -7
.
.
.
46038 - 46040.0 = -2
46040 - 46040 = 0

* When the diffrence is a float, hit

|  Price | Weight    |
|--------|-----------|
| 46040  | 0.99      |

[0.01,0.02,...,0.98] : weights
*poped a weight*

## Alg 2

Take the ratio of the price to the

current_price. Smallest ratio gets

assigned highest weight

