# Author: Alex King
# GitHub username: AlexKing16
# Date: 8/17/2023
# Description: Several classes relating to the various parts of chess to be used in a class named ChessVar
# which plays an abstract variant of Chess


class ChessVar:
    """Uses several classes to represent an abstract variant of Chess"""
    def __init__(self):
        self._game_state = "UNFINISHED"
        self._to_move = 'w'
        self._waiting = 'b'
        self._board = Board()
        self._last_move = True
        self._board.print_board()

    def get_game_state(self):
        """Returns the value of the variable self._game_state"""
        return self._game_state

    def check_kings(self):
        """Checks the current row that the king pieces are located in throughout the game and will change the
        self._game_state accordingly"""
        if self._board.get_white_king_row() == 8:
            if self._last_move is True:
                self._last_move = False
                return
            elif self._board.get_black_king_row() != 8:
                self._game_state = 'WHITE_WON'
                print(self._game_state)
            elif self._board.get_black_king_row() == 8:
                self._game_state = 'TIE'
                print(self._game_state)
        elif self._board.get_black_king_row() == 8:
            self._game_state = 'BLACK_WON'
            print(self._game_state)

    def get_board(self):
        """Returns the value of the variable self._board"""
        return self._board

    def get_to_move(self):
        """Returns the value of the variable self._to_move"""
        return self._to_move

    def get_waiting(self):
        """Returns the value of the variable self._waiting"""
        return self._waiting

    @staticmethod
    def check_moves(move_from, move_to):
        """A static method that returns True or False based on if the player entered positions are valid
         positions on the board or not"""
        row_set = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'}
        col_set = {'1', '2', '3', '4', '5', '6', '7', '8'}
        if move_from != move_to:
            if move_from[0] in row_set and move_to[0] in row_set:
                if move_from[1::] in col_set and move_to[1::] in col_set:
                    return True
        return False

    def make_move(self, move_from, move_to):
        """Method to move a piece on the current game's board from its current position to a new position on the
         board. Makes any checks and updates to the game as necessary"""
        if self._game_state != 'UNFINISHED':
            print('The game is over: ' + self.get_game_state())
            return False
        elif self.check_moves(move_from, move_to):
            # check what piece is at the inputted position
            piece = self._board.get_piece(move_from)  # store actual obj of piece
            if self._board.get_piece(move_from) == '___':
                print("No piece at entered spot")
                return False
            # check if piece can be moved
            if piece.token()[0] != self._to_move:
                print('Invalid move! Out of turn order')
                return False
            else:
                # if piece is valid, check if the position it is being moved to is also valid
                pc_at_new_spot = self._board.get_piece(move_to)
                if pc_at_new_spot == '___' or pc_at_new_spot.get_color() == self._waiting:
                    # check if attempted move is valid
                    if piece.valid_movement(move_to, self.get_board()):
                        # update piece pos and board
                        if pc_at_new_spot != '___':
                            pc_at_new_spot.update_pos('0')
                        piece.update_pos(move_to)
                        self._board.update_board(move_from, '___')
                        self._board.update_board(move_to, piece)
                        self._board.print_board()
                        # check positions of kings and change move turn
                        self.check_kings()
                        self._to_move, self._waiting = self._waiting, self._to_move
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False


class ChessPiece:
    """The base class to represent a chess piece for the ChessVar class"""
    def __init__(self, color, current_pos):
        self._color = color
        self._current_pos = current_pos

    def get_color(self):
        """Returns the current value of the variable self._color"""
        return self._color

    def get_current_pos(self):
        """Returns the current value of the variable self._current_pos"""
        return self._current_pos

    def update_pos(self, new_pos):
        """Changes the value of the variable self._current_pos to equal the inputted value represented by new_pos"""
        self._current_pos = new_pos


