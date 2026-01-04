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
        self.log = []
        self.highlights = []
        self.check = 0
    
    def reset_board(self): # resets the board only
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

    def is_safe(self, square):
        return True
    
    # check if the line BETWEEN two squares is clear
    def is_line_clear(self, first, second): # redo
        # square = col, row
        if first[0] == second[0]:
            step_col = 0
        else:
            # -1 indicates that the piece is moving to the left, to vertical line "a"
            step_col = 1 if second[0] > first[0] else -1
        
        if first[1] == second[1]:
            step_row = 0
        else:
            # -1 indicates that the piece is moving up to the 8th horizontal line
            step_row = 1 if second[1] > first[1] else -1

        start_row = first[1] + step_row
        start_col = first[0] + step_col

        while (start_row, start_col) != (second[1], second[0]):
            if self.board[start_row][start_col]:
                return False
            start_col += step_col
            start_row += step_row
        return True

    def enemy_present(self, square):
        # square = col, row
        enemy = {-1: "b", 1: "w"}
        return self.board[square[1]][square[0]] and self.board[square[1]][square[0]][0] == enemy[self.turn]
    
    # might be better to add "double step" mark in log to check if the last move was a double step. Leave it for now
    def en_passant(self, color, target_col, target_row): 
        #needed = f'{color}p {self.coords[target_col]}{8 - target_row}'
        if self.log and self.log[-1] == f'{color}p {self.coords[target_col]}{8 - target_row}':
            if not f'{color}p {self.coords[target_col]}{8 - target_row - self.turn}' in self.log:
                print(target_col, target_row)
                self.board[target_row][target_col] = ""
                return True
        return False
        
    def legal(self, first, second, piece):  # impement validation here
        print(self.log)
        # check if the right piece was selected 
        color = {-1: "w", 1: "b"}
        if piece[0] != color[self.turn]:
            print("Not your turn idiot")
            return False
        row_dif = abs(second[1] - first[1])
        col_dif = abs(second[0] - first[0])

        # knights
        if piece[1] == "n":
            pass
        
        # pawns
        if piece[1] == "p":
            print(self.turn)
            # check if the user is trying to move a pawn backwards
            if second[1] - first[1] != row_dif * self.turn:
                print("You can't move a pawn backwards idiot")
                return False
            
            # moving forward
            if not col_dif:
                # return False if the user is trying to move the pawn more than 2 squares ahead, 2 squares not from the start or something is on the target square
                if any((row_dif > 2, (row_dif == 2 and first[1] not in (6, 1)), self.board[second[1]][second[0]])):
                    return False
                # is_line_clear checks up to and including the last square but we just checked it above so we don't have to worry about it
                return self.is_line_clear(first, second)
            
            # taking horizontally
            if row_dif == 1 and col_dif == 1:
                # fix the hardcoding later
                if self.enemy_present(second):
                    return True
                # check for an en passant
                return self.en_passant(color[self.turn - (2 * self.turn)], second[0], first[1])

        # rooks    
        elif piece[1] == "r": 
            if row_dif and col_dif:
                return False
            return self.is_line_clear(first, second)
        # bishops
        elif piece[1] == "b":
            if row_dif != col_dif:
                return False
            return self.is_line_clear(first, second)

        # queens
        elif piece[1] == "q":
            # check if a move is in a straight line
            if row_dif == 0 or col_dif == 0 or row_dif == col_dif:
                return self.is_line_clear(first, second)
        
        # kings
        elif piece[1] == "k":
            if row_dif <= 1 and col_dif <= 1:
                return self.is_safe(second)
        return False
        
    def make_move(self, clicks):
        # first = clicks[0]
        # second = clicks[1]
        moving_piece = self.board[clicks[0][1]][clicks[0][0]]
        # return false if the target square contains a piece of the same color as the first square
        if self.board[clicks[1][1]][clicks[1][0]] and self.board[clicks[1][1]][clicks[1][0]][0] == moving_piece[0]:
            return False
        if self.legal(clicks[0], clicks[1], moving_piece): # check if the move is legal
            self.board[clicks[0][1]][clicks[0][0]] = ""    
            self.board[clicks[1][1]][clicks[1][0]] = moving_piece
            self.log.append(f'{moving_piece} {self.coords[clicks[1][0]]}{8 - clicks[1][1]}') # append the move to the log
            self.turn *= -1
            return True
        return False
    


# to do next:
# finish move validation
# implement checks
# implement is_safe function
# implement checkmates