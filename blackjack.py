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

def load_card(rank,suit, x, y):
    # Dimensions of a card
    spacing = 11.5
    width = 75
    height = 105

    # Rank = 0 means loading a card back
    if rank == 0:
        screen.blit(deck_sprite,(x,y),(119,374,width,height))
        return

    x_pos = bj.RANKS.index(rank) # This Calculates the position of the card on the spritesheet.

    #Converts Positioning of the SUITS index to the coresponding row of the sprite index.
    y_pos = bj.SUITS.index(suit) 
    if y_pos != 3:
        y_pos += 1
        y_pos %= 3

    
    # Initalize at the first card, skipping the back card.
    sprite_x = 200 + (x_pos * spacing) + x_pos * 72
    sprite_y = 150 + (y_pos * spacing) + y_pos * 100
    screen.blit(deck_sprite,(x,y),(sprite_x,sprite_y,width,height))
    return


screen.blit(background,(0,0))
pg.display.flip()

run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    
    load_card("Q","club",100,100)
    pg.display.flip() 


    
    



pg.quit()