class King(ChessPiece):
    """An extension of the ChessPiece class. Represents the king piece type for the ChessVar class"""
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self._is_king = True
        self._access_set = set()

    def token(self):
        """Creates the visual for the king piece type on the printed chess board"""
        return str(self._color) + 'ki'

    def is_king(self):
        """Returns the current value of the self._is_king variable"""
        return self._is_king

    def get_access_set(self):
        """Returns the current value of the self._access_set variable"""
        return self._access_set

    def piece_access(self, temp_pos, board, moving_pc_current_pos=None):
        """Checks where on the board a piece has access to based on its movement and position of other pieces
        on the board. Stores valid positions in the self._access_set"""
        row_tup = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        current_col = row_tup.index(temp_pos[0])
        current_row = int(temp_pos[1])
        temp_access_set = set()

        for row in range(current_row - 1, current_row + 2):
            if row <= 0 or row > 8:
                continue

            new_row = str(row)
            for col in range(current_col - 1, current_col + 2):
                if col < 0 or col > 7:
                    continue
                new_col = row_tup[col]
                spot = new_col + new_row
                pc_at_spot = board.get_piece(spot)
                if spot == self._current_pos:
                    continue
                elif spot == moving_pc_current_pos:
                    temp_access_set.add(spot)
                    continue
                elif pc_at_spot == '___':
                    temp_access_set.add(new_col + new_row)
                elif pc_at_spot.get_color() == self._color:
                    continue
                elif pc_at_spot.is_king():
                    return False
        self._access_set = temp_access_set
        return True

    def valid_movement(self, new_pos, board):
        """Checks if moving the king piece type on the board from its current position
         to the inputted new_pos on the board is a valid move"""
        new_pos_state = board.get_piece(new_pos)
        row_tup = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        current_col = row_tup.index(self._current_pos[0])
        new_col = row_tup.index(new_pos[0])

        # check new spot
        if new_pos_state != '___':
            if new_pos_state.get_color() == self._color:
                return False

        # check if row or column is more than one away from current
        if abs(int(new_pos[1]) - int(self._current_pos[1])) <= 1:
            if abs(new_col - current_col) <= 1:

                # KING IN CHECK...CHECK
                if self.piece_access(new_pos, board):
                    if board.all_pc_access(self._current_pos):
                        if self._color == 'w':
                            pc_sets = board.get_black_pcs()
                        else:
                            pc_sets = board.get_white_pcs()
                        for pc in pc_sets:
                            pc_pos = pc.get_current_pos()
                            if pc_pos == '0':
                                continue
                            pc.piece_access(pc.get_current_pos(), board)
                            pc_set = pc.get_access_set()
                            if new_pos in pc_set:
                                return False
                        return True
                    else:
                        return False
        return False


