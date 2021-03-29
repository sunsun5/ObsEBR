import pandas as pd
from itertools import product
from functions import overlap

Intervals1 = pd.read_excel('intervals_an/intervals-0.985.xlsx', index_col=0)
Intervals2 = pd.read_excel('intervals_an/intervals-0.993.xlsx', index_col=0)
print(Intervals1)
for (i1,int1),(i2,int2) in product(
        enumerate(Intervals1),enumerate(Intervals2)):
    if overlap(int1,int2):
        print(i1,i2)