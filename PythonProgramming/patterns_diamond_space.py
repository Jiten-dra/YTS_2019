noofstars = int(input("enter number"))

mid = int(noofstars/2)+1
star = 1
blank = int(noofstars/2)

for i in range (0, mid,1):

    for b in range(0,blank,1):
        print("  ",end="")
    for s in range (0,star,1):
        print("* ",end="")
    blank = blank - 1
    star = star + 2
    print("")

#print(blank)
#print((star))
blank =1
star = star - 4
for i in range (mid, noofstars,1):

    for b in range(0,blank,1):
        print("  ",end="")
    for s in range (0,star,1):
        print("* ",end="")
    blank = blank + 1
    star = star - 2
    print("")