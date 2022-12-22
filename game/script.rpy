label main_menu:
    $ _config.quit_confirm = False
    return
image grey = Solid("#a0aaaf")
label start:
    
    $ map = Grid(
        types = (E_chip_blue, E_chip_green, E_chip_orange, E_chip_purple, E_chip_red, E_chip_yellow),#, E_CORN, E_LEMON, E_MELON, E_ORANGE),
        xysize = (8, 8)
    )
    $ map.Fill()

    show grey
    if persistent.FAQ == False:
        "[persistent.FAQ]"
        "How to play:"

        "To swap 2 nuts in places, click first on 1, and then on another nut"
        "When you select the first nut, all the nuts with which it can be changed will be highlighted."
        "To cancel the selection click on the nut again"
    $ persistent.FAQ = True
    label .loop:
        show screen timer_test
        if not map.CheckAvailableTurns():
            jump no_turns
        $ map.ResetBoom()
        call screen m3_select_first(map=map)
        $ bomb["x"][0] = cell_selected[0]
        $ bomb["y"][0] = cell_selected[1]
        if _return == "selected":

            call screen m3_select_second(map=map)
            if _return == "deselected":
                jump .loop

            
            $ cell_swaped = _return
            $ bomb["x"][1] = cell_swaped[0]
            $ bomb["y"][1] = cell_swaped[1]
            if bomb["x"] != [None, None]:
                if map.grid[bomb["x"][0]][bomb["y"][0]].type != E_chip_bomb and map.grid[bomb["x"][1]][bomb["y"][1]].type != E_chip_bomb:
                    $ bomb["type"] = None
                    $ bomb["x"] = [None, None]
                    $ bomb["y"] = [None, None]
            call screen m3_swap(map=map, xy1=cell_selected, xy2=cell_swaped)

            $ map.SwapAndMark(cell_selected, cell_swaped)
            $ go_boom = True
            $ map.bombs()
            while go_boom:
                
                call screen m3_boom(map=map)
                
                $ map.DoBoom()
                $ map.Fall()
                call screen m3_fall(map=map)
                $ map.ResetFall()
                $ go_boom = map.SearchAndMark()

            call screen m3_points(map)
            
            $ map.PointsUpdate()
    
    
    jump .loop
label no_turns:
    "There is no more available turns"
label end:
    return
label test:
    hide screen timer_test
    "end"
    return


screen timer_test:
    zorder 100
    default timer_var =  iter_time
    default minutes = 0
    default seconds = 0
    timer timer_var action Hide("m3_reward"), Hide("m3_ui"), Hide("m3_swap"), Hide("m3_points"), Hide("m3_fall"), Jump("test")
    if iter_time > 0:
        timer 1 repeat True action SetVariable("iter_time", iter_time-1)
    $ minutes = iter_time//60
    $ seconds = iter_time % 60
    hbox:
        xalign .5 
        yalign .87
        #text "[minutes] min [seconds] sec" size 64
        text "{:02}:{:02}".format(minutes, seconds) size 64
    #text "[iter_time] seconds" xalign .5 yalign .87 size 64