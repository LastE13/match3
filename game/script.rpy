# The script of the game goes in this file.
init python:
    import random

    k1 = 0
    k2 = 0
    img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]
    mass = [[0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [0]*10]
    numbutt = 0 #- Число кнопок в текущей группе
    imgbutt = '' #- картинка группы/(предыдущего поля)
    total = 0 #- Число групп

    def Check ():
        global k1, k2
        if (k2+3) < 10:
            if mass[k1][k2+2] == mass[k1][k2+3] == mass[k1][k2]:
                mass[k1][k2], mass[k1][k2+1] = mass[k1][k2+1], mass[k1][k2]
        if (k2-3) >= 0:
            if mass[k1][k2-2] == mass[k1][k2-3] == mass[k1][k2]:
                mass[k1][k2], mass[k1][k2-1] = mass[k1][k2-1], mass[k1][k2]
        if (k1+3) < 10:
            if mass[k1+2][k2] == mass[k1+3][k2] == mass[k1][k2]:
                mass[k1][k2], mass[k1+1][k2] = mass[k1+1][k2], mass[k1][k2]
        if (k1-3) >= 0:
            if mass[k1-2][k2] == mass[k1-3][k2] == mass[k1][k2]:
                mass[k1][k2], mass[k1-1][k2] = mass[k1-1][k2], mass[k1][k2]




    def an():
        #АНАЛИЗ ПО ГОРИЗОНТАЛИ
        for y range (1, 10):
            numbutt = 0 #Обнуляем число кнопок в текущей группе
            for x range (1, 10):
                if x == 1:
                    imgbutt = mass[y][x]
                if mass[y][x] == imgbutt:#imgbutt - число группы
                    numbutt += 1
                else:
                    if numbutt > 2: #Найдена группа из numbutt кнопок imgbutt(>=3)
                        #Код подсчёта групп/очков
                        total += 1 #Число групп. Факт нахождения групп
                        #Выделение группы
                        for l in range (0, (numbutt - 1)):
                            mass[x- numbutt + l][y] *= (-1) #Замена знака у готовых групп
                    imgbutt = mass[y][x] #Сброс группы на новую
                    numbutt = 1
                    if (X==10) and (numbutt > 2): #Концевая группа
                        #Код подсчёта групп/очков
                        total += 1
                        #Выделение группы
                        for l in range(1, numbutt):
                            mass[x - numbutt + l][y] *= (-1) #Замена знака у готовых групп


        #АНАЛИЗ ПО ВЕРТИКАЛИ
        for x range (1, 10):#ЦИКЛ x = 1 То 10: Поле 10х 10
            numbutt = 0 #Число фишек в текущей группе
            for y range (1, 10):#ЦИКЛ y = 1 То 10:
                if y==1:
                    imgbutt = mass[x][y] #ЕСЛИ y = 1 To imgbutt = | M(y, x) |
                if mass[x][y] == imgbutt:#imgbutt - число группы
                    numbutt += 1
                else:
                    if numbutt > 2: #Найдена группа из numbutt фишек imgbutt(>=3)
                        #Код подсчёта групп/очков
                        total += 1 #Число групп. Факт нахождения групп
                        #Выделение группы
                        for l in range (0, (numbutt - 1)):
                            mass[y- numbutt + l][x] *= (-1) #Замена знака у готовых групп
                    imgbutt = mass[x][y] #Сброс группы на новую
                    numbutt = 1
                    if (y==10) and (numbutt > 2): #Концевая группа
                        #Код подсчёта групп/очков
                        total += 1
                        #Выделение группы
                        for l in range(1, numbutt):
                            mass[y - numbutt + l][x] *= (-1) #Замена знака у готовых групп


    for i in range(0, 10):
        for j in range(0, 10):
            mass[i][j] = random.choice(img_list)
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
