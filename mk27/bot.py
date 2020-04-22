import random
# from battlehack2020.stubs import *
# This is an example bot written by the developers!
# Use this to help write your own code, or run it against your bot to see how well you can do!

DEBUG = 1
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
index = 0

forward = 0
if team == Team.WHITE:
    forward = 1
else:
    forward = -1
goal = 0
if team == Team.WHITE:
    goal = board_size - 1
else:
    goal = 0

if team == Team.WHITE:
    index = 0
else:
    index = board_size - 1

def min_list(l):
    minn = 99999
    for x in l:
        if x < minn:
            minn = x

    return minn

def overlord():
    global team, opp_team, robottype, forward, row, col, pawn_state, index, goal

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

    ourplayers = [0 for x in range(board_size)]
    theirs = [0 for x in range(board_size)]
    deepest = [0 for x in range(board_size)]

    for c in range(board_size):
        ally = 0
        ene = 0
        for r in range(board_size):
            query = check_space(r, c)
            if query == team:
                ally += 1
            elif query == opp_team:
                ene += 1

        ourplayers[c] = ally
        theirs[c] = ene

    for c in range(board_size):
        deep = 0
        if team == Team.BLACK:
            for r in range(board_size-1,-1,-1):
                query = check_space_wrapper(r, c, board_size)
                a = check_space_wrapper(r, c - 1, board_size)
                b = check_space_wrapper(r, c + 1, board_size)
                if query == opp_team or a == opp_team or b == opp_team:
                    deep = r - goal
                    break

        else:
            for r in range(board_size):
                query = check_space_wrapper(r, c, board_size)
                a = check_space_wrapper(r, c - 1, board_size)
                b = check_space_wrapper(r, c + 1, board_size)
                if query == opp_team or a == opp_team or b == opp_team:
                    deep = goal - r
                    break
        deepest[c] = deep

    col_score = [100 for x in range(board_size)]
    heuristic = {}
    # dlog(str(min_list(ourplayers)))

    # dlog()
    half = board_size / 2
    mult = 2
    pref = []
    if(timer) < 50:
        pref = [-mult if (c < half + 1) else mult for c in range(board_size)]
    else:
        # dlog("OTHER WAY")
        pref = [- mult if (c > half - 1) else mult for c in range(board_size)]

    heuristic = {c:0 for c in range(board_size)}
    for c in range(board_size):
        # if ourplayers[c] > 4:
        if False:
            heuristic[c] = 100
        elif ourplayers[c] < 2:
            heuristic[c] = -100 + 2*ourplayers[c]
        else:
            heuristic[c] = ourplayers[c] - theirs[c] + pref[c] - deepest[c]*2
    # if min_list(ourplayers) < 5:
    #     heuristic = {c:(ourplayers[c] - theirs[c]) for c in range(board_size)}
    # else:
    #     heuristic = {c:(col_score[c] + ourplayers[c]*ourplayers[c] - deepest[c]) for c in range(board_size)}

    h_list = [c for c in range(board_size)]

    # dlog(str(ourplayers.sort()))
    # if min_list(ourplayers) < 5:
    #     others = sort(ourplayers)
    #     for c in others:
    #         if not check_space(index, c):                
    #             spawn(index, c)
    #             dlog('LOW unit at: (' + str(index) + ', ' + str(c) + ')')
    #             return
    
    h_list.sort(key = heuristic.get)
    dlog(str(h_list))
    for c in h_list:
        if not check_space(index, c):
            spawn(index, c)
            dlog('Heuristic unit at: (' + str(index) + ', ' + str(c) + ')')
            return

    dlog('Finish reaction strat')

    availcols = {i for i    in range(board_size)}
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

def too_close():
    global team, goal, row

    if abs(row - goal) < 5:
        return True
    else:
        return False

pawn_state = "ADVANCE"
timer = 0
pawn_thresh = 30

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
        # dlog('Moved forward!')
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

def good_enough():
    global team, opp_team, robottype, forward, row, col, pawn_state
    global local_timer, goal

    if abs(row - goal) <= 7:
        return True
    else:
        return False
def advance():
    global team, opp_team, robottype, forward, row, col, pawn_state
    # dlog("ADVANCE")
    if attempt_capture():
        return
    # elif good_enough():
    #     return
    elif flank_secured() <= 0:
        # dlog("My state: "+pawn_state)
        # pawn_state = "HALT"
        return
    else:
        attempt_forward()
        return
