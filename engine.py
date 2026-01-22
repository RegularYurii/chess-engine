class engine():
    def __init__(self):
        self.turn = -1 # turn -1 -> white to move
        self.coords = ["a", "b", "c", "d", "e", "f", "g", "h"]
        self.board = [
                        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], 
                        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]
        #board[row][col]
        # -1 represents the white's king, 1 - black's
        self.kings = {-1: (7, 4), 1: (0, 4)}
        self.log = [] # change log format + en passant checker
        self.highlights = []
        self.check = False
        self.color = {-1: "w", 1: "b"}    

    def reset_board(self): # resets the board only, maybe combine with restart function
        self.board = [
                        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], 
                        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

    def restart(self):
        self.log = []
        self.highlights = []
        self.reset_board()
        self.turn = -1
        self.check = False
        self.kings = {-1: (7, 4), 1: (0, 4)}

    def make_move(self, clicks):
        moving_piece = self.board[clicks[0][0]][clicks[0][1]]
        target_piece = self.board[clicks[1][0]][clicks[1][1]]
        king_sq = self.kings[self.turn]

        # return false if the target square contains a piece of the same color as the first square
        if self.is_ally(moving_piece, target_piece):
            return False
        
        #  check if the move is legal, and if so first make the move and check if the king is safe, if not undo the move
        if self.is_legal(clicks[0], clicks[1], moving_piece):
            # empty the square the piece moves from
            self.place_piece(clicks[0])
            # place the piece at the target square
            self.place_piece(clicks[1], moving_piece)
            # if a king was moved update its position
            if moving_piece[1] == "k":
                self.kings[self.turn] = clicks[1]

            # make sure there's no check when the piece is moved
            if not self.is_attacked(self.kings[self.turn]):
                self.add_to_log(clicks[0], clicks[1], moving_piece)
                self.turn *= -1
                # add cache maybe                     change self.kings(kings' positions) and self.turn
                self.check = self.is_attacked(self.kings[self.turn])
                print("Is check -", self.check)
                return True
            # if the move results in checking yourself place the moving piece back
            last_move = self.log[-1].split(" ")
            if last_move[-1] == "double":
                self.board[8-4][clicks[1][1]] = f'{self.color[-self.turn]}p'
                
            self.place_piece(clicks[1], target_piece)
            self.place_piece(clicks[0], moving_piece)
            self.kings[self.turn] = king_sq
        return False
    
    # it's a separate method because the a move can be a castle, or a double pawn move. maybe implement taking moves as well
    def add_to_log(self, moving_from, moving_to, moving_piece):
        type = "" # type of the move (double pawn move, castling)
        from_row = moving_from[0]
        #from_col = moving_from[1]
        to_row = moving_to[0]
        to_col = moving_to[1]
        if moving_piece[1] == "p" and abs(to_row - from_row) == 2:
            type = "double" 
        self.log.append(f'{moving_piece} {self.coords[to_col]}{8 - to_row} {type}') # append the move to the log

    def place_piece(self, square, piece=""):
        row = square[0]
        col = square[1]
        self.board[row][col] = piece

    def piece_color(self, piece):
        if piece:
            return piece[0]
        return False
    
    def is_ally(self, first, second):
        return self.piece_color(first) == self.piece_color(second)
    
    def is_legal(self, first, second, piece):  # impement validation here, shorten it somehow
        row_dif = abs(second[0] - first[0])
        col_dif = abs(second[1] - first[1])
        if piece[1] == "p":
            return self.is_legal_pawn(first, second, row_dif, col_dif)
        elif piece[1] == "n":
            return self.is_legal_knight(first, second, row_dif, col_dif)
        elif piece[1] == "r": 
            return self.is_legal_rook(first, second, row_dif, col_dif)
        elif piece[1] == "b":
            return self.is_legal_bishop(first, second, row_dif, col_dif)
        elif piece[1] == "q":
            return self.is_legal_queen(first, second, row_dif, col_dif)
        elif piece[1] == "k":
            return self.is_legal_king(second, row_dif, col_dif)

    def is_legal_knight(self, first, second, row_dif, col_dif):
        return ((col_dif == 1 and row_dif == 2) or (row_dif == 1 and col_dif == 2))
    
    def is_legal_pawn(self, first, second, row_dif, col_dif):
        # check if the user is trying to move a pawn backwards
        if second[0] - first[0] != row_dif * self.turn:
            return False
        
        # moving forward
        if not col_dif:
            # return False if the user is trying to move the pawn more than 2 squares ahead, 2 squares not from the start or something is on the target square
            # make every piece(or at least rooks, pawns, and kings) an object of a class "piece" having an attribute "moved"
            if any((row_dif > 2, (row_dif == 2 and first[0] not in (6, 1)), self.board[second[0]][second[1]])):
                return False
            # is_line_clear checks up to and including the last square but we just checked it above so we don't have to worry about it
            return self.is_line_clear(first, second)
        
        # taking horizontally
        if row_dif == 1 and col_dif == 1:
            # fix the hardcoding
            if self.enemy_present(second):
                return True
            # check for an en passant
            return self.en_passant(second[1], first[0])

    def is_legal_rook(self, first, second, row_dif, col_dif):
        if row_dif and col_dif:
            return False
        return self.is_line_clear(first, second)
    
    def is_legal_bishop(self, first, second, row_dif, col_dif):
        if row_dif != col_dif:
            return False
        return self.is_line_clear(first, second)
    
    def is_legal_queen(self, first, second, row_dif, col_dif):
        # check if a move is in a straight line
        if row_dif == 0 or col_dif == 0 or row_dif == col_dif:
            return self.is_line_clear(first, second)
        return False
    
    def is_legal_king(self, second, row_dif, col_dif):
        return row_dif <= 1 and col_dif <= 1 and not self.is_attacked(second)

    def is_attacked(self, square):
        return bool(self.attacked_from(square))
        
    # returns the squares the given square is attacked from
    def attacked_from(self, square): # optimise later
        # check if enemy's king is ajdacent to the square or if non king piece is attacking the square
        attacking_squares = []
        attacking_squares += (self.attacked_by_non_king_from(square))
        attacking_squares += (self.attacked_by_king(square))
        #print(attacking_squares)

        return attacking_squares

        
    
    def attacked_by_non_king_from(self, square):
        attacking_squares = []
        # check if the square is on an attacked line
        attacking_squares += (self.attacked_by_q_r_b_from(square))

        # check if the square is attacked by a knight
        attacking_squares += (self.attacked_by_knight_from(square))
        
        # check if a pawn is attacking
        attacking_squares += (self.attacked_by_pawn_from(square))
        
        return attacking_squares

        
    def attacked_by_knight_from(self, square):
        attacking_squares = []
        directions = [(-2, -1), (-2, 1),(-1, -2),(-1, 2),
                    (2, -1), (2, 1), (1, 2),(1, -2)]
        for d in directions:
            row = square[0] + d[0]
            col = square[1] + d[1]                                                                                          # fix the hardcoding
            if (row >= 0) and (row <= 7) and (col >= 0) and (col <= 7) and self.board[row][col] and self.board[row][col] == f'{self.color[-self.turn]}n':
                attacking_squares.append((row, col))
        return attacking_squares
    
    def attacked_by_q_r_b_from(self, square):
        attacking_squares = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), # (col, row) changes when checking horizontal & vertical lines
                    (-1, 1), (1, 1), (-1, -1), (1, -1)] # (col, row) changes when checking diagonals
        for d in directions:
            row = square[0] + d[0]
            col = square[1] + d[1]
            while (row >= 0) and (row <= 7) and (col >= 0) and (col <= 7):
                if self.board[row][col]:
                    piece = self.board[row][col]
                    if piece[0] == self.color[self.turn]: # break if the met piece is of the same color
                        break
                    if (row == square[0] or col == square[1]):
                        if piece[1] in "qr": # return if on the same line but the met piece is not a rook or a queen
                            attacking_squares.append((row, col))
                        break
                    if abs(row - square[0]) == abs(col - square[1]):
                        if piece[1] in "bq":
                            attacking_squares.append((row, col))
                        break
                row += d[0]
                col += d[1]
        return attacking_squares

    def attacked_by_pawn_from(self, square): # fix
        attacking_squares = []
        directions = [(-1, -1),(-1, 1),(1, -1),(1, 1)]
        for d in directions:
            row = square[0] - d[0]
            col = square[1] - d[1]                                                                # d[0] == -self.turn if a pawn is attacking in the right direction 
            if (row >= 0) and (row <= 7) and (col >= 0) and (col <= 7) and self.board[row][col] and d[0] == -self.turn and self.board[row][col] == f'{self.color[-self.turn]}p':
                attacking_squares.append((row, col))
        return attacking_squares
    
    def attacked_by_king(self, square):
        attacking_squares = []
        row_dif = abs(self.kings[-self.turn][0] - square[0])
        col_dif = abs(self.kings[-self.turn][1] - square[1])
        if row_dif <= 1 and col_dif <= 1:
            attacking_squares.append((self.kings[-self.turn][0], self.kings[-self.turn][1]))
        return attacking_squares



    # check if the line BETWEEN two squares is clear
    def is_line_clear(self, first, second): # redo
        if first[1] == second[1]:
            step_col = 0
        else:
            # -1 indicates that the piece is moving to the left, to vertical line "a"
            step_col = 1 if second[1] > first[1] else -1
        
        if first[0] == second[0]:
            step_row = 0
        else:
            # -1 indicates that the piece is moving up to the 8th horizontal line
            step_row = 1 if second[0] > first[0] else -1

        start_row = first[0] + step_row
        start_col = first[1] + step_col

        while (start_row, start_col) != (second[0], second[1]):
            if self.board[start_row][start_col]:
                return False
            start_col += step_col
            start_row += step_row
        return True

    def enemy_present(self, square):
        # square = row, col
        return self.board[square[0]][square[1]] and self.board[square[0]][square[1]][0] == self.color[-self.turn]
    
    def en_passant(self, target_col, target_row): 
        if self.log:
            last_move = self.log[-1].split(" ")
            # no point to check who made the last move because it's impossible to make 2 moves in a row
            if last_move[2] == "double" and last_move[1] ==  f'{self.coords[target_col]}{8 - target_row}':
                # change it so en_passant doesn't make moves on the board
                self.board[target_row][target_col] = ""
                return True
        return False
        
    def is_stalemate(self):
        return 0

    def is_checkmate(self):
        if not self.check:
            return False
        attacking_squares = self.attacked_from(self.kings[self.turn])
        # check if it's a double check
        if len(attacking_squares) > 1:
            # return king_can_escape (if can't it's a checkmate)
            return False
        attacking_piece = self.board[attacking_squares[0][0]][attacking_squares[0][1]]
        if self.can_be_taken(attacking_squares[0][0], attacking_squares[0][1], attacking_piece):
            return False
        # elif can_be_blocked
        # elif king_can_escape
        return False
    
    def can_be_taken(self, row, col, attacking_piece):
        # check if getting rid of the attacking piece saves from a check (we can't simply pu "" because it might be a battery of rooks)
        if attacking_piece[1] == "n":
            self.board[row][col] = f'{attacking_piece[0]}q'
        else:
            self.board[row][col] = f'{attacking_piece[0]}n'
        # if capturing saves from a check, make sure it is possible to take the piece, otherwise return False
        should_be_taken = not self.is_attacked(self.kings[self.turn])
        self.board[row][col] = attacking_piece
        if should_be_taken:
            #print(self.attacked_by_non_king_from(attacking_square), self.attacked_by_king(attacking_square))
            # maybe pass self.turn to the functions
            self.turn *= -1
            can_take = bool(self.attacked_by_non_king_from((row, col)) or self.attacked_by_king((row, col)))
            self.turn *= -1
            if can_take:
                return True
        return False

# to do next:
# implement checkmates
# implement castling (and its validation)

# figure out how to get rid of "undo move" logic, and fix the board mutations

# get rid of or change the piece_color
# fix the confusing attacked_from etc functions
# optimise, make the functions shorter
# 

# add caching
        
# implement no-draw and chess tic tac toe
