init python:
    fall_time_per_cell = .25

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

    use m3_ui(map)

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

    use m3_ui(map)


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

    use m3_ui(map)


screen m3_fall(map):
    on "show" action Show("m3_reward", amt=map.reward)
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

    use m3_ui(map)


screen m3_ui(map):

    ## Points
    vbox:
        align .1, .3
        text "POINTS: {}".format(map.points)
        text "TURNS: {}".format(map.CheckAvailableTurns())

    ## Reset
    textbutton "RESET":
        align .1, .5
        action Jump("end")

screen m3_reward(amt):

    label str(amt):
        text_outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
        align .5, .25
        at transform:
            alpha 0
            linear .25 alpha 1 zoom 1.5 yoffset 10
            linear .5 yoffset 30
            linear .5 alpha 0 yoffset 40

    timer 1.25 action Hide("m3_reward")
