import yaml


class GameInstance:
    def __init__(self, name_of_gamefile):


        """
        file encoded in yaml consist of information about the board and playerposition, and the treasures
        respectively:
            Board elements are: 'a' for place on which one can stand
                                'b' for place on which one cannot stand
                                'aa' for treasures
                                'ab' for traps
                                'c' is player
            Playerposition is list consist of three elements, the first two are position, third one is a number
             of collected treasures
        """
        with open(name_of_gamefile, 'r') as gamefile:
            x = yaml.load(gamefile)
            self.playerpos = x['playerpos']
            self.board = x['board']

        number_of_treasures_left = 0
        for line in self.board:
            if 'aa' in line:
                for sign in line:
                    if sign == 'aa':
                        number_of_treasures_left += 1
        if self.playerpos[-1] == 0 and len(self.playerpos) == 3:
            self.playerpos.append(number_of_treasures_left)
        self.score = self.playerpos[-1] * 10
        self.actionlist = ((-1, 0), (1, 0), (0, 1), (0, -1))

    def move(self, direction):
        try:
            action = 'NSEW'.index(direction)
            nextpos = [self.playerpos[0] + self.actionlist[action][0], self.playerpos[1] + self.actionlist[action][1]]
            nextsign = self.board[nextpos[0]][nextpos[1]]
            if nextsign[0] == 'b':
                return False
            if len(nextsign) == 2:
                if nextsign[1] == 'b':
                    return True
                if nextsign[1] == 'a':
                    self.playerpos[-1] -= 1
                    self.score += 1000
                    if self.playerpos[-1] == 0:
                        return True
                    else:
                        self.playerpos[0] = nextpos[0]
                        self.playerpos[1] = nextpos[1]

            self.playerpos[0] += self.actionlist[action][0]
            self.playerpos[1] += self.actionlist[action][1]
            self.score -= 10

        except ValueError:
            return

    def display_board(self):
        number_of_line = 0
        for line in self.board:
            temporary_line = line
            if number_of_line == self.playerpos[0]:
                temporary_line[self.playerpos[1]] = 'c'
                print(*temporary_line, end="\n")
                temporary_line[self.playerpos[1]] = 'a'
            else:
                print(*temporary_line, end="\n")
            number_of_line += 1

    def getinput(self):
        while True:
            tempinput = input("GO!")
            if tempinput in "nsweNSWE":
                return tempinput.upper()
            elif tempinput in 'Qq':
                self.savegame()
                print("saved")
                continue

    def savegame(self):
        savegame = {'board': self.board,
                    'playerpos': self.playerpos,
                    'score': self.score}
        with open('save.yml', 'w') as savefile:
            yaml.dump(savegame, savefile, default_flow_style=False)


while True:

    x = input('To load game press l, to newgame press n')
    if x in 'lL':
        game = GameInstance('save.yml')
    else:
        game = GameInstance('new 2.yml')
    while True:
        game.display_board()
        temp = game.getinput()
        temp = game.move(temp)
        if temp:
            if game.playerpos[-1] == 0:
                result = 'won'
            else:
                result = 'lost'
            print('Game over, Score: {0}, You {1}'.format(game.score, result))
            break
    input("press any to load again")

