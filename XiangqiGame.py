# Author: Chad Smith
# Date:02/24/2020
# Description: A Chinese Chess program. Players are 'red' and 'black'. Player 'red' moves first and
# then players alternate turns until the game state is updated to 'RED_WON' or 'BLACK_WON'. If a
# move is invalid the move method returns False, otherwise it returns True. There is a display_board
# method which will allows for tracking piece movement. Classes are XiangqiGame, Piece, General,
# Guard, Cannon, Soldier, Elephant, Chariot and Horse.


class XiangqiGame:
    """Contains a data member for the current player's turn, the game state, whether Red is in check
    or whether black is in check, a board data member which is a list of lists that contains the
    piece data members which make up all of the game pieces and two data members for tracking the
    location of bK and rK (black General/King and red General/King). There are getter and setter
    methods, an is_in_check method, a move method, a self_in_check method, an opponent_in_check
    method and a display_board method."""

    def __init__(self):
        self._turn = 'red'
        self._game_state = 'UNFINISHED'
        self._red_in_check = False
        self._black_in_check = False
        self._board = [['--'] * 9 for num in range(10)]
        self._black_general = General('black')  #
        self._red_general = General('red')  #
        self._black_guard = Guard('black')  #
        self._red_guard = Guard('red')
        self._black_cannon = Cannon('black')
        self._red_cannon = Cannon('red')
        self._black_soldier = Soldier("black")
        self._red_soldier = Soldier('red')
        self._black_elephant = Elephant('black')
        self._red_elephant = Elephant('red')
        self._black_chariot = Chariot('black')
        self._red_chariot = Chariot('red')
        self._black_horse = Horse('black')
        self._red_horse = Horse('red')

        self._board[9][4] = self._black_general.get_piece()
        self._board[9][3] = self._board[9][5] = self._black_guard.get_piece()
        self._board[9][2] = self._board[9][6] = self._black_elephant.get_piece()
        self._board[9][1] = self._board[9][7] = self._black_horse.get_piece()
        self._board[9][0] = self._board[9][8] = self._black_chariot.get_piece()
        self._board[7][1] = self._board[7][7] = self._black_cannon.get_piece()
        self._board[6][0] = self._board[6][2] = self._board[6][4] = self._board[6][6] = \
            self._board[6][8] = self._black_soldier.get_piece()

        self._board[0][4] = self._red_general.get_piece()
        self._board[0][3] = self._board[0][5] = self._red_guard.get_piece()
        self._board[0][2] = self._board[0][6] = self._red_elephant.get_piece()
        self._board[0][1] = self._board[0][7] = self._red_horse.get_piece()
        self._board[0][0] = self._board[0][8] = self._red_chariot.get_piece()
        self._board[2][1] = self._board[2][7] = self._red_cannon.get_piece()
        self._board[3][0] = self._board[3][2] = self._board[3][4] = self._board[3][6] = \
            self._board[3][8] = self._red_soldier.get_piece()
        self._bK_position = [9, 4]
        self._rK_position = [0, 4]

    def get_turn(self):
        """Returns XiangqiGame's turn data member."""
        return self._turn

    def get_game_state(self):
        """Returns XiangqiGame's game_state data member."""
        return self._game_state

    def get_bk_position(self):
        """Returns the bK's (Black King/General) position."""
        return self._bK_position

    def get_rk_position(self):
        """Returns the rK's (Red King/General) position."""
        return self._rK_position

    def get_red_in_check(self):
        """Returns red_in_check."""
        return self._red_in_check

    def get_black_in_check(self):
        """Returns black in check."""
        return self._black_in_check

    def set_bk_position(self, row, column):
        """Sets the bK's (Black King/General) position."""
        self._bK_position = [row, column]

    def set_rk_position(self, row, column):
        """Sets the rK's (Red King/General) position."""
        self._rK_position = [row, column]

    def set_turn(self, turn):
        """Sets XiangqiGame's turn data member."""
        self._turn = turn

    def set_game_state(self, new_state):
        """Sets XiangqiGame's game_state data member."""
        self._game_state = new_state

    def end_turn(self):
        """Updates the turn data member from red to black or black to red."""
        if self.get_turn() == 'red':
            self.set_turn('black')
        elif self.get_turn() == 'black':
            self.set_turn('red')

    def is_in_check(self, red_or_black):
        """Takes as a parameter either 'red' or 'black' and returns True if that player is in
        check, otherwise returns False."""

        if red_or_black == 'red':
            if self.get_red_in_check():
                return True
        elif red_or_black == 'black':
            if self.get_black_in_check():
                return True
        return False

    def make_move(self, from_square, to_square):
        """Takes two parameters - strings that represent the square moved from and the square moved
        to. If the square being moved from does not contain a piece belonging to the player whose
        turn it is, or if the indicated move is not legal, or if the game has already been won, then
        it should just return False. Otherwise it should make the indicated move, remove any
        captured piece, update the game state if necessary, update whose turn it is, and return
        True."""

        if self.get_game_state() != "UNFINISHED":
            # Game is over
            return False

        input_validation = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

        move_dictionary = {
            'i': 0,
            'h': 1,
            'g': 2,
            'f': 3,
            'e': 4,
            'd': 5,
            'c': 6,
            'b': 7,
            'a': 8
        }
        # *****************************************************************************************
        # This section contains input validation and checks if move is within the board's boundary
        # *****************************************************************************************

        # checks to make sure the correct colored piece is being moved
        column = move_dictionary[from_square[0]]
        if len(from_square) == 3:
            row = 9
        else:
            row = (int(from_square[1]) - 1)
        if self._board[row][column][0] != self.get_turn()[0]:
            return False

        # checks to make sure the 'from square' is different from the 'to square'
        if from_square == to_square:
            return False

        # checks if the letter given is a valid file/column
        if from_square[0] not in move_dictionary or to_square[0] not in move_dictionary:
            return False

        # if the length of the coordinate is greater than 3 or less than 2, it is an invalid move
        if len(from_square) > 3 or len(to_square) > 3 or len(from_square) < 2 or len(to_square) < 2:
            return False

        # if coordinate length is 3, then the row must be equal to 10 to be a valid move
        if len(from_square) == 3:
            if int(from_square[1:3]) != 10:
                return False
        if len(to_square) == 3:
            if int(to_square[1:3]) != 10:
                return False

        # checks if invalid string characters are used
        if from_square[1] not in input_validation or to_square[1] not in input_validation:
            return False

        # checks if the 'from square' is empty
        if len(from_square) == 3:
            if self._board[9][move_dictionary[from_square[0]]] == '--':
                # The 'move from' coordinates point to an empty square
                return False
        else:
            if self._board[int(from_square[1]) - 1][move_dictionary[from_square[0]]] == '--':
                # The 'move from' coordinates point to an empty square
                return False

        # checks if the 'to square' has your own piece
        if len(to_square) == 3:
            if self._board[9][move_dictionary[to_square[0]]][0] == 'r':
                if self.get_turn() == 'red':
                    # Red piece cannot move to position occupied by red piece
                    return False
            if self._board[9][move_dictionary[to_square[0]]][0] == 'b':
                if self.get_turn() == 'black':
                    # Black piece cannot move to position occupied by black piece
                    return False
        else:
            if self._board[int(to_square[1]) - 1][move_dictionary[to_square[0]]][0] == 'r':
                if self.get_turn() == 'red':
                    # Red piece cannot move to position occupied by red piece
                    return False
            if self._board[int(to_square[1]) - 1][move_dictionary[to_square[0]]][0] == 'b':
                if self.get_turn() == 'black':
                    # Black piece cannot move to position occupied by black piece
                    return False

        # *****************************************************************************************
        # This section calls the piece's move method for additional move validation
        # *****************************************************************************************
        obj_dictionary = {
            'rK': self._red_general,
            'bK': self._black_general,
            'rG': self._red_guard,
            'bG': self._black_guard,
            'rE': self._red_elephant,
            'bE': self._black_elephant,
            'rH': self._red_horse,
            'bH': self._black_horse,
            'rT': self._red_chariot,
            'bT': self._black_chariot,
            'rC': self._red_cannon,
            'bC': self._black_cannon,
            'rS': self._red_soldier,
            'bS': self._black_soldier
        }

        # converts from_square and to_square to list coordinates
        if len(from_square) == 3:
            from_row_coordinate = 9
        else:
            from_row_coordinate = (int(from_square[1]) - 1)
        from_column_coordinate = move_dictionary[from_square[0]]

        if len(to_square) == 3:
            to_row_coordinate = 9
        else:
            to_row_coordinate = (int(to_square[1]) - 1)
        to_column_coordinate = move_dictionary[to_square[0]]

        # access the object being moved and call it's move method passing coordinates for the move
        valid_move = obj_dictionary[self._board[from_row_coordinate][from_column_coordinate]].move(
            from_row_coordinate, from_column_coordinate, to_row_coordinate, to_column_coordinate,
            self._board)
        # if valid move was set to True from piece's move method then does not return
        if valid_move == False:
            # The object's move method returned False for invalid move
            return False

        # *****************************************************************************************
        # Moves piece and checks if it places current player's King in check, if yes, reverses move.
        # Test pieces and coordinates are used in order to avoid making unwanted changes to objects.
        # *****************************************************************************************

        def self_in_check(from_row, from_column, to_row, to_column, king_row, king_column):

            test_piece = str(self._board[from_row][from_column])    # string at the 'from' location
            to_position = str(self._board[to_row][to_column])       # string at the 'to' location
            self._board[from_row][from_column] = '--'
            self._board[to_row][to_column] = str(test_piece)

            # position of the General/King
            k_position = [int(king_row), int(king_column)]

            if test_piece == 'rK' or test_piece == 'bK':
                # Updates the location of rK and bK if moved
                original_king_row = int(king_row)
                original_king_col = int(king_column)

                if test_piece == 'rK' or test_piece == 'bK':
                    k_position = [to_row, to_column]

            # Tests for self check. Calls the move method for all offensive opposing pieces using
            # the General's coordinates for the 'to square' coordinates. If True is returned, an
            # opposing player's move to your king is valid and you would be in check.

            self_check = None
            check_counter = 0
            if test_piece[0] == 'b':
                for rows in range(0, 10):
                    for col in range(0, 9):
                        if self._board[rows][col][0] == 'r':
                            self_check = obj_dictionary[self._board[rows][col]].move(rows, col,
                                k_position[0], k_position[1], self._board)
                            if self_check is True:        # you've placed yourself in check
                                check_counter += 1

            elif test_piece[0] == 'r':
                for rows in range(0, 10):
                    for col in range(0, 9):
                        if self._board[rows][col][0] == 'b':
                            self_check = obj_dictionary[self._board[rows][col]].move(rows, col,
                                k_position[0], k_position[1], self._board)

                            if self_check is True:        # you've placed yourself in check
                                check_counter += 1

            # reverse test_piece move, as you cannot place yourself in check
            self._board[to_row][to_column] = str(to_position)
            self._board[from_row][from_column] = str(test_piece)

            if check_counter > 0:
                # print("You cannot place yourself in check.")
                return True

            return False

        # runs the self_in_check method with coordinates for the red kind or black king, depending
        # on the who's turn it is
        if self.get_turn() == 'red':
            placed_myself_in_check = self_in_check(from_row_coordinate, from_column_coordinate,
                                                   to_row_coordinate, to_column_coordinate,
                                                   int(int(self.get_rk_position()[0])),
                                                   int(int(self.get_rk_position()[1])))
        else:
            placed_myself_in_check = self_in_check(from_row_coordinate, from_column_coordinate,
                                                   to_row_coordinate, to_column_coordinate,
                                                   int(int(self.get_bk_position()[0])),
                                                   int(int(self.get_bk_position()[1])))

        # You cannot make a move which places yourself in check
        if placed_myself_in_check is True:
            return False

        # *****************************************************************************************
        # Moves the piece from one 'square' to the next. The validity of the move should be checked
        # before this block of code is reached.
        # *****************************************************************************************
        if len(from_square) == 3:
            piece = self._board[9][move_dictionary[from_square[0]]]
            self._board[9][move_dictionary[from_square[0]]] = '--'
        else:
            piece = self._board[int(from_square[1]) - 1][move_dictionary[from_square[0]]]
            self._board[int(from_square[1]) - 1][move_dictionary[from_square[0]]] = '--'

        if len(to_square) == 3:
            self._board[9][move_dictionary[to_square[0]]] = piece
            self.end_turn()
        else:
            self._board[int(to_square[1]) - 1][move_dictionary[to_square[0]]] = piece
            self.end_turn()

        # Updates the location of rK and bK if moved
        if self._board[to_row_coordinate][to_column_coordinate] == 'rK':
            self.set_rk_position(to_row_coordinate, to_column_coordinate)
        elif self._board[to_row_coordinate][to_column_coordinate] == 'bK':
            self.set_bk_position(to_row_coordinate, to_column_coordinate)

        # ****************************************************************************************
        # Checks if move just made places opponent in check. If black moved, then calls each black
        # piece move method with the 'to coordinates' for the red General. If any move returns True,
        # red is in check. Runs the same procedure if red moved with red pieces and black General
        # coordinates.
        # ****************************************************************************************

        def opponent_in_check(to_row, to_column):

            r_check = 0
            b_check = 0
            if self._board[to_row][to_column][0] == 'b':
                for row in range(0, 10):
                    for square in range(0, 9):
                        if self._board[row][square][0] == 'b':
                            if obj_dictionary[self._board[row][square]].move(row, square,
                                    self.get_rk_position()[0], self.get_rk_position()[1],
                                                                             self._board):
                                r_check += 1  # you've placed opponent in check

            elif self._board[to_row][to_column][0] == 'r':
                for row in range(0, 10):
                    for square in range(0, 9):
                        if self._board[row][square][0] == 'r':
                            if obj_dictionary[self._board[row][square]].move(row, square,
                                    self.get_bk_position()[0], self.get_bk_position()[1],
                                                                             self._board):
                                b_check += 1  # you've placed opponent in check

            # Sets r_check or b_check to True if check was identified above.
            if r_check > 0:
                self._red_in_check = True
            else:
                self._red_in_check = False
            if b_check > 0:
                self._black_in_check = True
            else:
                self._black_in_check = False

        # runs opponent in check method defined above
        opponent_in_check(to_row_coordinate, to_column_coordinate)

        # *****************************************************************************************
        # If a piece is in check. This block will check for check mate.
        # *****************************************************************************************

        if self.get_red_in_check(): # if red is in check this block runs
            num_moves_escape_check = 0
            rk_row = int(self.get_rk_position()[0])
            rk_col = int(self.get_rk_position()[1])
            for row in range(0, 10):
                for square in range(0, 9):  # loop through the whole board
                    if self._board[row][square][0] == 'r':  # if we found a red piece
                        for a_row in range(0, 10):
                            for a_square in range(0, 9):    # move red piece to every spot on board
                                # if the to_move does not contain a red piece
                                if self._board[a_row][a_square][0] != 'r':
                                    # if the object's move method returns True
                                    if obj_dictionary[self._board[row][square]].move(row, square,
                                                                    a_row, a_square, self._board):
                                        # test move with still_in_check method to verify if it gets
                                        # you out of check
                                        still_in_check = self_in_check(row, square, a_row, a_square,
                                                                       rk_row, rk_col)
                                        # makes sure the rk position wasn't inadvertently changed
                                        self.set_rk_position(rk_row, rk_col)

                                        if still_in_check is False:
                                            num_moves_escape_check += 1

            if num_moves_escape_check == 0:
                self.set_game_state('BLACK_WON')

        if self.get_black_in_check():   # if black is in check this block runs
            num_moves_escape_check = 0
            bk_row = int(self.get_bk_position()[0])
            bk_col = int(self.get_bk_position()[1])
            for row in range(0, 10):
                for square in range(0, 9):  # loop through the whole board
                    if self._board[row][square][0] == 'b':  # if we found a black piece
                        for a_row in range(0, 10):
                            for a_square in range(0, 9):   # move black piece to every spot on board
                                # if the to_move does not contain a red piece
                                if self._board[a_row][a_square][0] != 'b':
                                    # if the object's move method returns True
                                    if obj_dictionary[self._board[row][square]].move(row, square,
                                                                    a_row, a_square, self._board):
                                        # test move with still_in_check method to verify if it gets
                                        # you out of check
                                        still_in_check = self_in_check(row, square, a_row, a_square,
                                                                       bk_row, bk_col)
                                        # makes sure the bk position wasn't inadvertently changed
                                        self.set_bk_position(bk_row, bk_col)

                                        if still_in_check is False:
                                            num_moves_escape_check += 1

            if num_moves_escape_check == 0:
                self.set_game_state('RED_WON')

        # *****************************************************************************************
        # This last section checks for stalemate. If the player has no valid moves they lose.
        # *****************************************************************************************

        red_moves_remaining = 0
        rk_row = int(self.get_rk_position()[0])
        rk_col = int(self.get_rk_position()[1])
        for row in range(0, 10):
            for square in range(0, 9):  # loop through the whole board
                if self._board[row][square][0] == 'r':  # if we found a red piece
                    for a_row in range(0, 10):
                        for a_square in range(0, 9):  # move red piece to every spot on board
                            # if the to_move does not contain a red piece
                            if self._board[a_row][a_square][0] != 'r':
                                # if the object's move method returns True
                                if obj_dictionary[self._board[row][square]].move(row, square,
                                                                                 a_row, a_square,
                                                                                 self._board):
                                    # test move to verify if it places you in check
                                    if not self_in_check(row, square, a_row, a_square,
                                                                   rk_row, rk_col):
                                        # moves remain for red
                                        red_moves_remaining += 1
                                    # makes sure the rk position wasn't inadvertently changed
                                    self.set_rk_position(rk_row, rk_col)
                                    """
                                    print(obj_dictionary[self._board[row][square]], "rK pos: ",
                                          self.get_rk_position(), "remaining: ",
                                          red_moves_remaining)
                                    """
        black_moves_remaining = 0
        bk_row = int(self.get_bk_position()[0])
        bk_col = int(self.get_bk_position()[1])
        for row in range(0, 10):
            for square in range(0, 9):  # loop through the whole board
                if self._board[row][square][0] == 'b':  # if we found a black piece
                    for a_row in range(0, 10):
                        for a_square in range(0, 9):  # move black piece to every spot on board
                            # if the to_move does not contain a red piece
                            if self._board[a_row][a_square][0] != 'b':
                                # if the object's move method returns True
                                if obj_dictionary[self._board[row][square]].move(row, square,
                                                                                 a_row, a_square,
                                                                                 self._board):
                                    # test move to verify if it places you in check
                                    if not self_in_check(row, square, a_row, a_square,
                                                                   bk_row, bk_col):
                                        # moves remain for black
                                        black_moves_remaining += 1
                                    # makes sure the bk position wasn't inadvertently changed
                                    self.set_bk_position(bk_row, bk_col)

        if red_moves_remaining == 0:        # if red has no remaining moves, stalemate & black wins
            self.set_game_state('BLACK_WON')
        elif black_moves_remaining == 0:    # if black has no remaining moves, stalemate & red wins
            self.set_game_state('RED_WON')

        # last line of code to run for the move method, returns True per assignment
        return True

    def display_board(self):
        """Method which displays the board in its current state."""
        print('\n')
        print('   ', ' 0', '  1', '  2', '  3', '  4', '  5', '  6', '  7', '  8')
        row_num = 1
        for row in self._board:
            print(str(row_num).rjust(2), " ", end='')
            for square in row:
                print(square, " ", end='')
            print(row_num - 1)
            row_num += 1
        print('   ', ' i', '  h', '  g', '  f', '  e', '  d', '  c', '  b', '  a')


