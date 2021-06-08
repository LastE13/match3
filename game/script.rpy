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

    img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]

    class Element:
        def __init__(self, type):
            self.type = type
            self.go_boom = False
            self.fall_amt = 0

    class Grid:
        def __init__(self, types, xysize):
            self.xysize = xysize
            self.types = types
            self.points = 0
            self.grid = [ [Element(E_NULL) for i in range(xysize[1])] for j in range(xysize[0]) ]

        def CheckBoom(self, xy, target_type = None, mark = False):

            x, y = xy
            boom = False
            left, top = xy
            right, bottom = xy

            if target_type is None:
                target_type = self.grid[x][y].type

            if target_type == E_NULL:
                return 0

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

        def CalcFall(self):
            ## TODO: посчитать насколько каждый элемент должен упасть, и записать это ему в поле fall_amt. Нужно для анимации. Отдельно будет DoFall
            for x in range(self.xysize[0]):
                fall_amt = 0
                for _y in range(self.xysize[1]):
                    y = _y - i
                    element = self.grid[x][y]
                    if element.type == E_NULL:
                        fall_amt += 1
                    else:
                        element.fall_amt = fall_amt

        def DoFall(self):
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    element = self.grid[x][y]
                    if element.fall_amt > 0:
                        self.grid[x][y + element.fall_amt].type = element.type
                        element.fall_amt = 0

        def CheckSwap(self, xy1, xy2):
            x1, y1 = xy1
            x2, y2 = xy2
            check1 = self.CheckBoom(xy1, self.grid[x2][y2].type)
            check2 = self.CheckBoom(xy2, self.grid[x1][y1].type)
            return (check1 or check2)


    #img_list = ["apple_%s", "banana_%s", "carrot_%s", "cherry_%s", "corn_%s", "lemon_%s", "melon_%s", "orange_%s"]

default cell_selected = None
screen m3_select_first(map):
    for x in range (map.xysize[0]):
        for y in range (map.xysize[1]):
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
        for y in range (map.xysize[1]):
            $ element = map.grid[x][y]
            if element.type != E_NULL:
                frame:

                    if cell_selected != (x, y):
                        background None

                    align (.5,.5)
                    xoffset 72*(x - map.xysize[0]//2)
                    yoffset 72*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]

                        if cell_selected == (x, y):
                            action SetVariable('cell_selected', None), Return("deselected")

                        elif cell_selected in ((x-1, y),(x+1, y),(x, y-1),(x, y+1)) and map.CheckSwap(cell_selected, (x, y)):
                            action Return((x, y))


image grey = Solid("#a0aaaf")
label start:
    $ map = Grid(
        types = (E_APPLE, E_BANANA, E_CARROT, E_CHERRY, E_CORN, E_LEMON, E_MELON, E_ORANGE),
        xysize = (10, 5)
    )
    $ map.Fill()

    show grey

    label .loop:

        call screen m3_select_first(map=map)
        if _return == "selected":

            call screen m3_select_second(map=map)
            if _return == "deselected":
                jump .loop


    return
