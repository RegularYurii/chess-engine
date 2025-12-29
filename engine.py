class engine():
    def __init__(self):
        self.turn = 0 # turn 0 - white to move
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
        self.log = []
        self.highlights = []
    
    def reset(self): # resets the board only
        self.board = [
                        ["br", "bn", "bb", "bq", "bk", "bb", "bn", "br"],
                        ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        [ "",   "",   "",   "",   "",   "",   "",   ""], 
                        [ "",   "",   "",   "",   "",   "",   "",   ""],
                        ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"], 
                        ["wr", "wn", "wb", "wq", "wk", "wb", "wn", "wr"]]

    def legal(self, first, second):
        pass # impement validation here

    def make_move(self, clicks): # make a change such that when first is empty the moving_piece becomes second
        first = clicks[0]
        second = clicks[1]
        moving_piece = self.board[clicks[0][1]][clicks[0][0]]
        if moving_piece: # check if the move is legal
            self.board[clicks[0][1]][clicks[0][0]] = ""    
            self.board[clicks[1][1]][clicks[1][0]] = moving_piece
            self.log.append(f'{moving_piece} {self.coords[clicks[1][0]]}{8 - clicks[1][1]}') # append the move to the log
        #print(self.log)