label main_menu:
    $ _config.quit_confirm = False
    return
init python:
    E_NULL = None
    E_APPLE = 0
    E_BANANA = 1
    E_CARROT = 2
    E_CHERRY = 3
    E_CORN = 4
    E_LEMON = 5
    E_MELON = 6
    E_ORANGE = 7
    mes='Points: 0'#Сообщение с количеством поинтов
    fall_time_per_cell = .25

    img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]

    class Element:
        def __init__(self, type):
            self.type = type
            self.go_boom = False
            self.fall_amt = 0

    class Grid:
        def __init__(self, types, xysize):
            self.xysize = xysize#Размер сетки
            self.types = types#Типы объектов
            self.points = 0#Очки
            self.grid = [ [Element(E_NULL) for i in range(xysize[1])] for j in range(xysize[0]) ]#Заполнение сетки пустыми полями

        def CheckBoom(self, xy, target_type = None, mark = False):

            x, y = xy
            boom = False
            left, top = xy
            right, bottom = xy

            if target_type is None:
                target_type = self.grid[x][y].type#Передаёт в target_type тип объекта расположенного по х и у

            if target_type == E_NULL:
                return 0#Если тип обекта E_NULL вернуть 0

            ###
            # LEFT
            offset = 1
            while True:
                if x - offset < 0:
                    break

                if self.grid[x - offset][y].type == target_type:
                    offset += 1
                    left -= 1
                else:
                    break

            ###
            # RIGHT
            offset = 1
            while True:
                if x + offset >= self.xysize[0]:
                    break

                if self.grid[x + offset][y].type == target_type:
                    offset += 1
                    right += 1
                else:
                    break

            ###
            # TOP
            offset = 1
            while True:
                if y - offset < 0:
                    break

                if self.grid[x][y - offset].type == target_type:
                    offset += 1
                    top -= 1
                else:
                    break

            ###
            # BOTTOM
            offset = 1
            while True:
                if y + offset >= self.xysize[1]:
                    break

                if self.grid[x][y + offset].type == target_type:
                    offset += 1
                    bottom += 1
                else:
                    break

            dhor = right - left
            if dhor > 1:
                boom = True
                if mark:
                    for i in range(dhor + 1):
                        self.grid[left + i][y].go_boom = True

            dver = bottom - top
            if dver > 1:
                boom = True
                if mark:
                    for i in range(dver + 1):
                        self.grid[x][top + i].go_boom = True

            return boom


        def Fill(self):
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    if self.grid[x][y].type == E_NULL:
                        self.FillElement((x, y))

        def FillElement(self, xy):
            x, y = xy
            valid_types = []
            for t in self.types:
                if not self.CheckBoom((x, y), t):
                    valid_types.append(t)

            self.grid[x][y].type = renpy.random.choice(valid_types)

        def DoBoom(self):
            boom_amt = 0
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    element = self.grid[x][y]
                    if element.go_boom:
                        boom_amt += 1
                        element.type = E_NULL
                        element.go_boom = False

            boom_amt -= 2
            self.points += boom_amt**2 * 10

        def ResetBoom(self):
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    self.grid[x][y].go_boom = False

        def Fall(self):
            for x in range(self.xysize[0]):
                k = self.xysize[1] - 1
                mass = self.grid[x][::-1]
                while True:
                    if mass[k].type == E_NULL:
                        for i in range(k + 1, self.xysize[1]):
                            mass[i - 1], mass[i] = mass[i], mass[i - 1]
                            if mass[i - 1].type != E_NULL:
                                mass[i - 1].fall_amt += 1

                    k -= 1
                    if k<0:
                        break

                self.grid[x] = mass[::-1]

                last_amt = self.xysize[1]
                for _y in range(self.xysize[1]):
                    y = self.xysize[1] - _y - 1
                    if self.grid[x][y].type != E_NULL:
                        last_amt = self.grid[x][y].fall_amt

                    else:
                        self.FillElement((x, y))
                        if last_amt > 0:
                            self.grid[x][y].fall_amt = last_amt
                        else:
                            self.grid[x][y].fall_amt = 1

        def ResetFall(self):
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    self.grid[x][y].fall_amt = 0

        def CheckSwap(self, xy1, xy2):
            x1, y1 = xy1
            x2, y2 = xy2

            ## swap elements
            temp = self.grid[x1][y1]
            self.grid[x1][y1] = self.grid[x2][y2]
            self.grid[x2][y2] = temp

            ## check how grid will behave
            check1 = self.CheckBoom(xy1)
            check2 = self.CheckBoom(xy2)

            ## swap elements back
            temp = self.grid[x1][y1]
            self.grid[x1][y1] = self.grid[x2][y2]
            self.grid[x2][y2] = temp

            return (check1 or check2)

        def SwapAndMark(self, xy1, xy2):
            x1, y1 = xy1
            x2, y2 = xy2

            ## swap elements
            temp = self.grid[x1][y1]
            self.grid[x1][y1] = self.grid[x2][y2]
            self.grid[x2][y2] = temp

            ## check how grid will behave
            self.CheckBoom(xy1, mark = True)
            self.CheckBoom(xy2, mark = True)

        def SearchAndMark(self):
            result = False
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    if self.CheckBoom((x, y), mark = True):
                        result = True
            return result

    #img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]

