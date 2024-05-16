import pygame as pg
import bj_game as bj
import sys
import os

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)
screen.convert()

#background

background = pg.image.load('bj_game_assets\\background.png')
deck_sprite = pg.image.load('bj_game_assets\\full_deck_spritesheet.png').convert()
# Deck sritesheet , card sprites are 70px wide and 100px tall. First column of sprites is back of card variants
# First card at (120,150) | Hearts, Diamonds, Clubs, Spades

def load_card(rank,suit):
    # Creates a surface 70x100 which is the dimension of the card.
    card = pg.Surface((70,100))
    

    if rank == 0:
        return (119,374,70,100)

    
    x_pos = bj.RANKS.index(rank) # This Calculates the position of the card on the spritesheet.

    #Converts Positioning of the SUITS index to the coresponding row of the sprite index.
    y_pos = bj.SUITS.index(suit) 
    if y_pos != 3:
        y_pos += 1
        y_pos %= 3

    # Initalize at the first card, skipping the back card.
    x = 202 + x_pos * 84
    y = 149 + y_pos * 113

    spacing = 10
    
    card.blit(deck_sprite,(0,0),(x,y,70,100))
    return card


screen.blit(background,(0,0))
pg.display.flip()

run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    screen.blit(deck_sprite,(0,0),load_card(0,0))/
    pg.display.flip() 


    
    



pg.quit()