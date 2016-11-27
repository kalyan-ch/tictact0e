import pygame, os

class TicToe(object):
    
    def __init__(self, width, height, fps, n):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.display.set_caption("Tic Tac Toe")
        pygame.mixer.music.load('data/intro.mp3')

        self.width = width
        self.height = height
        self.gridW = int(self.width) - 40
        self.gridH = int(self.width) - 200
        self.xOffset = 20
        self.yOffset = 100
        self.n = n
        self.board = [[0 for x in range(n)] for x in range(n)]
        self.fps = fps
        self.screen = pygame.display.set_mode((self.width,self.height),pygame.DOUBLEBUF)
        self.bg = pygame.Surface(self.screen.get_size())
        self.bg.fill((204, 204, 204))
        self.fps = fps
        self.gridArea = pygame.draw.rect(self.bg, (255,255,255), (self.xOffset,self.yOffset,self.gridW, self.gridH))
        self.draw_lines()

        pygame.mixer.music.play(-1,0.0)
        print self.board
        self.screen.blit(self.bg, (0,0))


    def run(self):
        running = True
        
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousepos = pygame.mouse.get_pos()
                    self.move(mousepos)

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
    
    def move(self, mousepos):
        x = mousepos[0]
        y = mousepos[1]
        
        wThres = self.gridW/self.n + self.xOffset
        hThres = self.gridH/self.n + self.yOffset
        
        if x > self.xOffset and y > self.yOffset:
            a,b = 0,0
            
