
n = 11

isPlus = True
mid = int(n/2)

n_opertion = 0
n_rows = 0

import numpy as np
arr = np.zeros([n,n])
r,c = mid,mid
count = 0
arr[r,c] = count
count+=1
n_opertion+=1
while(n_rows < n-1):
    if isPlus:
        for i in range(n_opertion):
            c+=1
            arr[r,c]=count
            count+=1
        for i in range(n_opertion):
            r+=1
            arr[r,c]=count
            count+=1
    else:
        for i in range(n_opertion):
            c-=1
            arr[r,c]=count
            count+=1
        for i in range(n_opertion):
            r-=1
            arr[r,c]=count
            count+=1
    n_opertion+=1
    isPlus = not isPlus
    n_rows+=1

print(arr)
