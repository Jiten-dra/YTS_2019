noofstars = int(input("enter number"))


for row in range (0,noofstars+1,1):
    for st in range (0, row,1):
        print("*",end="")
    print("")

mid = int(noofstars/2)+1
print("mid value is ",mid)
star = 1
blank = int(noofstars/2)
print("blank ",blank)

for i in range (0, mid,1):

    for b in range(0,blank,1):
        print(" ",end="")
    for s in range (0,star,1):
        print("*",end="")
    blank = blank - 1
    star = star + 2
    print("")

#print(blank)
#print((star))
blank =1
star = star - 4
for i in range (mid, noofstars,1):

    for b in range(0,blank,1):
        print(" ",end="")
    for s in range (0,star,1):
        print("*",end="")
    blank = blank + 1
    star = star - 2
    print("")