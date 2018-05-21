"""CamTacToe - play tic tac toe against the greats"""
import re
import time
import random
import emoji

class Game(object):
    """Base game class
    Contains only basic variables at this point that should apply to any game
    """
    def __init__(self):
        self.game_started = False
        self.game_ended = False


class CamTacToe(Game):
    """This is the good shit, the shit you heard your buddy whispering about
    Smarter than Watson and faster than Sunway TaihuLight; you better
    bring your A-game if you're not tryna come off lookin like a fool
    """
    def __init__(self):
        """Initialize base class and camtactoe class variables
        These can be modified to change different aspects of the game
        """
        super(CamTacToe, self).__init__()
        self.state = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.history = [self.state[:]]
        self.player_char = 'x'
        self.opponent_char = 'o'
        self.difficulty = 0
        self.player_start = 0

    def __draw_board(self, state=None):
        """Draw the game board to the console"""
        if not state:
            state = self.state
        if self.game_started:
            print('\r\033[8A')
        print(emoji.emojize(' {state[0]} | {state[1]} | {state[2]} \n___|___|___\n'
                            ' {state[3]} | {state[4]} | {state[5]} \n___|___|___\n'
                            ' {state[6]} | {state[7]} | {state[8]} \n   |   |   \n'.format(state=state)))


    def __make_move(self, user):
        """Make a move, used by both the player and the AI"""
        if user:
            pos = int(input('Make your move (1-9): '))
            print('\033[2A\r                                       ')
            while self.state[pos-1] != ' ':
                pos = int(input('\rSeat\'s taken. Make your move (1-9): '))
                print('\033[2A\r                                       ')
            self.state[pos-1] = self.player_char
        else:
            time.sleep(.5)
            pos = random.randint(1, 9)
            if self.difficulty == 1:
                best = self.__find_best()
                pos = best+1 if best else pos
            while self.state[pos-1] != ' ':
                pos = random.randint(1, 9)
            self.state[pos-1] = self.opponent_char
        self.history.append(self.state[:])

    def __find_best(self):
        """Finds the best move to take for the AI.
        Looks one move ahead to see if there is a move that will win or a
        move that will block a win
        """
        # First look for offensive moves
        for i in range(0, 3):
            col = self.__get_col(i)
            if len(col.get('empty')) == 1:
                if col.get(self.opponent_char) == 2:
                    return col.get('empty')[0]
        for i in range(0, 3):
            row = self.__get_row(i)
            if len(row.get('empty')) == 1:
                if row.get(self.opponent_char) == 2:
                    return row.get('empty')[0]
        for i in range(0, 2):
            diag = self.__get_diag(i)
            if len(diag.get('empty')) == 1:
                if diag.get(self.opponent_char) == 2:
                    return diag.get('empty')[0]

        # Then check again looking for defensive moves
        for i in range(0, 3):
            col = self.__get_col(i)
            if len(col.get('empty')) == 1:
                if col.get(self.player_char) == 2:
                    return col.get('empty')[0]
        for i in range(0, 3):
            row = self.__get_row(i)
            if len(row.get('empty')) == 1:
                if row.get(self.player_char) == 2:
                    return row.get('empty')[0]
        for i in range(0, 2):
            diag = self.__get_diag(i)
            if len(diag.get('empty')) == 1:
                if diag.get(self.player_char) == 2:
                    return diag.get('empty')[0]

        ##### CLEAN THIS METHOD UP LATER #####
        return None


    def __check_winner(self):
        """Checks to see if anyone has won or if there are no moves left"""
        for i in range(0, 3):
            col = self.__get_col(i)
            if col.get(self.player_char) == 3:
                print('\nYou win!')
                self.game_ended = True
                return
            if col.get(self.opponent_char) == 3:
                print('\nYou lose.')
                self.game_ended = True
                return
            row = self.__get_row(i)
            if row.get(self.player_char) == 3:
                print('\nYou win!')
                self.game_ended = True
                return
            if row.get(self.opponent_char) == 3:
                print('\nYou lose.')
                self.game_ended = True
                return
        for i in range(0, 2):
            diag = self.__get_diag(i)
            if diag.get(self.player_char) == 3:
                print('\nYou win!')
                self.game_ended = True
                return
            if diag.get(self.opponent_char) == 3:
                print('\nYou lose.')
                self.game_ended = True
                return
        if self.state.count(' ') == 0:
            print('\nDraw!')
            self.game_ended = True


    def __get_col(self, index):
        """Gets data for the column at the given index"""
        counts = {
            self.player_char: 0,
            self.opponent_char: 0,
            'empty': []
        }
        for i in range(0, 3):
            if self.state[index+(i*3)] is self.player_char:
                counts[self.player_char] += 1
            elif self.state[index+(i*3)] is self.opponent_char:
                counts[self.opponent_char] += 1
            else:
                counts['empty'].append(index+(i*3))
        return counts

    def __get_row(self, index):
        """Gets data for the row at the given index"""
        counts = {
            self.player_char: 0,
            self.opponent_char: 0,
            'empty': []
        }
        for i in range(0, 3):
            if self.state[(index*3)+i] is self.player_char:
                counts[self.player_char] += 1
            elif self.state[(index*3)+i] is self.opponent_char:
                counts[self.opponent_char] += 1
            else:
                counts['empty'].append((index*3)+i)
        return counts

    def __get_diag(self, index):
        """Gets data for the diagonal at the given index
        In this case 0 is '\' and 1 is '/'
        """
        counts = {
            self.player_char: 0,
            self.opponent_char: 0,
            'empty': []
        }
        if index is 0:
            for i in range(0, 3):
                if self.state[(i*3)+i] is self.player_char:
                    counts[self.player_char] += 1
                elif self.state[(i*3)+i] is self.opponent_char:
                    counts[self.opponent_char] += 1
                else:
                    counts['empty'].append((i*3)+i)
        if index is 1:
            for i in range(0, 3):
                if self.state[(i*3)+(2-i)] is self.player_char:
                    counts[self.player_char] += 1
                elif self.state[(i*3)+(2-i)] is self.opponent_char:
                    counts[self.opponent_char] += 1
                else:
                    counts['empty'].append((i*3)+(2-i))
        return counts

    def play(self):
        """The play method for the game
        Plays the game with the current configuration
        """
        self.__draw_board()
        self.game_started = True
        turn = self.player_start
        while not self.game_ended:
            self.__make_move(turn)
            self.__draw_board()
            self.__check_winner()
            turn = abs(turn-1)

    def print_history(self):
        """Prints the history of the game"""
        self.game_started = False
        for state in self.history:
            self.__draw_board(state)

if __name__ == '__main__':
    MYGAME = CamTacToe()

    DIFFICULTY = input('Choose your difficuty (0,1): ')
    if DIFFICULTY in ['0', '1']:
        MYGAME.difficulty = int(DIFFICULTY)
    else:
        print('Invalid entry, defaulted to 0')

    STARTING_PLAYER = input('You want to go first? ')
    if re.match(r'[y|sure|aff|of course]', STARTING_PLAYER):
        MYGAME.player_start = 1
    else:
        print('It\'s over player, I have the high ground')

    MYGAME.player_char = ':fire:'
    MYGAME.opponent_char = ':hundred_points:'
    MYGAME.play()
    REPLAY = input('Ready for that instant replay? ')
    if re.match(r'[y|sure|aff|of course]', REPLAY):
        MYGAME.print_history()