class Piece:
    """ Super class for all Chinese chess pieces. """

    def __init__(self, red_or_black):
        self._color = red_or_black
        self._piece = None

    def get_color(self):
        return self._color

    def get_piece(self):
        return self._piece


class General(Piece):
    """ General/King chess piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rK'
        elif red_or_black == 'black':
            self._piece = 'bK'

    def move(self, from_row, from_column, to_row, to_column, board):
        """ Accepts parameters for the 'from' coordinates and 'to' coordinates. Identifies whether
        the object being moved is red or black. Returns True if the move is a valid move and False
        otherwise. Moves one point vertically or horizontally and is confined to the palace. It may
        not move to the same column as the opposing General without intervening pieces."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        # red General must stay within the castle
        if self.get_piece()[0] == 'r':
            if to_row < 0 or to_row > 2 or to_column < 3 or to_column > 5:
                return False

        # black General must stay within the castle
        elif self.get_piece()[0] == 'b':
            if to_row < 7 or to_row > 9 or to_column < 3 or to_column > 5:
                return False

        # cannot make diagonal moves which would be increase/decrease in both row and column
        if from_row != to_row and from_column != to_column:
            return False
        # move horizontally 1 'square' at a time
        if from_row == to_row:
            if to_column != (from_column - 1) and to_column != (from_column + 1):
                return False
        # move vertically 1 'square' at a time
        elif from_column == to_column:
            if to_row != (from_row - 1) and to_row != (from_row + 1):
                return False

        # *****************************************************************************************
        # This Section Identifies Whether a General's move results in an empty file between Generals
        # *****************************************************************************************
        intervening_pieces = False      # this flags if intervening pieces exist between Generals
        # Identifies if the red General is being moved.
        if board[from_row][from_column] == 'rK':
            for num in range(0, 10):
                # If the red General is being moved, checks if the to_column contains black General
                if board[num][to_column] == 'bK':
                    for rows_to_bK in range(from_row+1, num):
                        # If the to_column contains the black General, checks if the column has any
                        # pieces located between the two Generals
                        if board[rows_to_bK][to_column] != '--':
                            intervening_pieces = True
                    if intervening_pieces is False:
                        # Generals would be facing each other without intervening pieces
                        return False
        # Identifies if the black General is being moved.
        if board[from_row][from_column] == 'bK':
            for num in range(0, 10):
                # If the red General is being moved, checks if the to_column contains black General
                if board[num][to_column] == 'rK':
                    for rows_to_rK in range(from_row-1, num, -1):
                        # If the to_column contains the black General, checks if the column has any
                        # pieces located between the two Generals
                        if board[rows_to_rK][to_column] != '--':
                            intervening_pieces = True
                    if intervening_pieces is False:
                        # Generals would be facing each other without intervening pieces
                        return False

        return True