local_timer = 0
attack_timer = 0
attack_thresh = 25
def flank_secured():
    global team, opp_team, robottype, forward, row, col, pawn_state
    global local_timer, index, attack_timer, attack_thresh, goal
    
    balls = 0
    flank = 0
    ene = 0
    sho = 0
    if check_space_wrapper(row, col + 1, board_size) == team:
        balls += 1
        flank += 1
        sho += 1
    if check_space_wrapper(row, col - 1, board_size) == team:
        balls += 1
        flank += 1
        sho += 1
    if check_space_wrapper(row - forward, col + 1, board_size) == team:
        balls += 1
        flank += 1
    if check_space_wrapper(row - forward, col - 1, board_size) == team:
        balls += 1
        flank += 1
    if check_space_wrapper(row - forward*2, col - 1, board_size) == team:
        balls += 1
        flank += 1
    if check_space_wrapper(row - forward*2, col + 1, board_size) == team:
        balls += 1
        flank += 1
    if check_space_wrapper(row - forward, col, board_size) == team:
        balls += 1

    if check_space_wrapper(row + forward*2, col - 1, board_size) == opp_team:
        balls -= 1
        ene += 1
    if check_space_wrapper(row + forward*2, col + 1, board_size) == opp_team:
        balls -= 1
        ene += 1
    far_front = False
    if check_space_wrapper(row + forward*2, col, board_size) == team:
        far_front = True
    # for c in range(-1,2):
    #     if check_space_wrapper(row + forward, col + c, board_size) == opp_team:
    #         ene += 1
    # for c in range(-1,2)
    #     if check_space_wrapper(row + forward * 2, col + c, board_size) == opp_team:
    #         ene += 1


    # elif ene == 1 and col != 0 and col != board_size and flank > 4 and sho > 1:
    #     return 3
    tt = 0

    # attack_thresh = 25 - abs(row - goal)
    attack_thresh = 15 + abs(row - goal)
    if abs(row - index) < 3:
        tt = 1
    else:
        tt = 5
    # if far_front:
    #     return 3
    if ene == 0:
        return 3
    if ene == 1 and col != 0 and col != board_size-1 and flank > 4 and sho > 1:
        attack_timer += 1
        if attack_timer > attack_thresh:
            return 3
    if ene == 1 and (col == 0 or col == board_size-1) and flank > 2 and sho > 0:
        # dlog("REEEEEEEEEEE")
        attack_timer += 1
        if attack_timer > attack_thresh:
            return 3
    # dlog(str(attack_timer))
    if flank > tt:
        attack_timer += 1
        tc = too_close() 
        if local_timer > 40:
            return 3
        if tc:
            local_timer += 1
            return -2
        if attack_timer > attack_thresh:
            return 3
    return -2
    # if ene == 0:
    #     return 3
    # elif flank > 3:
    #     return 3
    # elif flank > 2 and col < board_size/2:
    #     return 3


def halt():
    global team, opp_team, robottype, forward, row, col, pawn_state, timer, pawn_thresh
    

    # dlog("HALT")
    if attempt_capture():
        return
    if flank_secured() > 0:
        # if timer > pawn_thresh:
        if True:
            pawn_state = "ADVANCE"
            attempt_forward()
        else:
            return
    else:
        pawn_state = "ADVANCE"
        attempt_forward()
        return

def pawn():
    global team, opp_team, robottype, forward, row, col, pawn_state, timer, pawn_thresh
    row, col = get_location()
    # dlog('My location is: ' + str(row) + ' ' + str(col))


    # pawn_switcher = {
    #     "STAGE": stage,
    #     "ADVANCE": advance,
    #     "HALT": halt
    # }

    # func = pawn_switcher.get(pawn_state)
    # func()
    advance()

def turn():
    """
    MUST be defined for robot to run
    This function will be called at the beginning of every turn and should contain the bulk of your robot commands
    """
    global team, opp_team, robottype, forward, row, col, pawn_state, timer
    timer += 1

    if robottype == RobotType.PAWN:
        pawn()

    # OVERLORD
    else:
        overlord()

    bytecode = get_bytecode()
    # dlog('Done! Bytecode left: ' + str(bytecode))

