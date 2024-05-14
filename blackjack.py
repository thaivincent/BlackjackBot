import pg as pg

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)
background = pg.image.load()
run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    



pg.quit()