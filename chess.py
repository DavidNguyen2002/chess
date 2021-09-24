def game():

    board = [[None for x in range(8)] for y in range(8)]
    players = dict()

    class PlayingPiece(object):
        def __init__(self, row, col, team):
            self.row = row
            self.col = col
            self.team = team
        
        def move(self, i, j):
            if self.can_attack(i, j):
                board[self.row][self.col] = None
                self.row, self.col = i, j
                if board[i][j] != None:
                    players[not self.team].rem(board[i][j])
                board[i][j] = self
                return True
            return False
        
        def __str__(self):
            # make board prettier
            color = "W" if self.team else "B"
            if self.__class__.__name__ == "Knight":
                piece = "N"
            else:
                piece = str(self.__class__.__name__)[0]
            return "{}{}".format(color, piece)
        
        def __repr__(self):
            return self.__str__()

    class Player(object):
        def __init__(self, color):
            self.pieces = list()
            if color == "w":
                self.pieces.append(King(7, 4, True))
                self.pieces.append(Queen(7, 3, True))
                self.pieces.append(Bishop(7, 2, True))
                self.pieces.append(Bishop(7, 5, True))
                self.pieces.append(Knight(7, 1, True))
                self.pieces.append(Knight(7, 6, True))
                self.pieces.append(Rook(7, 0, True))
                self.pieces.append(Rook(7, 7, True))
                for i in range(8):
                    self.pieces.append(Pawn(6, i, True))
            else:
                self.pieces.append(King(0, 4, False))
                self.pieces.append(Queen(0, 3, False))
                self.pieces.append(Bishop(0, 2, False))
                self.pieces.append(Bishop(0, 5, False))
                self.pieces.append(Knight(0, 1, False))
                self.pieces.append(Knight(0, 6, False))
                self.pieces.append(Rook(0, 0, False))
                self.pieces.append(Rook(0, 7, False))
                for i in range(8):
                    self.pieces.append(Pawn(1, i, False))
            for piece in self.pieces:
                board[piece.row][piece.col] = piece
            self.color = True if color == "w" else False
            players[self.color] = self
        
        def rem(self, piece):
            self.pieces.remove(piece)
        
        def turn(self):
            inp = input("start? ").split(",")
            start_row, start_col = inp[0], inp[1]
            start_row = int(start_row)
            start_col = int(start_col)
            inp2 = input("end? ").split(",")
            end_row, end_col = inp2[0], inp2[1]
            end_row = int(end_row)
            end_col = int(end_col)
            # Fix this input later
            piece = board[start_row][start_col]
            # check if this piece belongs to player

            piece.move(end_row, end_col)


    class King(PlayingPiece):
        def check(self, other):
            for piece in other.pieces:
                if piece.can_attack(self.row, self.col):
                    return True
            return False
        
        def can_attack(self, i, j):
            if (abs(i-self.row) > 1 or abs(j-self.col) > 1) or self.row == self.col:
                return False
            if i < 0 or i >= 8 or j < 0 or j >= 8:
                return False
            if self.row == i and self.col == j:
                return False
            return board[i][j] == None or board[i][j].team != self.team
        
        def move(self, i, j):
            self.row, self.col = i, j

    class Bishop(PlayingPiece):
        def can_attack(self, i, j):
            return self.bish_attack(i, j)

        def bish_attack(self, i, j):
            row, col = self.row, self.col
            if i-row != j-col:
                return False
            if row == i and col == j:
                return False
            x = -1 if i > row else 1
            y = -1 if j > col else 1
            while i + x != row:
                i += x
                j += y
                if board[i][j] != None:
                    return False
            i += x
            j += y
            return board[i][j] == None or board[i][j].team != self.team
        
    
    class Rook(PlayingPiece):
        def can_attack(self, i, j):
            return self.rook_attack(i ,j)
        
        def rook_attack(self, i , j):
            row = self.row
            col = self.col
            if row != i and col != j:
                return False
            if row == i and col == j:
                return False
            if row == i:
                y = -1 if j > col else 1
                while j + y != col:
                    j += y
                    if board[row][j] != None:
                        return False
                j += y
                return board[row][j] == None or board[row][j].team != self.team
            else:
                x = -1 if i > row else 1
                while i + x != row:
                    i += x
                    if board[x][col] != None:
                        return False
                i += x
                return board[i][col] == None or board[i][col].team != self.team
            
            
    
    class Queen(Bishop, Rook):
        def can_attack(self, i, j):
            return self.rook_attack(i, j) or self.bishop_attack(i, j)

    class Knight(PlayingPiece):
        def can_attack(self, i, j):
            if i < 0 or i >= 8 or j < 0 or j >= 8:
                return False
            if self.row == i and self.col == j:
                return False
            x = abs(self.row - i)
            y = abs(self.col - j)
            if (x == 2 or x == 1) and (y == 2 or y == 1):
                return x != y and (board[i][j] == None or board[i][j].team != self.team)
            return False
    
    class Pawn(PlayingPiece):
        def __init__(self, row, col, team):
            self.row = row
            self.col = col
            self.team = team
            self.moved = False
        
        def can_attack(self, i, j):
            if i < 0 or i >= 8 or j < 0 or j >= 8:
                return False
            if self.row == i and self.col == j:
                return False
            if abs(self.col-j) > 1:
                return False
            if self.col - j == 0:
                if self.team:
                    if i > self.row:
                        return False
                    if (self.moved and i < self.row - 1) or (not self.moved and i < self.row - 2):
                        return False
                else:
                    if i < self.row:
                        return False
                    if (self.moved and i > self.row + 1) or (not self.moved and i > self.row + 2):
                        return False
                return board[i][j] == None
            else:
                return board[i][j].team != self.team

    def print_board():
        for row in board:
            print(row)
    
    def play():
        p1 = Player("w")
        p2 = Player("b")
        
        while True:
            #Fix turns 
            print_board()
            p1.turn()
            print_board()
            p2.turn()
        
    play()
game()