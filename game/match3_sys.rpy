init python:
    E_NULL = None
    E_chip_blue = 0
    E_chip_green = 1
    E_chip_orange = 2
    E_chip_purple = 3
    E_chip_red = 4
    E_chip_yellow = 5
    E_chip_bomb = 6
    #E_MELON = 6
    #E_ORANGE = 7
    iter_time = 120#Shutdown timer
    bomb_boom = False
    if persistent.FAQ is None:
        persistent.FAQ = False
    img_list = ["chip_blue_%s", "chip_green_%s", "chip_orange_%s", "chip_purple_%s", "chip_red_%s", "chip_yellow_%s", "chip_bomb_%s"]#List of images for buttons
    bomb = {"x" : [None, None], "y" : [None, None], "type" : None}
    class MatchTemplate:#Class of masks for the grid
        def __init__(self, *mask):
            self.mask = mask
            self.width = 0
            self.height = 0
            for m in mask:
                if m[0]+1 > self.width:
                    self.width = m[0]+1
                if m[1]+1 > self.height:
                    self.height = m[1]+1

    default_templates = (#Массив со всеми вариантами возможных складований
    # X X _ X | X _ X X | X _ _ | _ X X | _ _ X | X X _ |
    #         |         | _ X X | X _ _ | X X _ | _ _ X |
    MatchTemplate((0, 0), (1, 0), (3, 0)),
    MatchTemplate((0, 0), (2, 0), (3, 0)),
    MatchTemplate((0, 0), (1, 1), (2, 1)),
    MatchTemplate((0, 1), (1, 0), (2, 0)),
    MatchTemplate((0, 0), (1, 1), (2, 1)),
    MatchTemplate((0, 1), (1, 1), (2, 0)),
    MatchTemplate((0, 0), (1, 0), (2, 1)),

    # X | X | _ X | X _ | X _ | _ X |
    # X | _ | X _ | _ X | X _ | _ X |
    # _ | X | X _ | _ X | _ X | X _ |
    # X | X |     |     |     |     |
    MatchTemplate((0, 0), (0, 1), (0, 3)),
    MatchTemplate((0, 0), (0, 2), (0, 3)),
    MatchTemplate((1, 0), (0, 1), (0, 2)),
    MatchTemplate((0, 0), (1, 1), (1, 2)),
    MatchTemplate((0, 0), (0, 1), (1, 2)),
    MatchTemplate((1, 0), (1, 1), (0, 2)),

    # X _ X | _ X _ | _ X | X _ |
    # _ X _ | X _ X | X _ | _ X |
    #       |       | _ X | X _ |
    MatchTemplate((0, 0), (1, 1), (2, 0)),
    MatchTemplate((0, 1), (1, 0), (2, 1)),
    MatchTemplate((1, 0), (0, 1), (1, 2)),
    MatchTemplate((0, 0), (1, 1), (0, 2)),
    )

    class Element:
        def __init__(self, type):
            self.type = type
            self.go_boom = False
            self.fall_amt = 0

    class Grid:#Grid class of elements (nuts)
        def __init__(self, types, xysize, templates = default_templates):
            self.xysize = xysize
            self.types = types
            self.templates = templates
            self.points = 0
            self.reward = 0
            self.chain = 0
            self.grid = [ [Element(E_NULL) for i in range(xysize[1])] for j in range(xysize[0]) ]

        def CheckBoom(self, xy, target_type = None, mark = False):
            #We check whether it is possible to blow up

            x, y = xy
            boom = False
            left, top = xy
            right, bottom = xy

            if target_type is None:
                target_type = self.grid[x][y].type
                
                #if target_type == 6:
                    #return True

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
            #Filling in empty elements
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    if self.grid[x][y].type == E_NULL:
                        self.FillElement((x, y))

        def FillElement(self, xy):
            #Creating elements
            boom = 0
            x, y = xy
            valid_types = []
            for t in self.types:
                if not self.CheckBoom((x, y), t):
                    valid_types.append(t)
            boom = renpy.random.randint(0, 50)#The random number by which the bomb or the usual nut will be determined. If 1 drops out, a bomb. The larger the range, the rarer the bombs
            if boom == 1:
                
                for i in range(self.xysize[0]):
                    for j in range(self.xysize[1]):
                        if self.grid[i][j].type == E_chip_bomb:
                            self.grid[x][y].type = renpy.random.choice(valid_types)
                            break
                if self.grid[x][y].type == E_NULL:
                    self.grid[x][y].type = E_chip_bomb
            else:
                self.grid[x][y].type = renpy.random.choice(valid_types)
            

        def DoBoom(self):
            #Checking if it is still possible to blow up something
            boom_amt = 0
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):
                    element = self.grid[x][y]
                    if element.go_boom:
                        boom_amt += 1
                        element.type = E_NULL
                        element.go_boom = False

            self.chain += 1
            boom_amt -= 2
            self.reward += (boom_amt * 10) * self.chain

        def ResetBoom(self):
            #We reset the possibility of an explosion everywhere
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
                last_y = None
                for _y in range(self.xysize[1]):
                    y = self.xysize[1] - _y - 1
                    if self.grid[x][y].type != E_NULL:
                        last_amt = self.grid[x][y].fall_amt
                        last_y = y

                    else:
                        self.FillElement((x, y))
                        if last_amt > 0:
                            self.grid[x][y].fall_amt = last_amt
                        else:
                            self.grid[x][y].fall_amt = last_y

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
            
            if self.grid[x1][y1].type == 6:#We return the opportunity to drop a bomb
                bomb["type"] = self.grid[x2][y2].type
                return True
            if self.grid[x2][y2].type == 6:#We return the opportunity to drop a bomb
                bomb["type"] = self.grid[x1][y1].type
                return True
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

        def CheckAvailableTurns(self):
            amt = 0
            ## iterating through the entire grid
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):

                    ## for each pair of coordinates, we iterate through all the templates
                    for t in self.templates:

                        ## if the template does not fit to the end of the grid - into the stump of it
                        if x + t.width > self.xysize[0]:
                            continue
                        if y + t.height > self.xysize[1]:
                            continue

                        ## if the same type of element is located according to the template, we count the match
                        ## if at least one element does not match, drop the template
                        e = None
                        breaked = False
                        for xmod, ymod in t.mask:
                            e_type = self.grid[x + xmod][y + ymod].type
                            if e is None:
                                e = e_type
                            if e == e_type:
                                continue

                            breaked = True
                            break

                        ## this section is called only when the loop has not been broken
                        if not breaked:
                            amt += 1
            return amt > 0

        def PointsUpdate(self):#Updating glasses
            self.points += self.reward
            self.reward = 0
            self.chain = 0
        def bombs(self):#Bomb function
            global bomb, bomb_boom
            boom_amt = 0
            xx = bomb["x"]
            yy = bomb["y"]
            type = bomb["type"]
            if bomb["type"] != None and bomb["type"] != E_NULL:
                self.grid[xx[0]][yy[0]].go_boom = True
                self.grid[xx[1]][yy[1]].go_boom = True
                for x in range(self.xysize[0]):
                    for y in range(self.xysize[1]):
                        if self.grid[x][y].type == type:
                            #self.grid[x][y].type = E_NULL
                            self.grid[x][y].go_boom = True
                            boom_amt += 1
                self.chain += 1
                self.reward += (boom_amt * 2) * self.chain
                bomb_boom = True
                bomb["type"] = None
                bomb["x"] = [None, None]
                bomb["y"] = [None, None]

                        

                        
#