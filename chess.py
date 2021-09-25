def game():

    board = [[None for x in range(8)] for y in range(8)]
    players = dict()

    class PlayingPiece(object):
        def __init__(self, row, col, team):
            self.row = row
            self.col = col
            self.team = team
            self.name = self.__class__.__name__
        
        def move(self, i, j):
            if (i, j) in self.get_attackable():
                board[self.row][self.col] = None
                self.row, self.col = i, j
                if board[i][j] != None:
                    players[not self.team].rem(board[i][j])
                board[i][j] = self
                return True
            return False

        def valid_coord(self, i, j):
            return 0 <= i < 8 and 0 <= j < 8

        def __str__(self):
            color = "W" if self.team else "B"
            if self.name == "Knight":
                piece = "N"
            else:
                piece = self.name[0]
            return f"{color}{piece}"
        
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
            cols = {"a":0, "b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
            inp = input("start? ")
            start_row, start_col = inp[1], inp[0].lower()
            start_row = 8 - int(start_row)
            start_col = cols[start_col]
            piece = board[start_row][start_col]
            while piece == None or not piece.valid_coord(start_row, start_col) or board[start_row][start_col] not in self.pieces:
                print("NOT VALID. TRY AGAIN")
                inp = input("start? ")
                start_row, start_col = inp[1], inp[0].lower()
                start_row = 8 - int(start_row)
                start_col = cols[start_col]
                piece = board[start_row][start_col]

            inp2 = input("end? ")
            end_row, end_col = inp2[1], inp2[0].lower()
            end_row = 8 - int(end_row)
            end_col = cols[end_col]

            while not piece.move(end_row, end_col):
                print("NOT VALID. TRY AGAIN")
                inp2 = input("end? ")
                end_row, end_col = inp2[1], inp2[0].lower()
                end_row = 8 - int(end_row)
                end_col = cols[end_col]

    class King(PlayingPiece):

        def get_surrounding(self):
            li = list()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    if self.valid_coord(self.row+i, self.col+j):
                        li.append((self.row+i, self.col+j))
            return li

        def get_attackable(self):
            attack = list()
            invalid = list()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    cur_row = self.row + i
                    cur_col = self.col + j
                    if self.valid_coord(cur_row, cur_col) and (board[cur_row][cur_col] == None or board[cur_row][cur_col].team != self.team):
                        for piece in players[not self.team].pieces:
                            if piece.name == "King":
                                invalid = piece.get_surrounding()
                            elif piece.name == "Pawn":
                                temp = board[cur_row][cur_col]
                                board[cur_row][cur_col] = self
                                attackable = True if (cur_row, cur_col) in piece.get_attackable() else False
                                board[cur_row][cur_col] = temp
                                if attackable:
                                    break
                            elif (cur_row, cur_col) in piece.get_attackable():
                                break
                        else:
                            attack.append((cur_row, cur_col))
            attack = [x for x in attack if x not in invalid]
            return attack


    class Bishop(PlayingPiece):
        def get_attackable(self):
            return self.bish_attack()

        def bish_attack(self):
            attack = list()
            moves = [(1,1), (1,-1), (-1,-1), (-1,1)]
            for move in moves:
                cur_row = self.row + move[0]
                cur_col = self.col + move[1]
                while self.valid_coord(cur_row, cur_col) and board[cur_row][cur_col] == None:
                    attack.append((cur_row, cur_col))
                    cur_row += move[0]
                    cur_col += move[1]
                if self.valid_coord(cur_row, cur_col) and board[cur_row][cur_col].team != self.team:
                    attack.append((cur_row, cur_col))
            return attack


        
    
    class Rook(PlayingPiece):

        def get_attackable(self):
            return self.rook_attack()

        def rook_attack(self):
            attack = list()
            moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            for move in moves:
                cur_row = self.row + move[0]
                cur_col = self.col + move[1]
                while self.valid_coord(cur_row, cur_col) and board[cur_row][cur_col] == None:
                    attack.append((cur_row, cur_col))
                    cur_row += move[0]
                    cur_col += move[1]
                if self.valid_coord(cur_row, cur_col) and board[cur_row][cur_col].team != self.team:
                    attack.append((cur_row, cur_col))
            return attack
            
            
    
    class Queen(Bishop, Rook):
        def get_attackable(self):
            return self.rook_attack() + self.bish_attack()

    class Knight(PlayingPiece):
        def get_attackable(self):
            moves = [(2,1),(1,2),(-1,-2),(-2,-1),(1,-2),(2,-1),(-1,2),(-2,1)]
            attack = list()
            for move in moves:
                cur_row = self.row + move[0]
                cur_col = self.col + move[1]
                if self.valid_coord(cur_row, cur_col) and (board[cur_row][cur_col] == None or board[cur_row][cur_col].team != self.team):
                    attack.append((cur_row, cur_col))
            return attack
    
    class Pawn(PlayingPiece):
        def __init__(self, row, col, team):
            self.row = row
            self.col = col
            self.team = team
            self.moved = False
            self.name = "Pawn"

        def move(self, i, j):
            valid = super().move(i, j)
            if valid:
                self.moved = True
            return valid

        def get_attackable(self):
            attack = list()
            row_dir = -1 if self.team else 1
            if not self.moved:
                r = self.row + (row_dir * 2)
                if board[r][self.col] == None:
                    attack.append((r, self.col))
            r = self.row + row_dir
            if self.valid_coord(r, self.col) and board[r][self.col] == None:
                attack.append((r, self.col))
            if self.valid_coord(r, self.col - 1) and board[r][self.col - 1] != None and board[r][self.col - 1].team != self.team:
                attack.append((r, self.col - 1))
            if self.valid_coord(r, self.col + 1) and board[r][self.col + 1] != None and board[r][self.col + 1].team != self.team:
                attack.append((r, self.col + 1))
            return attack


    def print_board():
        s = "-" * 41
        s = "  " + s
        print(s)
        for i in range(8):
            row = board[i]

            s = "{} |".format(8-i)
            for x in row:
                if x:
                    s += " {} ".format(x)
                else:
                    s += "    "
                s += "|"
            print(s)
            s = "-" * 41
            s = "  " + s
            print(s)
        space = "    "
        s = f"{space}A{space}B{space}C{space}D{space}E{space}F{space}G{space}H"
        print(s)
    
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