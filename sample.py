# -*- coding: utf-8 -*-

import pygame

pygame.init()

screen = pygame.display.set_mode((800,600))
bg = pygame.Surface(screen.get_size())
bg.fill((0,0,0))
bg = bg.convert()
screen.blit(bg, (0, 0))

clock = pygame.time.Clock()
mloop = True
fps = 60
playtime = 0.0

while mloop:
    mlsc = clock.tick(fps)
    playtime += mlsc/1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mloop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                mloop = False

    txt = "FPS: {0:.2f}   Playtime: {1:.2f}".format(clock.get_fps(), playtime)
    pygame.display.set_caption(txt)

    pygame.display.flip()

pygame.quit();