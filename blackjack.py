import pygame as pg
import bj_game 

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)

#background

background = pg.image.load('bj_game_assets\\background.png')
deck_sprite = pg.image.load('bj_game_assets\\full_deck_spritesheet.jpg')
# Deck sritesheet , card sprites are 70px wide and 100px tall. First column of sprites is back of card variants
# First card at (120,150) is the Ace of Hearts | Hearts, Diamonds, Clubs, Spades

def load_card(rank,suit):

    card = pg.Surface((70,100))
    card.blit(deck_sprite,(0,0),(x,y,70,100))
    return card

    

run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    screen.blit(background,(0,0))
    pg.display.flip()




pg.quit()