class Rook(ChessPiece):
    """An extension of the ChessPiece class. Represents the rook piece type for the ChessVar class"""
    def __init__(self, color, current_pos):
        super().__init__(color, current_pos)
        self._is_king = False
        self._access_set = set()

    def token(self):
        """Creates the visual for the rook piece type on the printed chess board"""
        return str(self._color) + 'r'

    def is_king(self):
        """Returns the current value of the self._is_king variable"""
        return self._is_king

    def get_access_set(self):
        """Returns the current value of the self._access_set variable"""
        return self._access_set

    def piece_access(self, temp_pos, board, moving_pc_current_pos=None):
        """Checks where on the board a piece has access to based on its movement and position of other pieces
               on the board. Stores valid positions in the self._access_set"""
        row_tup = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        current_row = temp_pos[1]
        current_col = row_tup.index(temp_pos[0])
        temp_access_set = set()

        # Check rest of row this piece is in
        # Right
        for pos in range(current_col + 1, len(row_tup)):
            spot = row_tup[pos] + temp_pos[1]
            pc_at_spot = board.get_piece(spot)
            if pc_at_spot == '___':
                temp_access_set.add(spot)
            if pc_at_spot != '___':
                if spot == moving_pc_current_pos:
                    continue
                if pc_at_spot.get_color() != self._color:
                    if pc_at_spot.is_king():
                        return False
                    else:
                        temp_access_set.add(spot)
                        break
                else:
                    break
        # Left
        for pos_1 in range(current_col - 1, -1, -1):
            spot_1 = row_tup[pos_1] + temp_pos[1]
            pc_at_spot_1 = board.get_piece(spot_1)
            if pc_at_spot_1 == '___':
                temp_access_set.add(spot_1)
            if pc_at_spot_1 != '___':
                if spot_1 == moving_pc_current_pos:
                    continue
                if pc_at_spot_1.get_color() != self._color:
                    if pc_at_spot_1.is_king():
                        return False
                    else:
                        temp_access_set.add(spot_1)
                        break
                else:
                    break

        # Check rest of column this piece is in
        # Up
        for pos_2 in range(int(current_row) + 1, 9):
            spot_2 = temp_pos[0] + str(pos_2)
            pc_at_spot_2 = board.get_piece(spot_2)
            if pc_at_spot_2 == '___':
                temp_access_set.add(spot_2)
            if pc_at_spot_2 != '___':
                if spot_2 == moving_pc_current_pos:
                    continue
                if pc_at_spot_2.get_color() != self._color:
                    temp_access_set.add(spot_2)
                    if pc_at_spot_2.is_king():
                        return False
                else:
                    break
        # Down
        for pos_3 in range(int(current_row) - 1, 0, -1):
            spot_3 = temp_pos[0] + str(pos_3)
            pc_at_spot_3 = board.get_piece(spot_3)
            if pc_at_spot_3 == '___':
                temp_access_set.add(spot_3)

            elif pc_at_spot_3 != '___':
                if spot_3 == moving_pc_current_pos:
                    continue
                if pc_at_spot_3.get_color() != self._color:
                    temp_access_set.add(spot_3)
                    if pc_at_spot_3.is_king():
                        return False
                    else:
                        break
        self._access_set = temp_access_set
        return True

    def valid_movement(self, new_pos, board):
        """Checks if moving the rook piece on the board from its current position
               to the inputted new_pos on the board is a valid move"""
        if self.piece_access(self._current_pos, board):
            if new_pos in self._access_set:
                if self.piece_access(new_pos, board):
                    if board.all_pc_access(self._current_pos):
                        return True
                    else:
                        return False
                return False


class Bishop(ChessPiece):
    """An extension of the ChessPiece class. Represents the bishop piece type for the ChessVar class"""
    def __init__(self, color, current_pos, num):
        super().__init__(color, current_pos)
        self._num = num
        self._is_king = False
        self._access_set = set()

    def token(self):
        """Creates the visual for the bishop piece type on the printed chess board"""
        return str(self._color) + 'b' + self._num

    def is_king(self):
        """Returns the current value of the self._is_king variable"""
        return self._is_king

    def get_access_set(self):
        """Returns the current value of the self._access_set variable"""
        return self._access_set

    def piece_access(self, temp_pos, board, moving_pc_current_pos=None):
        """Checks where on the board a piece has access to based on its movement and position of other pieces
            on the board. Stores valid positions in the self._access_set"""
        row_tup = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        col_tup = (1, 2, 3, 4, 5, 6, 7, 8)
        current_row = int(temp_pos[1])
        current_col = row_tup.index(temp_pos[0])
        temp_access_set = set()

        up_right_list = []
        down_right_list = []
        up_left_list = []
        down_left_list = []
        diagonals_list = [up_right_list, up_left_list, down_right_list, down_left_list]

        for new_diagonal in range(1, 8):
            up = current_row + new_diagonal
            down = current_row - new_diagonal
            left = current_col - new_diagonal
            right = current_col + new_diagonal

            if 0 <= right <= 7 and up in col_tup:
                up_right = str(row_tup[right]) + str(up)
                up_right_list.append(up_right)
            if 0 <= right <= 7 and down in col_tup:
                down_right = str(row_tup[right]) + str(down)
                down_right_list.append(down_right)
            if 0 <= left <= 7 and up in col_tup:
                up_left = str(row_tup[left]) + str(up)
                up_left_list.append(up_left)
            if 0 <= left <= 7 and down in col_tup:
                down_left = str(row_tup[left]) + str(down)
                down_left_list.append(down_left)

        for diagonal in diagonals_list:
            for spot in diagonal:
                pc_at_spot = board.get_piece(spot)
                if pc_at_spot == '___':
                    temp_access_set.add(spot)
                elif pc_at_spot != '___':
                    if spot == moving_pc_current_pos:
                        temp_access_set.add(spot)
                        continue
                    if pc_at_spot.get_color() == self._color:
                        break
                    elif pc_at_spot.is_king():
                        return False
                    else:
                        temp_access_set.add(spot)
                        break
        self._access_set = temp_access_set
        return True

    def valid_movement(self, new_pos, board):
        """Checks if moving the bishop piece on the board from its current position
            to the inputted new_pos on the board is a valid move"""
        if self.piece_access(self._current_pos, board):
            if new_pos in self._access_set:
                if self.piece_access(new_pos, board):
                    if board.all_pc_access(self._current_pos):
                        return True
                    else:
                        return False
                return False