class Guard(Piece):
    """ Guard chess piece. Sub class of Piece. """
    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rG'
        elif red_or_black == 'black':
            self._piece = 'bG'

    def move(self, from_row, from_column, to_row, to_column, board):
        """ Accepts parameters for the 'from' coordinates and 'to' coordinates. Identifies whether
        the object being moved is red or black. Returns True if the move is a valid move and False
        otherwise. Moves one point diagonally and is confined to the palace."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        # red Guard must stay within the castle
        if self.get_piece()[0] == 'r':
            if to_row < 0 or to_row > 2 or to_column < 3 or to_column > 5:
                return False

        # black Guard must stay within the castle
        elif self.get_piece()[0] == 'b':
            if to_row < 7 or to_row > 9 or to_column < 3 or to_column > 5:
                return False

        # must make diagonal moves which would be increase/decrease in both row and column
        if from_row == to_row and from_column == to_column:
            return False
        if from_row != (to_row + 1) and from_row != (to_row - 1):
            return False
        if from_column != (to_column + 1) and from_column != (to_column - 1):
            return False

        return True


class Cannon(Piece):
    """ Cannon chess piece. Sub class of Piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rC'
        elif red_or_black == 'black':
            self._piece = 'bC'

    def move(self, from_row, from_column, to_row, to_column, board):
        """ Returns True if the move is valid and False otherwise. Moves exactly like the chariot
        piece but captures differently. To capture the cannon must jump over exactly one piece, be
        it friend or foe, along its line of movement."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        # cannot make diagonal moves which would be increase/decrease in both row and column
        if from_row != to_row and from_column != to_column:
            return False

        num_of_pieces_between = 0

        if from_row == to_row:
            # right horizontal move
            if (to_column - from_column) > 0:
                for num in range(from_column + 1, to_column):
                    if board[from_row][num] != '--':
                        num_of_pieces_between += 1
            # left horizontal move
            elif (to_column - from_column) < 0:
                for num in range(from_column - 1, to_column, -1):
                    if board[from_row][num] != '--':
                        num_of_pieces_between += 1
        elif from_column == to_column:
            # forward vertical move (from red's perspective)
            if (to_row - from_row) > 0:
                for num in range(from_row + 1, to_row):
                    if board[num][from_column] != '--':
                        num_of_pieces_between += 1
            # backwards vertical move (from red's perspective)
            elif (to_row - from_row) < 0:
                for num in range(from_row - 1, to_row, -1):
                    if board[num][from_column] != '--':
                        num_of_pieces_between += 1

        # the cannon cannot jump more than 1 piece at a time
        if num_of_pieces_between > 1:
            return False

        # if there is 1 intervening piece, the cannon can capture if the 'to_square' contains an
        # opposing player's piece
        if num_of_pieces_between == 1 and board[from_row][from_column][0] == 'r':
            if board[to_row][to_column][0] != 'b':
                return False
        if num_of_pieces_between == 1 and board[from_row][from_column][0] == 'b':
            if board[to_row][to_column][0] != 'r':
                return False
        # if there are no intervening pieces the cannon cannot capture
        if num_of_pieces_between == 0 and board[to_row][to_column][0] != '-':
            return False

        return True


class Soldier(Piece):
    """ Soldier chess piece. Sub class of Piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rS'
        elif red_or_black == 'black':
            self._piece = 'bS'

    def move(self, from_row, from_column, to_row, to_column, board):
        """Returns True if the move is valid and False otherwise. Move and capture by advancing one
        point forward prior to crossing the river. Once the river is crossed it can move and
        capture one point horizontally as well. The pawn can never retreat or move backwards."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        # red soldier cannot move backwards
        if self.get_piece()[0] == 'r':

            # cannot make diagonal moves which would be increase/decrease in both row and column
            if from_row != to_row and from_column != to_column:
                return False

            #  Red soldier's moves before crossing the river
            if from_row <= 4:
                if from_column == to_column:   # Soldier must move vertically 1 'square' at a time
                    if to_row != (from_row + 1):    # Soldier cannot move backwards
                        return False
                else:
                    return False

            #  Red soldier's moves after crossing the river
            if from_row >= 5:
                # move horizontally 1 'square' at a time
                if from_row == to_row:
                    if to_column != (from_column - 1) and to_column != (from_column + 1):
                        return False
                # move forward 1 'square' at a time
                elif from_column == to_column:
                    if to_row != (from_row + 1):    # Soldier cannot move backwards
                        return False
                else:
                    return False

        # black soldier cannot move backwards
        elif self.get_piece()[0] == 'b':

            # cannot make diagonal moves which would be increase/decrease in both row and column
            if from_row != to_row and from_column != to_column:
                return False

            #  Black soldier's moves before crossing the river
            if from_row >= 5:
                if from_column == to_column:  # Soldier must move vertically 1 'square' at a time
                    if to_row != (from_row - 1):  # Soldier cannot move backwards
                        return False
                else:
                    return False

            #  Black soldier's moves after crossing the river
            if from_row <= 4:
                # move horizontally 1 'square' at a time
                if from_row == to_row:
                    if to_column != (from_column - 1) and to_column != (from_column + 1):
                        return False
                # move forward 1 'square' at a time
                elif from_column == to_column:
                    if to_row != (from_row - 1):  # Soldier cannot move backwards
                        return False
                else:
                    return False

        return True


class Elephant(Piece):
    """ Elephant chess piece. Sub class of Piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rE'
        elif red_or_black == 'black':
            self._piece = 'bE'

    def move(self, from_row, from_column, to_row, to_column, board):
        """ Returns True if the move is valid and False otherwise. Moves exactly two point in any
        diagonal direction and it may not jump over intervening pieces or cross the river."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        to_coordinates = [to_row, to_column]

        if self.get_piece()[0] == 'r':
            if to_row > 4:
                # Invalid move. Elephants cannot cross the river.
                return False

        if self.get_piece()[0] == 'b':
            if to_row < 5:
                # Invalid move. Elephants cannot cross the river.
                return False

        # the elephant has at most 4 valid moves listed below, if the coordinates for a valid move
        # are given, checks if there are any intervening pieces
        if to_coordinates == [from_row+2, from_column+2]:
            if board[from_row+1][from_column+1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row+2, from_column-2]:
            if board[from_row+1][from_column-1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row-2, from_column-2]:
            if board[from_row-1][from_column-1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row-2, from_column+2]:
            if board[from_row-1][from_column+1] != '--':
                return False
            else:
                return True
        else:
            return False


class Chariot(Piece):
    """ Chariot chess piece. Sub class of Piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rT'
        elif red_or_black == 'black':
            self._piece = 'bT'

    def move(self, from_row, from_column, to_row, to_column, board):
        """Returns True if the move is valid and False otherwise. Moves similar to a rook in
         international chess. It may move as many points as it chooses vertically or horizontally
         but it cannot jump over pieces in its path of movement."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        # diagonal moves are not allowed, move bust be in the must be same row or the same column

        if from_row == to_row:
            # right horizontal move
            if (to_column - from_column) > 0:
                for num in range(from_column+1, to_column):
                    if board[from_row][num] != '--':
                        return False
                return True

            # left horizontal move
            if (to_column - from_column) < 0:
                for num in range(from_column-1, to_column, -1):
                    if board[from_row][num] != '--':
                        return False
                return True

        elif from_column == to_column:
            # forward vertical move (from red's perspective)
            if (to_row - from_row) > 0:
                for num in range(from_row+1, to_row):
                    if board[num][from_column] != '--':
                        return False
                return True

                # backwards vertical move (from red's perspective)
            if (to_row - from_row) < 0:
                for num in range(from_row-1, to_row, -1):
                    if board[num][from_column] != '--':
                        return False
                return True
        else:
            return False


class Horse(Piece):
    """ Horse chess piece. Sub class of Piece. """

    def __init__(self, red_or_black):
        super().__init__(self)
        if red_or_black == 'red':
            self._piece = 'rH'
        elif red_or_black == 'black':
            self._piece = 'bH'

    def move(self, from_row, from_column, to_row, to_column, board):
        """ Returns True if the move is valid and False otherwise. The horse moves one point
         horizontally or vertically, and the one point diagonally. It cannot move through a piece
         bloacking its path of movement."""

        # no move has been made
        if from_row == to_row and from_column == to_column:
            return False

        to_coordinates = [to_row, to_column]

        # the horse has at most 8 valid moves listed below, if the coordinates for a move are given,
        # we check for 'hobbling the horses leg', ie the horse cannot pass through another piece
        if to_coordinates == [from_row+1, from_column+2]:
            if board[from_row][from_column+1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row-1, from_column+2]:
            if board[from_row][from_column+1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row + 1, from_column - 2]:
            if board[from_row][from_column - 1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row - 1, from_column - 2]:
            if board[from_row][from_column - 1] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row+2, from_column+1]:
            if board[from_row+1][from_column] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row+2, from_column-1]:
            if board[from_row+1][from_column] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row-2, from_column+1]:
            if board[from_row-1][from_column] != '--':
                return False
            else:
                return True
        elif to_coordinates == [from_row-2, from_column-1]:
            if board[from_row-1][from_column] != '--':
                return False
            else:
                return True
        else:
            return False


game = XiangqiGame()

while game.get_game_state() == 'UNFINISHED':

    print("\n--------------------------------")
    print("Player's turn: ", game.get_turn())
    print("Red is in check? ", game.is_in_check('red'))
    print("Black is in check? ", game.is_in_check('black'))
    print("Game state:", game.get_game_state())
    print("--------------------------------")
    game.display_board()

    print("\n")
    from_move = input("From: ")
    to_move = input("To: ")

    game.make_move(from_move, to_move)

print("GAME OVER")

print("\n--------------------------------")
print("Player's turn: ", game.get_turn())
print("Red is in check? ", game.is_in_check('red'))
print("Black is in check? ", game.is_in_check('black'))
print("Game state:", game.get_game_state())
print("--------------------------------")
game.display_board()


"""
print(
# ************************************* GAME 1 : RED WINS ****************************************
game.make_move('h3', 'e3'),
game.make_move('h8', 'e8'),
game.make_move('i1', 'i2'),
game.make_move('g7', 'g6'),
game.make_move('e3', 'e7'),     # red checks black
game.make_move('e8', 'e4'),
game.make_move('b1', 'c3'),
game.make_move('i7', 'i6'),
game.make_move('c3', 'e4'),
game.make_move('i6', 'i5'),
game.make_move('i4', 'i5'),
game.make_move('i10', 'i7'),
game.make_move('e7', 'e6'),
game.make_move('i7', 'h7'),
game.make_move('h1', 'i3'),
game.make_move('h7', 'h1'),
game.make_move('g1', 'e3'),
game.make_move('h1', 'f1'),     # black checks red
game.make_move('e1', 'f1'),
game.make_move('b8', 'b4'),
game.make_move('e4', 'd6'),
game.make_move('a7', 'a6'),
game.make_move('i2', 'f2'),
game.make_move('b10', 'c8'),
game.make_move('d6', 'e8'),     # red checks black
game.make_move('f10', 'e9'),
game.make_move('b3', 'd3'),
game.make_move('g10', 'e8'),
game.make_move('d3', 'd5'),
game.make_move('b4', 'g4'),
game.make_move('i3', 'g4'),
game.make_move('a6', 'a5'),
game.make_move('c1', 'a3'),
game.make_move('a10', 'b10'),
game.make_move('a10', 'b10'),
game.make_move('d1', 'e2'),
game.make_move('b10', 'b1'),     # black checks red
game.make_move('a1', 'b1'),
game.make_move('a5', 'b5'),
game.make_move('c4', 'c5'),
game.make_move('b5', 'c5'),
game.make_move('b1', 'b4'),
game.make_move('c8', 'a7'),
game.make_move('b4', 'f4'),
game.make_move('a7', 'b5'),
game.make_move('f4', 'f10')     # red checkmates black - RED_WON
)
print("\n--------------------------------")
print("Player's turn: ", game.get_turn())
print("Red is in check? ", game.is_in_check('red'))
print("Black is in check? ", game.is_in_check('black'))
print("Game state:", game.get_game_state())
print("--------------------------------")
game.display_board()
"""


"""
# ************************************* GAME 2 : BLACK WINS ***************************************
game = XiangqiGame()
print(
game.make_move('i4', 'i5'),
game.make_move('b10', 'c8'),    # black
game.make_move('b1', 'c3'),
game.make_move('c8', 'e9'),      # black
game.make_move('c3', 'e2'),
game.make_move('e9', 'f7'),      # black
game.make_move('e2', 'd4'),
game.make_move('f7', 'e9'),      # black
game.make_move('c4', 'c5'),
game.make_move('c7', 'c6'),      # black
game.make_move('d4', 'c6'),
game.make_move('c10', 'e8'),     # black
game.make_move('g1', 'i3'),
game.make_move('e8', 'c6'),      # black
game.make_move('i3', 'g5'),
game.make_move('c6', 'a8'),      # black
game.make_move('g5', 'e3'),
game.make_move('a10', 'a9'),     # black
game.make_move('i1', 'i4'),
game.make_move('a9', 'c9'),      # black
game.make_move('i4', 'h4'),
game.make_move('c9', 'c5'),      # black
game.make_move('h4', 'h8'),
game.make_move('b8', 'b4'),     # black
game.make_move('h3', 'h7'),
game.make_move('e7', 'e6'),      # black
game.make_move('h7', 'h10'),
game.make_move('b4', 'g4'),      # black
game.make_move('i5', 'i6'),
game.make_move('g4', 'g1'),      # black
game.make_move('e1', 'e2'),
game.make_move('i7', 'i6'),      # black
game.make_move('a1', 'a3'),
game.make_move('c5', 'c2')      # black checkmates red - BLACK_WON
)
print("\n--------------------------------")
print("Player's turn: ", game.get_turn())
print("Red is in check? ", game.is_in_check('red'))
print("Black is in check? ", game.is_in_check('black'))
print("Game state:", game.get_game_state())
print("--------------------------------")
game.display_board()
"""


"""
game = XiangqiGame()
# ****************************** GAME 3 : STALE MATE BLACK_WINS ***********************************
game.make_move('a4', 'a5')
game.make_move('a7', 'a6')
game.make_move('c4', 'c5')
game.make_move('c7', 'c6')
game.make_move('e4', 'e5')
game.make_move('e7', 'e6')
game.make_move('g4', 'g5')
game.make_move('g7', 'g6')
game.make_move('i4', 'i5')
game.make_move('a6', 'a5')
game.make_move('i5', 'i6')
game.make_move('c6', 'c5')
game.make_move('i6', 'i7')
game.make_move('e6', 'e5')
game.make_move('i7', 'i8')
game.make_move('g6', 'g5')
game.make_move('a1', 'a5')
game.make_move('a10', 'a5')
game.make_move('b3', 'b5')
game.make_move('b8', 'b1')
game.make_move('i8', 'i9')
game.make_move('i10', 'i9')
game.make_move('f1', 'e2')
game.make_move('a5', 'b5')
game.make_move('h3', 'h10')
game.make_move('i9','i1')
game.make_move('h10', 'f10')
game.make_move('i1', 'h1')
game.make_move('e2', 'd3')
game.make_move('b1', 'd1')
game.make_move('f10', 'd10')
game.make_move('d1', 'g1')
game.make_move('e1', 'd1')
game.make_move('e5', 'e4')
game.make_move('d10', 'd8')
game.make_move('e4', 'e3')
game.make_move('d8', 'e8')
game.make_move('e3', 'd3')
game.make_move('c1', 'e3')
game.make_move('h1', 'h3')
game.make_move('e8', 'e9')
game.make_move('h3', 'e3')
game.make_move('e9', 'e4')
game.make_move('e3', 'e4')      # stalemate no remaining moves for red 

print("\n--------------------------------")
print("Player's turn: ", game.get_turn())
print("Red is in check? ", game.is_in_check('red'))
print("Black is in check? ", game.is_in_check('black'))
print("Game state:", game.get_game_state())
print("--------------------------------")
game.display_board()
"""