default cell_selected = None
screen m3_select_first(map):
    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            if element.type != E_NULL:
                frame:
                    background None
                    align (.5,.5)
                    xoffset 72*(x - map.xysize[0]//2)
                    yoffset 72*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        action SetVariable('cell_selected', (x, y)), Return("selected")

screen m3_select_second(map):
    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            $ is_nb = cell_selected in ((x-1, y),(x+1, y),(x, y-1),(x, y+1))
            $ valid = is_nb and map.CheckSwap(cell_selected, (x, y))
            if element.type != E_NULL:
                frame:
                    if cell_selected != (x, y) and not valid:
                        background None

                    align (.5,.5)
                    xoffset 72*(x - map.xysize[0]//2)
                    yoffset 72*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]

                        if cell_selected == (x, y):
                            action SetVariable('cell_selected', None), Return("deselected")

                        elif valid:
                            action Return((x, y))


screen m3_boom(map):
    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            if element.type != E_NULL:
                frame:
                    background None
                    align (.5,.5)
                    xoffset 72*(x - map.xysize[0]//2)
                    yoffset 72*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        if element.go_boom:
                            at transform:
                                linear .25 zoom .8
                                linear .15 zoom 1.25 alpha 0
    timer .5 action Return()


screen m3_fall(map):
    $ max_amt = -1
    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            $ amt = element.fall_amt
            if max_amt < amt:
                $ max_amt = amt
            if element.type != E_NULL:
                frame:
                    background None
                    align (.5,.5)
                    xoffset 72*(x - map.xysize[0]//2)
                    yoffset 72*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        if element.fall_amt > 0:
                            at transform:
                                yoffset -72*amt
                                linear fall_time_per_cell*amt yoffset 0
    timer fall_time_per_cell*max_amt action Return()


image grey = Solid("#a0aaaf")
label start:
    $ map = Grid(
        types = (E_APPLE, E_BANANA, E_CARROT, E_CHERRY, E_CORN, E_LEMON, E_MELON, E_ORANGE),#Отвечает за типы элементов в сетке
        xysize = (13, 13)#Количество столбиков и рядов
    )
    $ map.Fill()#Заполнение сетки

    show grey#Добавление фона

    label .loop:

        $ map.ResetBoom()
        call screen m3_select_first(map=map)
        if _return == "selected":

            call screen m3_select_second(map=map)
            if _return == "deselected":
                jump .loop

            $ map.SwapAndMark(cell_selected, _return)
            $ go_boom = True
            while go_boom:
                call screen m3_boom(map=map)
                $ map.DoBoom()
                $ map.Fall()
                call screen m3_fall(map=map)
                $ map.ResetFall()
                $ go_boom = map.SearchAndMark()


    jump .loop
