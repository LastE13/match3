# The script of the game goes in this file.
init python:
    import random

    k0=0
    k1=0
    k2=0
    nnn=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]
    mass=[[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10,[0]*10]
    x0=''
    x1=''

    def Check ():
        global k1, k2
        if (k2+3)<10:
            if mass[k1][k2+2]==mass[k1][k2+3]==mass[k1][k2]:
                mass[k1][k2], mass[k1][k2+1]=mass[k1][k2+1], mass[k1][k2]
        if (k2-3)>=0:
            if mass[k1][k2-2]==mass[k1][k2-3]==mass[k1][k2]:
                mass[k1][k2], mass[k1][k2-1]=mass[k1][k2-1], mass[k1][k2]
        if (k1+3)<10:
            if mass[k1+2][k2]==mass[k1+3][k2]==mass[k1][k2]:
                mass[k1][k2], mass[k1+1][k2]=mass[k1+1][k2], mass[k1][k2]
        if (k1-3)>=0:
            if mass[k1-2][k2]==mass[k1-3][k2]==mass[k1][k2]:
                mass[k1][k2], mass[k1-1][k2]=mass[k1-1][k2], mass[k1][k2]




    def delete():
        global x0, x1
        for i in range(0, 10):
            for j in range(0, 10):
                if mass[i][j]==x0:
                    if mass[i][j]==x1:
                        mas.pop(i, j)##########
                else:
                    x1=x0
            else:
                x0=x


    for i in range(0, 10):
        for j in range(0, 10):
            mass[i][j]=random.choice(img_list)
screen m3:
    tag menu
    add "#a0aaaf"

    for i in range(len(mass)):
        for j in range(len(mass[i])):
            imagebutton auto mass[i][j] xpos 500+72*j ypos 100+72*i action [SetVariable('k2',j), SetVariable('k1',i), Function(Check)]

    use navigation


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:
    call screen m3
    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
