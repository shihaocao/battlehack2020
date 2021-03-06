import random


# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 0
def dlog(str):
    if DEBUG > 0:
        log(str)


def check_space_wrapper(r, c, board_size):
    # check space, except doesn't hit you with game errors
    if r < 0 or c < 0 or c >= board_size or r >= board_size:
        return False
    try:
        return check_space(r, c)
    except:
        return None
a = 1
def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global a
    a += 1
    dlog('Starting Turn!')
    dlog('A: '+str(a))
    board_size = get_board_size()

    team = get_team()
    opp_team = Team.WHITE if team == Team.BLACK else team.BLACK
    dlog('Team: ' + str(team))

    robottype = get_type()
    dlog('Type: ' + str(robottype))

    if robottype == RobotType.PAWN:
        row, col = get_location()
        dlog('My location is: ' + str(row) + ' ' + str(col))

        if team == Team.WHITE:
            forward = 1
        else:
            forward = -1

        # try catpuring pieces
        if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
            capture(row + forward, col + 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')

        elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
            capture(row + forward, col - 1)
            dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')

        # halt if enemy knights move ahead
        elif check_space_wrapper(row + forward*2, col + 1, board_size) == opp_team: # up and right
            dlog("$ HALT")
        elif check_space_wrapper(row + forward*2, col - 1, board_size) == opp_team: # up and right
            dlog("$ HALT")



        # otherwise try to move forward
        elif row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size):
            #               ^  not off the board    ^            and    ^ directly forward is empty
            move_forward()
            dlog('Moved forward!')

        confusion = "you need a line here to avoid segfault. we aren't sure why but are working on it"
        # ^ I think this is related to the potential ambiguity of what the following else is referring to?

    # OVERLORD
    else:
        if team == Team.WHITE:
            index = 0
        else:
            index = board_size - 1

        cont = True

        for c in range(board_size):
            # dlog("Checking Col: "+str(c))
            ally = 0
            ene = 0
            for r in range(board_size):
                query = check_space(r, c)
                if query == team:
                    ally += 1
                elif query == opp_team:
                    ene += 1

            # dlog("R: "+str(r)+" C: "+str(c))

            if ((ally == 0) and (ene > 0)):
                # dlog("Re")
                if not check_space(index, c):
                    # dlog('Attempt spawn at: (' + str(index) + ', ' + str(c) + ')')
                    spawn(index, c)
                    cont = False
                    dlog('Reaction spawn at: (' + str(index) + ', ' + str(c) + ')')
                # else:
                #     dlog('No spawn')

        dlog('Finish reaction strat')

        if cont:
            for _ in range(board_size):
                i = random.randint(0, board_size - 1)
                if not check_space(index, i):
                    spawn(index, i)
                    dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                    break

    bytecode = get_bytecode()
    dlog('Done! Bytecode left: ' + str(bytecode))

