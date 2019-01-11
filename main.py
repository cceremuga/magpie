import chess
import random
from prompt_toolkit import prompt
from prompt_toolkit.styles import Style

WHITE_MOVE_NOTATION = '.'
BLACK_MOVE_NOTATION = '...'
QUIT_COMMANDS = ['q', 'quit', 'exit']
WHITE_SIDE = 'w'
BLACK_SIDE = 'b'

class Magpie:
    def __init__(self):
        self.chess_board = chess.Board()
        self.white_to_move = True
        self.move_counter = 1
        self.prompt_style = Style.from_dict({ 'prompt': '#ff0066' })
        self.prompt_message = [('class:prompt', 'Magpie>> ')]

        print('')
        print('~Magpie Chess Engine~')
        print('Stupidly early developer edition v0.01')
        print('')

        side = self.main_menu_loop();
        self.game_loop(side)

    def game_loop(self, side):
        print('')
        print('Use algebraic notation for all move input.')

        while True:
            if self.is_game_over():
                self.end_game()

            if self.is_user_move(side):
                self.user_move()
            else:
                self.ai_move()

    def end_game(self):
        print('Game over. Thanks for playing.')
        quit()

    def is_game_over(self):
        self.chess_board.is_checkmate() or self.chess_board.is_stalemate()

    def is_user_move(self, side):
        if self.white_to_move:
            if side == WHITE_SIDE:
                return True
            else:
                return False
        else:
            if side == WHITE_SIDE:
                return False
            else:
                return True

    def user_move(self):
        try:
            input_command = self.get_move()

            if input_command in QUIT_COMMANDS:
                quit()

            try:
                self.attempt_move(input_command)
            except ValueError:
                print('Unrecognized command, or move.')

        except KeyboardInterrupt:
            quit()

    def ai_move(self):
        print('')
        print('I am thinking...')
        move = self.get_best_move()
        self.attempt_move(move)

    def attempt_move(self, move):
        self.chess_board.push_san(move)
        self.output_board_state(move)

        if self.white_to_move:
            self.white_to_move = False
        else:
            self.white_to_move = True

    def quit(self):
        print('')
        print('Later!')
        print('')
        raise SystemExit

    def get_move(self):
        print('')
        if (self.white_to_move):
            print('White to move.')
        else:
            print('Black to move.')

        return self.get_input()

    def get_input(self):
        print('')
        return prompt(self.prompt_message, style=self.prompt_style)

    def output_board_state(self, move):
        print('')
        print(self.move_counter, WHITE_MOVE_NOTATION if self.white_to_move else BLACK_MOVE_NOTATION , move, sep='')
        print('')
        print(self.chess_board.unicode())

        if not self.white_to_move:
            self.move_counter = self.move_counter + 1

    def get_best_move(self):
        moves = []

        for move in self.chess_board.legal_moves:
            moves.append(move)

        secure_random = random.SystemRandom()
        return self.chess_board.san(secure_random.choice(moves))

    def main_menu_loop(self):
        while True:
            try:
                input_command = self.get_side_choice()

                if input_command in QUIT_COMMANDS:
                    quit()

                if input_command == '':
                    return WHITE_SIDE

                if input_command == WHITE_SIDE or input_command == BLACK_SIDE:
                    return input_command
                else:
                    print('')
                    print('Unknown command.')

            except KeyboardInterrupt:
                quit()

    def get_side_choice(self):
        print('Which side would you like to play? w for white or b for black. [w]')
        return self.get_input()

if __name__ == '__main__':
    Magpie()