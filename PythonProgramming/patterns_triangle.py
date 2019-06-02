noofstars = int(input("enter number"))

for row in range (0,noofstars+1,1):
    for st in range (0, row,1):
        print("*",end="")
    print("")

mid = int(noofstars/2)+1
star = 1
blank = int(noofstars/2)