class Knight(ChessPiece):
    """An extension of the ChessPiece class. Represents the knight piece type for the ChessVar class"""
    def __init__(self, color, current_pos, num):
        super().__init__(color, current_pos)
        self._num = num
        self._is_king = False
        self._access_set = set()

    def token(self):
        """Creates the visual for the knight piece type on the printed chess board"""
        return str(self._color) + 'k' + self._num

    def get_access_set(self):
        """Returns the current value of the self._access_set variable"""
        return self._access_set

    def is_king(self):
        """Returns the current value of the self._is_king variable"""
        return self._is_king

    def piece_access(self, temp_pos, board, moving_pc_current_pos=None):
        """Checks where on the board a piece has access to based on its movement and position of other pieces
            on the board. Stores valid positions in the self._access_set"""
        row_tup = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
        current_col = row_tup.index(temp_pos[0])
        current_row = int(temp_pos[1])
        temp_access_set = set()
        temp_access_list = []

        for col in range(current_col - 2, current_col + 3):
            if col < 0 or col == current_col or col > 7:
                continue
            elif col == current_col - 2 or col == current_col + 2:
                if current_row - 1 > 0:
                    temp_access_list.append(str(row_tup[col]) + str(current_row - 1))
                if current_row + 1 < 9:
                    temp_access_list.append(str(row_tup[col]) + str(current_row + 1))
            elif col == current_col - 1 or col == current_col + 1:
                if current_row - 2 > 0:
                    temp_access_list.append(str(row_tup[col]) + str(current_row - 2))
                if current_row + 2 < 9:
                    temp_access_list.append(str(row_tup[col]) + str(current_row + 2))

        for spot in temp_access_list:
            if spot == moving_pc_current_pos:
                temp_access_set.add(spot)
                continue
            pc_at_spot = board.get_piece(spot)
            if pc_at_spot == '___':
                temp_access_set.add(spot)
            elif pc_at_spot.get_color() == self._color:
                continue
            elif pc_at_spot.is_king():
                return False
            else:
                temp_access_set.add(spot)
                continue
        self._access_set = temp_access_set
        return True

    def valid_movement(self, new_pos, board):
        """Checks if moving the knight piece type on the board from its current position
            to the inputted new_pos on the board is a valid move"""
        if self.piece_access(self._current_pos, board):
            if new_pos in self._access_set:
                if self.piece_access(new_pos, board):
                    if board.all_pc_access(self._current_pos):
                        return True
                    else:
                        return False
                return False


