label main_menu:
    $ _config.quit_confirm = False
    return

image grey = Solid("#a0aaaf")
label start:
    $ map = Grid(
        types = (E_APPLE, E_BANANA, E_CARROT, E_CHERRY),#, E_CORN, E_LEMON, E_MELON, E_ORANGE),
        xysize = (10, 10)
    )
    $ map.Fill()

    show grey

    label .loop:
        if not map.CheckAvailableTurns():
            jump no_turns
        $ map.ResetBoom()
        call screen m3_select_first(map=map)
        if _return == "selected":

            call screen m3_select_second(map=map)
            if _return == "deselected":
                jump .loop

            $ cell_swaped = _return
            call screen m3_swap(map=map, xy1=cell_selected, xy2=cell_swaped)

            $ map.SwapAndMark(cell_selected, cell_swaped)
            $ go_boom = True
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
