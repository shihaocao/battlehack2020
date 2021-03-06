import random
# from battlehack2020.stubs import *
# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = -1
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

team = get_team()
board_size = get_board_size()

team = get_team()
opp_team = Team.WHITE if team == Team.BLACK else team.BLACK

robottype = get_type()
row, col = 0, 0

def overlord():
    global team, opp_team, robottype, forward, row, col, pawn_state

    if team == Team.WHITE:
        index = 0
    else:
        index = board_size - 1
    goal = board_size - 1 - index
    cont = True

    for c in range(board_size):
        ally = 0
        ene = 0
        for r in range(board_size):
            query = check_space(r, c)
            if query == team:
                ally += 1
            elif query == opp_team:
                ene += 1

        if ((ally == 0) and (ene > 0)):
            if not check_space(index, c):
                spawn(index, c)
                cont = False
                dlog('Reaction spawn at: (' + str(index) + ', ' + str(c) + ')')
                return

    dlog('Finish reaction strat')

    availcols = {i for i in range(board_size)}
    woncols = {i for i in range(board_size) if check_space(goal, i) == team}
    dlog("WON: "+str(woncols))
    rando = availcols - woncols
    dlog("RAND: "+str(rando))
    if cont:
        i = -1
        for _ in range(board_size):
            i = random.sample(rando, 1)[0]
            rando = rando - {i}
            if not check_space(index, i):
                spawn(index, i)
                dlog('Spawned unit at: (' + str(index) + ', ' + str(i) + ')')
                return

forward = 0
if team == Team.WHITE:
    forward = 1
else:
    forward = -1

pawn_state = "ADVANCE"
pawn_timer = 0
pawn_thresh = 200

def attempt_capture():
    global team, opp_team, robottype, forward, row, col, pawn_state

    # try catpuring pieces
    if check_space_wrapper(row + forward, col + 1, board_size) == opp_team: # up and right
        capture(row + forward, col + 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col + 1) + ')')
        return True

    elif check_space_wrapper(row + forward, col - 1, board_size) == opp_team: # up and left
        capture(row + forward, col - 1)
        dlog('Captured at: (' + str(row + forward) + ', ' + str(col - 1) + ')')
        return True
    
    return False

def attempt_forward():
    global team, opp_team, robottype, forward, row, col, pawn_state

    # otherwise try to move forward
    if row + forward != -1 and row + forward != board_size and not check_space_wrapper(row + forward, col, board_size):
        #               ^  not off the board    ^            and    ^ directly forward is empty
        move_forward()
        dlog('Moved forward!')
        return True
    
    return False

def check_halt():
    global team, opp_team, robottype, forward, row, col, pawn_state

    # halt if enemy knights move ahead
    if check_space_wrapper(row + forward*2, col + 1, board_size) == opp_team: # up and right
        # dlog("$ RECCOMEND HALTED")
        return True
    elif check_space_wrapper(row + forward*2, col - 1, board_size) == opp_team: # up and right
        # dlog("$ RECCOMEND HALTED")
        return True
    return False

def stage():
    global team, opp_team, robottype, forward, row, col, pawn_state

    dlog("STAGE")
    if attempt_capture():
        return
    elif attempt_forward():
        return
        
def advance():
    global team, opp_team, robottype, forward, row, col, pawn_state
    # dlog("ADVANCE")
    if attempt_capture():
        return
    elif check_halt():
        dlog("My state: "+pawn_state)
        pawn_state = "HALT"
        return
    else:
        attempt_forward()
        return

def flank_secured():
    global team, opp_team, robottype, forward, row, col, pawn_state
    if check_space_wrapper(row, col + 1, board_size) == team: # up and right
        return True
    elif check_space_wrapper(row, col - 1, board_size) == team:
        return True
    return False


def halt():
    global team, opp_team, robottype, forward, row, col, pawn_state, pawn_timer, pawn_thresh
    
    # dlog("HALT")
    if attempt_capture():
        return
    if check_halt():
        if flank_secured() and pawn_timer > pawn_thresh:
            pawn_state = "ADVANCE"
            attempt_forward()
        else:
            return
    else:
        pawn_state = "ADVANCE"
        attempt_forward()
        return

def pawn():
    global team, opp_team, robottype, forward, row, col, pawn_state, pawn_timer, pawn_thresh
    row, col = get_location()
    # dlog('My location is: ' + str(row) + ' ' + str(col))

    pawn_timer += 1

    pawn_switcher = {
        "STAGE": stage,
        "ADVANCE": advance,
        "HALT": halt
    }

    func = pawn_switcher.get(pawn_state)
    func()

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global team, opp_team, robottype, forward, row, col, pawn_state

    if robottype == RobotType.PAWN:
        pawn()

    # OVERLORD
    else:
        overlord()

    bytecode = get_bytecode()
    # dlog('Done! Bytecode left: ' + str(bytecode))

