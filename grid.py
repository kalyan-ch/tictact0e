import pygame, copy

class TicToe(object):
    
    def __init__(self, width, height, fps, n):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        pygame.mixer.music.load('data/music.mp3')

        self.logo = pygame.image.load('data/logo.png')
        self.logo = pygame.transform.scale(self.logo, (60, 60))
        self.winimg = pygame.image.load('data/you_win.gif')
        self.loseimg = pygame.image.load('data/you_lose.GIF')
        self.font = pygame.font.SysFont("Georgia", 30)
        self.title = self.font.render("TIC TAC TOE", 1, (0, 179, 179))
        self.width = width
        self.height = height
        self.gridW = int(self.width) - 40
        self.gridH = int(self.width) - 200
        self.xOffset = 20
        self.yOffset = 100
        self.n = n
        self.board = [[0 for x in range(n)] for x in range(n)]
        self.fps = fps
        self.winimg = pygame.transform.scale(self.winimg, (self.gridW, self.gridH))
        self.loseimg = pygame.transform.scale(self.loseimg, (self.gridW, self.gridH))
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.DOUBLEBUF)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill((204, 204, 204))
        self.fps = fps
        self.gridArea = pygame.draw.rect(self.bg, (255,255,255), (self.xOffset,self.yOffset,self.gridW, self.gridH))
        self.is_game_over = False
        self.winner = 0
        self.draw_lines()

        pygame.mixer.music.play(-1,0.0)
        self.screen.blit(self.bg, (0,0))
        


    def run(self):
        running = True
        
        while running:
            self.screen.blit(self.logo,(20,10))
            self.screen.blit(self.title, (90,20))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    if event.button == 1:
                        if not self.is_game_over:
                            self.movePlayer(mousepos)
                            self.moveAI()
                            
                            for x in self.board:
                                for y in x:
                                    print y,
                                print ""

                            print ""
                            
            pygame.display.flip()

        pygame.quit()

    def draw_lines(self):
        w = self.gridW
        h = self.gridH + 100
        n = self.n
        xO = self.xOffset
        yO = self.yOffset
        for x in range(1,n):
            pygame.draw.line(self.bg, (0,0,0), (x*w/n+xO, yO), (x*w/n+xO, h), 3)
            pygame.draw.line(self.bg, (0,0,0), (xO, x*(h-yO)/n+yO), (w+xO, x*(h-yO)/n+yO), 3)
    
    def movePlayer(self, mousepos):
        x = mousepos[0]
        y = mousepos[1]
        
        wThres = self.gridW/self.n
        hThres = self.gridH/self.n
        a = (x-self.xOffset)/wThres
        b = (y-self.yOffset)/hThres
        
        if a >= 0 and b >= 0 and self.board[b][a] != 1:
            self.board[b][a] = 1
            pygame.draw.rect(self.bg, (45,226,114), ((a*wThres)+self.xOffset, (b*hThres)+self.yOffset, wThres,hThres ))
            self.screen.blit(self.bg, (0,0))
            self.checkWin()

    def playTemp(self,board, row, col, player):
        board[row][col]=player

    def unPlayTemp(self,board, row, col):
        board[row][col]=0

    def moveAI(self):
        board = copy.deepcopy(self.board)
        if self.psblMvs(board):
            best_move = self.minimax(board, 2)
            (row, col) = best_move
            self.board[row][col] = 2
            wThres = self.gridW/self.n
            hThres = self.gridH/self.n
            pygame.draw.rect(self.bg, (150,18,59), ((col*wThres)+self.xOffset, (row*hThres)+self.yOffset, wThres,hThres ))
            self.screen.blit(self.bg, (0,0))
            self.checkWin()

    def minimax(self, board, plyr):
        maxi = -100
        action = ()
        psbl_mvs = self.psblMvs(board)
        plyr1 = 1
        if plyr == 1:
            plyr1 = 2
        
        for move in psbl_mvs:
            (row, col) = move
            self.playTemp(board,row,col,plyr)
            val = self.min_val(board, plyr1, -100, 100, plyr)
            self.unPlayTemp(board,row,col)
            if val >= maxi:
                maxi = val
                action = move

        return action

    def max_val(self, board, player, alpha, beta, original):
        moves = self.psblMvs(board);
        winner = self.checkWin1(board)
        if winner == 0 and len(moves) == 0:
            return 0
        elif winner == original:
            return 1
        elif winner != 0:
            return -1

        val = -100
        other = 1
        if player == 1:
            other = 2

        for move in moves:
            (row,col) = move
            self.playTemp(board,row,col,player)
            val = max(val, self.min_val(board, other, alpha, beta, original))
            self.unPlayTemp(board,row,col)
            if val >= beta:
                return val
            alpha = min(alpha,val)
        return val

    def min_val(self, board, player, alpha, beta, original):
        moves = self.psblMvs(board);
        winner = self.checkWin1(board)
        if winner == 0 and len(moves) == 0:
            return 0
        elif winner == original:
            return 1
        elif winner != 0:
            return -1

        val = 100
        other = 1
        if player == 1:
            other = 2

        for move in moves:
            (row, col) = move
            self.playTemp(board,row,col,player)
            val = min(val, self.max_val(board, other, alpha, beta, original))
            self.unPlayTemp(board,row,col)
            if val <= alpha:
                return alpha
            beta = min(beta,val)
        return val


    def checkWin(self):

        #user check
        if self.horCheck(self.board, 1) or self.verCheck(self.board, 1) or self.diaCheck(self.board, 1) or self.otherDiaCheck(self.board, 1):
            self.winner = 1
            
        #AI check
        if self.horCheck(self.board, 2) or self.verCheck(self.board, 2) or self.diaCheck(self.board, 2) or self.otherDiaCheck(self.board, 2):
            self.winner = 2
        
        if self.winner == 1:
            self.screen.blit(self.winimg,(20,100))
            self.is_game_over = True
        elif self.winner == 2:
            self.screen.blit(self.loseimg,(20,100))
            self.is_game_over = True
        elif self.checkZeros():
            self.is_game_over = True
        
    def horCheck(self, board, num):
        win1 = False
        for x in range(self.n):
            lineF = True
            for y in range(self.n):
                if board[x][y] != num:
                    lineF = False
                    break
            if lineF:
                win1 = True
                break

        return win1

    def verCheck(self, board, num):
        win1 = False
        for x in range(self.n):
            lineF = True
            for y in range(self.n):
                if board[y][x] != num:
                    lineF = False
                    break
            if lineF:
                win1 = True
                break

        return win1

    def diaCheck(self, board, num):
        win1 = True

        #mainDia
        for x in range(self.n):

            if board[x][x] != num:
                win1 = False
                break

        return win1

    def otherDiaCheck(self, board, num):
        win1 = True
        
        #otherDia
        for x in range(self.n):
            if board[x][self.n-x-1] != num:
                win1 = False
                break

        return win1

    def checkZeros(self):
        status = True
        
        for x in self.board:
            for y in x:
                if y == 0:
                    status = False
                    break
        
        return status

    def psblMvs(self, board):
        psbl_mvs = []
        for x in range(self.n):
            for y in range(self.n):
                if board[x][y] == 0:
                    psbl_mvs.append((x,y))

        return psbl_mvs

    def checkWin1(self, board):
        winner = 0

        #user check
        if self.horCheck(board, 1) or self.verCheck(board, 1) or self.diaCheck(board, 1) or self.otherDiaCheck(board, 1):
            winner = 1
        #AI check
        if self.horCheck(board, 2) or self.verCheck(board, 2) or self.diaCheck(board, 2) or self.otherDiaCheck(board, 2):
            winner = 2

        return winner