class Board:
    """A class to represent a chess board to be used in the Class ChessVar"""
    def __init__(self):
        """Initializes chess piece objects on the chess board in the correct starting positions. Board is represented
        as an array of arrays so each position can be clearly indexed"""
        # WHITE PIECES
        self._wr = Rook('w', 'a2')
        self._wki = King('w', 'a1')
        self._wb1 = Bishop('w', 'b2', '1')
        self._wb2 = Bishop('w', 'b1', '2')
        self._wk1 = Knight('w', 'c2', '1')
        self._wk2 = Knight('w', 'c1', '2')
        # BLACK PIECES
        self._br = Rook('b', 'h2')
        self._bki = King('b', 'h1')
        self._bb1 = Bishop('b', 'g2', '1')
        self._bb2 = Bishop('b', 'g1', '2')
        self._bk1 = Knight('b', 'f2', '1')
        self._bk2 = Knight('b', 'f1', '2')

        self._white_pcs = [self._wr, self._wki, self._wb1, self._wb2, self._wk1, self._wk2]
        self._black_pcs = [self._br, self._bki, self._bb1, self._bb2, self._bk1, self._bk2]
        self._all_pcs = [self._white_pcs, self._black_pcs]

        self._board_state = [
            ['8', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['7', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['6', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['5', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['4', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['3', '___', '___', '___', '___', '___', '___', '___', '___'],
            ['2', self._wr, self._wb1, self._wk1, '___', '___', self._bk1, self._bb1, self._br],
            ['1', self._wki, self._wb2, self._wk2, '___', '___', self._bk2, self._bb2, self._bki],
            ['', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ]

        self._col_dict = {
            'a': 1,
            'b': 2,
            'c': 3,
            'd': 4,
            'e': 5,
            'f': 6,
            'g': 7,
            'h': 8
        }

    def get_board_state(self):
        """Returns the current value of the self._board_state """
        return self._board_state

    def get_white_king_row(self):
        """Returns the row that the white king is currently located at on the board"""
        return int(self._wki.get_current_pos()[1])

    def get_black_king_row(self):
        """Returns the row that the black king is currently located at on the board"""
        return int(self._bki.get_current_pos()[1])

    def get_white_pcs(self):
        """Returns self._white_pcs, which is an array that holds all the white piece objects"""
        return self._white_pcs

    def get_black_pcs(self):
        """Returns self._black_pcs, which is an array that holds all the white piece objects"""
        return self._black_pcs

    def get_all_pcs(self):
        """Returns self._all_pcs, which is an array that holds the self._white_pcs and self._black_pcs arrays"""
        return self._all_pcs

    def get_piece(self, pos):
        """Returns the chess piece currently located at the inputted position on the board"""
        col = self._col_dict[pos[0]]
        row = 8 - int(pos[1])
        return self._board_state[row][col]

    def update_board(self, pos, update):
        """Updates the board based on new positions of chess pieces during gameplay"""
        col = self._col_dict[pos[0]]
        row = 8 - int(pos[1])
        self._board_state[row][col] = update

    def print_board(self):
        """Prints a visual representation of the current state of the board during gameplay. Only for visualization
        purposes"""
        for row in range(0, len(self._board_state) - 1):
            for index, col in enumerate(self._board_state[row]):
                if index == 8:
                    if col == '___':
                        print(col)
                    else:
                        print(col.token())
                elif index == 0 or col == '___':
                    print(col, end=' ')
                else:
                    print(col.token(), end=' ')
        for letter in self._board_state[8]:
            print(letter, end='   ')
            if letter == 'h':
                print()
                print()
                print('------------------------------------------------------')
                print()

    def all_pc_access(self, moving_pc_current_pos):
        """Runs the piece_access method on every piece on the board to check if the movement of a piece would
        result in either team's king being put in check. Returns True or False based on if a king would be subjected
        to check or not"""
        for pc_list in self._all_pcs:
            for piece in pc_list:
                pc_pos = piece.get_current_pos()
                if pc_pos == '0':
                    continue
                if piece.piece_access(pc_pos, self, moving_pc_current_pos):
                    continue
                else:
                    return False
        return True
