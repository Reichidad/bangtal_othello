from bangtal import *

setGameOption(GameOption.INVENTORY_BUTTON, False)
setGameOption(GameOption.MESSAGE_BOX_BUTTON, False)
setGameOption(GameOption.ROOM_TITLE, False)

scene1 = Scene("Othello Game", "images/background.png")
BLANK = 'images/blank.png'
POSSIBLE = ['images/black possible.png', 'images/white possible.png']
BLACK = 'images/black.png'
WHITE = 'images/white.png'

turn_state = [BLACK, WHITE]
turn_counter = 0

class Stone(Object):
    state = BLANK

    def set_state(self, state_input):
        self.state = state_input
        super().setImage(self.state)

stones = [[Stone(BLANK) for i in range(8)] for i in range(8)]


def game_init(stones):
    size = 80
    stones[3][3].set_state(BLACK)
    stones[4][4].set_state(BLACK)
    stones[4][3].set_state(WHITE)
    stones[3][4].set_state(WHITE)
    for i in range(8):
        for j in range(8):
            stones[i][j].locate(scene1, 40 + i * size, 40 + j * size)
            stones[i][j].show()
            stones[i][j].onMouseAction = lambda mx, my, action, ix = i, iy =j: changeState(ix, iy)


def counter_dir(x, y, dx, dy):
    turn = turn_counter % 2
    mine, other = turn_state[turn], turn_state[turn-1]
    possible_flag = False
    counter = 0

    while True:
        x += dx
        y += dy

        if x < 0 or x > 7: return counter
        if y < 0 or y > 7: return counter

        object = stones[x][y]
        if object.state == other:
            possible_flag = True
        elif object.state == mine:
            if possible_flag:
                while True:
                    x += - dx
                    y += - dy

                    change = stones[x][y]
                    if change.state == other:
                        counter += 1
                    else:
                        return counter
        else: return counter

def ai_counter(x, y):
    counter = 0
    counter += counter_dir(x, y, 0, 1)
    counter += counter_dir(x, y, 1, 1)
    counter += counter_dir(x, y, 1, 0)
    counter += counter_dir(x, y, 1, -1)
    counter += counter_dir(x, y, 0, -1)
    counter += counter_dir(x, y, -1, -1)
    counter += counter_dir(x, y, -1, 0)
    counter += counter_dir(x, y, -1, 1)

    return counter

def setPossible_xy_dir(x, y, dx, dy):
    turn = turn_counter % 2
    mine, other = turn_state[turn], turn_state[turn-1]
    possible_flag = False

    while True:
        x += dx
        y += dy

        if x < 0 or x > 7: return False
        if y < 0 or y > 7: return False

        object = stones[x][y]
        if object.state == other:
            possible_flag = True
        elif object.state == mine:
            return possible_flag
        else: return False



def setPossible_xy(x, y):
    object = stones[x][y]
    if object.state == BLACK: return False
    if object.state == WHITE: return False
    stones[x][y].set_state(BLANK)

    if setPossible_xy_dir(x, y, 0, 1): return True
    if setPossible_xy_dir(x, y, 1, 1): return True
    if setPossible_xy_dir(x, y, 1, 0): return True
    if setPossible_xy_dir(x, y, 1, -1): return True
    if setPossible_xy_dir(x, y, 0, -1): return True
    if setPossible_xy_dir(x, y, -1, -1): return True
    if setPossible_xy_dir(x, y, -1, 0): return True
    if setPossible_xy_dir(x, y, -1, 1): return True
    return False


def setPossible():
    global turn_counter
    flag = False
    ai_dict = {"max" : 0, "x" : -1, "y" : -1}

    b, w = stones_counter()
    num_print(b, w)

    for x in range(8):
        for y in range(8):
            if setPossible_xy(x, y):
                stones[x][y].set_state(POSSIBLE[turn_counter % 2])
                if turn_counter % 2 == 1:
                    max = ai_counter(x, y)
                    if ai_dict["max"] < max:
                        ai_dict["max"] = max
                        ai_dict["x"] = x
                        ai_dict["y"] = y
                flag = True
    if turn_counter %2 == 1 and flag is True:
        stones[ai_dict["x"]][ai_dict["y"]].set_state(turn_state[turn_counter % 2])
        reverse(ai_dict["x"], ai_dict["y"])
        turn_counter += 1
        return setPossible()

    return flag


def reverse_dir(x, y, dx, dy):
    turn = turn_counter % 2
    mine, other = turn_state[turn], turn_state[turn-1]
    possible_flag = False

    while True:
        x += dx
        y+= dy

        if x < 0 or x > 7: return
        if y < 0 or y > 7: return

        object = stones[x][y]
        if object.state == other:
            possible_flag = True
        elif object.state == mine:
            if possible_flag:
                while True:
                    x += - dx
                    y += - dy

                    change = stones[x][y]
                    if change.state == other:
                        change.set_state(mine)
                    else:
                        return
        else: return

def reverse(x, y):
    reverse_dir(x, y, 0, 1)
    reverse_dir(x, y, 1, 1)
    reverse_dir(x, y, 1, 0)
    reverse_dir(x, y, 1, -1)
    reverse_dir(x, y, 0, -1)
    reverse_dir(x, y, -1, -1)
    reverse_dir(x, y, -1, 0)
    reverse_dir(x, y, -1, 1)


def stones_counter():
    b = 0
    w = 0
    for x in range(8):
        for y in range(8):
            if stones[x][y].state == BLACK:
                b += 1
            elif stones[x][y].state == WHITE:
                w += 1
    return b, w


nums = []
def num_print(b, w):
    global nums
    for num in nums:
        num.hide()
    num_b1 = Object('images/L'+ str(b//10) + '.png')
    num_b1.locate(scene1, 750, 220)
    num_b2 = Object('images/L'+ str(b%10) + '.png')
    num_b2.locate(scene1, 830, 220)
    num_w1 = Object('images/L'+ str(w//10) + '.png')
    num_w1.locate(scene1, 1070, 220)
    num_w2 = Object('images/L'+ str(w%10) + '.png')
    num_w2.locate(scene1, 1150, 220)
    nums = [num_b1, num_b2, num_w1, num_w2]
    for num in nums:
        num.show()

def changeState(x, y):
    global turn_counter
    if stones[x][y].state == POSSIBLE[turn_counter % 2]:
        stones[x][y].set_state(turn_state[turn_counter % 2])
        reverse(x, y)
        turn_counter += 1
        if not setPossible():
            turn_counter += 1
            if not setPossible():
                showMessage("게임이 종료되었습니다.")


game_init(stones)
setPossible()
startGame(scene1)
