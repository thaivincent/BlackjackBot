import pygame as pg
import bj_game as bj
import sys
import os

pg.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)
screen.convert()

#Loading assets and images

background = pg.image.load('bj_game_assets\\background.png')
deck_sprite = pg.image.load('bj_game_assets\\full_deck_spritesheet.png').convert_alpha()
hit_button = pg.image.load("bj_game_assets\hit_button\Hit Button1.jpg")

class Button():
    def __init__(self,x,y,image): 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def draw(self):
        screen.blit(self.image, (self.rect.x,self.rect.y))

class animation(pg.sprite.Sprite):
    def __init__(self, x, y,dir):
        super().__init__()
        self.sprites = []
        for file in os.listdir(dir):
            f = os.path.join(dir,file)
            self.sprites.append(pg.image.load(f))
        self.is_animating = False
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.01

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]



        
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

button_sprites = pg.sprite.Group()
button = animation(100,100,"bj_game_assets\\hit_button")
button_sprites.add(button)


run = True
while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            button.animate()

    button_sprites.draw(screen)
    button.update()


    pg.display.flip()




    
    



pg.quit()