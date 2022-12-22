init python:

    at_spd_swap = .25
    at_spd_fall = .15
    at_spd_boom_startup = .15
    at_spd_boom_followup = .35
    at_spd_boom_bomb = 0.05

    cell_width = 72
    cell_height = 72
    cell_spacing = 0

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
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
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
                    else:
                        background "bg_frame" #alpha .5

                    align (.5,.5)
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        
                        if cell_selected == (x, y):
                            action SetVariable('cell_selected', None), Return("deselected")

                            #bombs
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
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        if element.go_boom:
                            if bomb_boom:
                                #Transformation for explosions + animation on top of the nuts themselves
                                foreground "test_boom"
                                at transform:
                                    linear at_spd_boom_startup zoom 1.25
                                    linear at_spd_boom_followup+at_spd_boom_bomb zoom 1.4 alpha 0
                            else:
                                #the usual transformation
                                at transform:
                                    linear at_spd_boom_startup zoom .8
                                    linear at_spd_boom_followup zoom 1.25 alpha 0
    if bomb_boom:
        timer at_spd_boom_startup+at_spd_boom_followup+at_spd_boom_bomb action SetVariable("bomb_boom", False), Return()
    else:
        timer at_spd_boom_startup+at_spd_boom_followup action Return()
    use m3_ui(map)
    
    use m3_reward(map.reward)
    
    


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
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        if element.fall_amt > 0:
                            at transform:
                                yoffset -cell_height*amt
                                linear at_spd_fall*amt yoffset 0
    timer at_spd_fall*max_amt action Return()

    use m3_ui(map)
    use m3_reward(map.reward)
    


screen m3_swap(map, xy1, xy2):
    
    $ dxy1 = (xy2[0] - xy1[0], xy2[1] - xy1[1])
    $ dxy2 = (xy1[0] - xy2[0], xy1[1] - xy2[1])
    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            if element.type != E_NULL:
                frame:
                    background None
                    align (.5,.5)
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]
                        if xy1 == (x, y):
                            at transform:
                                linear at_spd_swap xoffset cell_width*dxy1[0] yoffset cell_height*dxy1[1]
                        if xy2 == (x, y):
                            at transform:
                                linear at_spd_swap xoffset cell_width*dxy2[0] yoffset cell_height*dxy2[1]
    timer at_spd_swap action Return()

    use m3_ui(map)
    
    
    
    
    


screen m3_ui(map):

    ## Points
    text str(map.points):
        size 90
        xalign .5
        ypos 30

    vbox:
        align .1, .3
        text "TURNS: {}".format(map.CheckAvailableTurns())

    ## Reset
    textbutton "RESET":
        align .1, .5
        text_idle_color "#222"
        text_hover_color "#d62"
        action Jump("end")
    
    
    
    
screen m3_reward(amt):

    if amt > 0:
        label "+" + str(amt):
            text_outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
            text_size 60
            xalign .5
            ypos 100
    
    
    

screen m3_points(map):

    for x in range (map.xysize[0]):
        for _y in range (map.xysize[1]):
            $ y = map.xysize[1] - _y - 1
            $ element = map.grid[x][y]
            if element.type != E_NULL:
                frame:
                    background None
                    align (.5,.5)
                    xoffset cell_width*(x - map.xysize[0]//2)
                    yoffset cell_height*(y - map.xysize[1]//2)
                    imagebutton:
                        auto img_list[element.type]

    use m3_ui(map)

    label "+" + str(map.reward):
        text_outlines [ (absolute(1), "#000", absolute(0), absolute(0)) ]
        text_size 60
        xalign .5
        ypos 100
        at transform:
            linear .15 zoom 1.2
            linear .35 zoom .5 alpha 0 ypos 65

    timer .5 action Return()
