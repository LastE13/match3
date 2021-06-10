mass = [[1, 0], [2, 0], [0, 0], [3, 0], [0, 0], [4, 0], [5, 0]]
k = len(mass)
z = True
while z == True:
    if k==len(mass):
        if mass[k-1][0] == 0:
            pass
    else:

        print("1")
        if mass[k-1][0] == 0:
            for i in range(k, len(mass)):
                mass[i-1], mass[i] = mass[i], mass[i-1]
                if mass[i-1][0] !=0:
                    mass[i-1][1] +=1

    if k>1:
        k-=1
    else:
        z = False
    print(mass)
