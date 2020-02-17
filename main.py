#!/usr/bin/env python3

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
        self.prompt_style = Style.from_dict({'prompt': '#ff0066'})
        self.prompt_message = [('class:prompt', 'Magpie>> ')]

        print('')
        print('~Magpie Chess Engine~')
        print('Stupidly early developer edition v0.01')
        print('')

        side = self.main_menu_loop()
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
        print(self.move_counter, WHITE_MOVE_NOTATION if self.white_to_move else BLACK_MOVE_NOTATION, move, sep='')
        print('')
        print(self.chess_board.unicode())

        if not self.white_to_move:
            self.move_counter = self.move_counter + 1

    def get_best_move(self):
        ugly_moves = []

        for move in self.chess_board.legal_moves:
            ugly_moves.append(move)

        best_move = None
        best_value = -9999

        for move in ugly_moves:
            self.chess_board.push(move)
            board_value = -(self.evaluate())

            self.chess_board.pop()

            if board_value > best_value:
                best_value = board_value
                best_move = move

        return self.chess_board.san(best_move)

    def evaluate(self):
        total_evaluation = 0

        i = 0
        j = 0

        while i < 8:
            while j < 8:
                total_evaluation += self.get_piece_value(i, j)
                j += 1
            i += 1

        return total_evaluation

    def get_piece_value(self, file, rank):
        square = chess.square(file, rank)
        piece = self.chess_board.piece_at(square)

        if piece is None:
            return 0

        absolute_value = self.get_absolute_value(piece.symbol().lower())

        if piece.color:
            return absolute_value
        else:
            return -1 * absolute_value

    def get_absolute_value(self, piece):
        if piece == 'p':
            return 10

        if piece == 'r':
            return 50

        if piece == 'n':
            return 30

        if piece == 'b':
            return 30

        if piece == 'q':
            return 90

        if piece == 'k':
            return 900

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
        print('You will be playing as the white pieces.')
        return WHITE_SIDE
        # return self.get_input()


if __name__ == '__main__':
    Magpie()
