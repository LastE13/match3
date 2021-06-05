# The script of the game goes in this file.
init python:
    import random

    zzz="0"
    k0=0
    k1=0
    k2=0
    m1=''
    m2=''
    m3=''
    m4=''
    m5=''
    nnn=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]
    mass=[[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14,[0]*14]

    def Check ():
        global zzz, k1, k2, m1, m2, m3, m4, m5
        zzz+="2"
        if k2+3<=14:
            zzz="q"
            m1=mass[k1][k2+2]
            m2=mass[k1][k2+3]
            m3=mass[k1][k2]
            if mass[k1][k2+2]==mass[k1][k2+3]==mass[k1][k2]:
                mass[k1][k2], mass[k1][k2+1]=mass[k1][k2+1], mass[k1][k2]
                zzz+="1"
        elif k2-3>=0:
            m1=mass[k1][k2-2]
            m2=mass[k1][k2-3]
            m3=mass[k1][k2]
            zzz="w"
            if mass[k1][k2-2]==mass[k1][k2-3]==mass[k1][k2]:
                mass[k1][k2], mass[k1][k2-1]=mass[k1][k2-1], mass[k1][k2]
                zzz+="11"
        if k1+3<=14:
            zzz="e"
            m4=mass[k1+2][k2]
            m5=mass[k1+3][k2]
            m3=mass[k1][k2]
            if mass[k1+2][k2]==mass[k1+3][k2]==mass[k1][k2]:
                mass[k1][k2], mass[k1+1][k2]=mass[k1+1][k2], mass[k1][k2]
                zzz+="111"
        if k1-3>=0:
            zzz="r"
            m4=mass[k1-2][k2]
            m5=mass[k1-3][k2]
            m3=mass[k1][k2]
            if mass[k1-2][k2]==mass[k1-3][k2]==mass[k1][k2]:
                mass[k1][k2], mass[k1-1][k2]=mass[k1-1][k2], mass[k1][k2]
                zzz+="1111"

    for i in range(0, 14):
        for j in range(0, 14):
            mass[i][j]=random.choice(img_list)
screen m3:
    tag menu
    add "#a0aaaf"


    #text '[mass]' xpos 800 ypos 20
    for i in range(len(mass)):
        for j in range(len(mass[i])):
            imagebutton auto mass[i][j] xpos 400+72*j ypos 10+72*i action [SetVariable('k2',j), SetVariable('k1',i), Function(Check)]
    text '[zzz] | [k1] | [k2] ' xpos 100 ypos 20
    text '[m1] | [m2] | [m3]' xpos 100 ypos 60
    text '[m4] | [m5] | [m3]' xpos 100 ypos 100
    use navigation


# Declare characters used by this game. The color argument colorizes the
# name of the character.

define e = Character("Eileen")


# The game starts here.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.


    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.


    # These display lines of dialogue.

    e "You've created a new Ren'Py game."
    call screen m3
    e "Once you add a story, pictures, and music, you can release it to the world!"

    # This ends the game.

    return
