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

    class MatchTemplate:
        def __init__(self, *mask):
            self.mask = mask
            self.width = 0
            self.height = 0
            for m in mask:
                if m[0]+1 > self.width:
                    self.width = m[0]+1
                if m[1]+1 > self.height:
                    self.height = m[1]+1

    default_templates = (
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

    class Grid:
        def __init__(self, types, xysize, templates = default_templates):
            self.xysize = xysize
            self.types = types
            self.templates = templates
            self.points = 0
            self.reward = 0
            self.chain = 0
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

            self.chain += 1
            boom_amt -= 2
            self.reward += (boom_amt * 10) * self.chain

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
            ## ???????????????????? ?????? ??????????
            for x in range(self.xysize[0]):
                for y in range(self.xysize[1]):

                    ## ?????? ???????????? ???????? ?????????????????? - ???????????????????? ?????? ??????????????
                    for t in self.templates:

                        ## ???????? ???????????? ???? ?????????????? ???? ?????????? ?????????? - ?? ???????? ??????
                        if x + t.width > self.xysize[0]:
                            continue
                        if y + t.height > self.xysize[1]:
                            continue

                        ## ???????? ???? ?????????????? ???????????????????? ???????? ?? ?????? ???? ?????? ???????????????? - ?????????????????????? ????????????????????
                        ## ???????? ???????? ?? ???????? ?????????????? ???? ?????????????????? - ?????????????? ????????????
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

                        ## ?????? ???????????? ???????????????????? ???????????? ??????????, ?????????? ???????? ???? ?????? ????????????????
                        if not breaked:
                            amt += 1
            return amt > 0

        def PointsUpdate(self):
            self.points += self.reward
            self.reward = 0
            self.chain = 0
