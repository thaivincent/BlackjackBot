import pygame as pg

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)

#background

background = pg.image.load('bj_game_assets\\background.png')

run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.blit(background,(0,0))
    pg.display.flip()
    



pg.quit()