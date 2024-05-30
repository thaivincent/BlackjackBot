import pygame as pg
import bj_game as bj
import sys
import os
import random
import numpy

pg.init()

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 900

# How many decks in a standard game of blackjack
DECK_COUNT = 6

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), pg.RESIZABLE)
screen.convert()

# Loading assets and images

background = pg.image.load('bj_game_assets\\blackjack_background2.jpg')
deck_sprite = pg.image.load('bj_game_assets\\full_deck_spritesheet.png').convert_alpha()
hover_img = pg.image.load("bj_game_assets\\Medium Hover.png").convert_alpha()

GAME_FONT = pg.freetype.Font("bj_game_assets\\Minecraft.ttf", 48)


class animation(pg.sprite.Sprite):
    def __init__(self, x, y,dir):
        super().__init__()
        self.sprites = []
        for file in os.listdir(dir):
            f = os.path.join(dir,file)
            self.sprites.append(pg.image.load(f))

        self.clicked = False
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


    def check_clicked(self):  
        pos = pg.mouse.get_pos()
        action = False

        if self.rect.collidepoint(pos) and not self.clicked:
            hover = hover_img.get_rect()
            hover.topleft = (self.rect.left, self.rect.top)
            screen.blit(hover_img,hover)

            if pg.mouse.get_pressed()[0] == 1:
                self.clicked = True
                self.is_animating = True
                action = True

        if pg.mouse.get_pressed()[0] == 0:
                    self.clicked = False           
        return action




        
# Deck spritesheet , card sprites are 70px wide and 100px tall. First column of sprites is back of card variants
# First card at (120,150) | Hearts, Diamonds, Clubs, Spades

def load_card(card, x, y):
    # Dimensions of a card
    spacing = 11.5
    width = 75
    height = 105

    # Rank = 0 means loading a card back
    if card == 0:
        screen.blit(deck_sprite,(x,y),(119,374,width,height))
        return

    x_pos = bj.RANKS.index(card.rank) # This Calculates the position of the card on the spritesheet.

    #Converts Positioning of the SUITS index to the coresponding row of the sprite index.
    y_pos = bj.SUITS.index(card.suit) 
    if y_pos != 3:
        y_pos += 1
        y_pos %= 3

    
    # Initalize at the first card, skipping the back card.
    sprite_x = 200 + (x_pos * spacing) + x_pos * 72
    sprite_y = 150 + (y_pos * spacing) + y_pos * 100
    screen.blit(deck_sprite,(x,y),(sprite_x,sprite_y,width,height))
    return



def start_game():
    # Intialize a game deck and shuffle it
    global game_deck
    game_deck = list(numpy.repeat(bj.new_deck,DECK_COUNT))
    random.shuffle(game_deck)

    # Deal 2 cards to player and dealer
    playerhand = bj.Hand([game_deck.pop(0), game_deck.pop(0)],0,0) 
    dealerhand = bj.Hand([game_deck.pop(0), game_deck.pop(0)],0,0)
    return playerhand, dealerhand       

def player_turn():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if hit_button.check_clicked():
                bj.hit(playerhand.cards,game_deck)
                bj.get_total(playerhand)
                bj.print_hand(playerhand)
                return
            if stand_button.check_clicked():
                print("stand")
                return
    



dealer_starting_x = 609

playerhand,dealerhand = start_game()
bj.get_total(playerhand)
bj.get_total(dealerhand)
screen.blit(background,(0,0))
pg.display.flip()

buttons = pg.sprite.Group()
hit_button = animation(540,675,"bj_game_assets\\hit_button")
stand_button  = animation(740,675,"bj_game_assets\\stand_button")
buttons.add(hit_button)
buttons.add(stand_button)

# Initializing all statuses
run = True
dealer_loaded = False
player_loaded = False

while run:
    # Quit
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
    

    buttons.draw(screen)
    buttons.update()

    #Load all of the cards to the screen
    while not dealer_loaded :
        for i in dealerhand.cards:
            load_card(i,dealer_starting_x, 175)
            dealer_starting_x += 50
        if dealerhand.alt_tot != dealerhand.tot:
            string = str(dealerhand.tot) + "/" + str(dealerhand.alt_tot)
            GAME_FONT.render_to(screen,(480,205),str(string),(255,255,255))
            print(string)
        else: 
            GAME_FONT.render_to(screen,(510,205),str(dealerhand.tot),(255,255,255))
        
        dealer_loaded = True
        dealer_starting_x = 609

    while not player_loaded:
        for i in playerhand.cards:
            load_card(i,dealer_starting_x, 445)
            dealer_starting_x += 50
        
        player_loaded = True
        dealer_starting_x = 609   
    
    pg.display.flip()
    player_turn()



    
    



pg.quit()