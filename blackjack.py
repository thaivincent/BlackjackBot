import pygame as pg
import bj_game as bj
import sys
import os
import random
import numpy
import time

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
    global dealerhand
    global playerhand
    game_deck = list(numpy.repeat(bj.new_deck,DECK_COUNT))
    random.shuffle(game_deck)

    # Deal 2 cards to player and dealer
    playerhand = bj.Hand([game_deck.pop(0), game_deck.pop(0)],0,0) 
    dealerhand = bj.Hand([game_deck.pop(0), game_deck.pop(0)],0,0)
    return playerhand, dealerhand       


# stand_flag = False
bust_flag = False

def player_stand():
    global stand_flag
    stand_flag = True
    return

def player_bust():
    global bust_flag
    bust_flag = True
    return


def player_turn():
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if hit_button.check_clicked():
                bj.hit(playerhand.cards,game_deck)
                bj.get_total(playerhand)
                if playerhand.tot > 21 and playerhand.alt_tot > 21:
                    player_bust()
                bj.print_hand(playerhand)
                return
            if stand_button.check_clicked():
                player_stand()
                print("stand")
                return
    

def updateDealerTot():
    if dealerhand.alt_tot != dealerhand.tot:
        if dealerhand.alt_tot == 21:
            string = str(dealerhand.alt_tot)
            GAME_FONT.render_to(screen,(480,205),str(string),(255,255,255))
            print(string)
        else:
            string = str(dealerhand.tot) + "/" + str(dealerhand.alt_tot)
            GAME_FONT.render_to(screen,(480,205),str(string),(255,255,255))
            print(string)
    else: 
        GAME_FONT.render_to(screen,(510,205),str(dealerhand.tot),(255,255,255))


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


# Redraws the entire game: background, cards, and dealerhand value
def redraw_game():
    screen.blit(background,(0,0))
    dealer_starting_x = 609
    player_starting_x = 609
    for i in dealerhand.cards:
        load_card(i,dealer_starting_x, 175)
        dealer_starting_x += 60
    for i in playerhand.cards:
        load_card(i,player_starting_x, 445)
        player_starting_x += 60
    if not stand_flag:
        load_card(0, dealer_starting_x-60, 175)
    
    updateDealerTot()

    buttons.draw(screen)
    buttons.update()
    pg.display.flip()


# For clearing player and dealer hands, resets their totals as well
def clear_hand(hand):
    for card in hand.cards:
        card == None
    hand.tot = 0
    hand.alt_tot = 0
    return

# Resets game variables and hands
def reset_game():
    global dealer_starting_x
    dealer_starting_x = 609
    global dealer_loaded
    dealer_loaded = False
    global player_loaded
    player_loaded = False
    global stand_flag
    stand_flag = False
    global bust_flag
    bust_flag = False
    playerhand, dealerhand = start_game()
    buttons.draw(screen)
    buttons.update()
    return

# Initializing all statuses
run = True

# Function to exit game when the X button is pressed
def exit_game():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

# Checks winner of blackjack game, used each time the dealer hits
def check_winner():
    if (dealerhand.tot >= 17 and dealerhand.tot <= 21) or (dealerhand.alt_tot >= 17 and dealerhand.alt_tot <= 21):
            if playerhand.tot < dealerhand.tot and playerhand.tot < dealerhand.alt_tot:
                print("Dealer wins.")
            elif playerhand.tot == dealerhand.tot and playerhand.tot == dealerhand.tot:
                print("Push.")
            else:
                print("Dealer bust.")
    return


while run:

    # Initialize game
    exit_game()
    reset_game()
    redraw_game()

    #Load all of the cards to the screen
    while not dealer_loaded :
        exit_game()
        for i in dealerhand.cards:
            load_card(i,dealer_starting_x, 175)
            dealer_starting_x += 60
        
        # Loads back of card ON TOP of actual card, hence the -50 in x coordinate
        load_card(0, dealer_starting_x-60, 175)
        
        if bj.get_value(dealerhand.cards[0]) == "A":
            string = str(1) + "/" + str(11)
            GAME_FONT.render_to(screen,(480,205),str(string),(255,255,255))
            print(string)
        else: 
            GAME_FONT.render_to(screen,(510,205),str(bj.get_value(dealerhand.cards[0])),(255,255,255))
        
        dealer_loaded = True
        dealer_starting_x = 609

    while not player_loaded:
        exit_game()
        for i in playerhand.cards:
            load_card(i,dealer_starting_x, 445)
            dealer_starting_x += 60
        
        player_starting_x = dealer_starting_x

        player_loaded = True
        dealer_starting_x = 609   

    pg.display.flip()

    while not stand_flag: 
        exit_game()
        if (bust_flag) or (playerhand.tot >= 21 and playerhand.alt_tot >= 21):
            print("Here1")
            pg.display.flip()
            break
        else:
            player_turn()
            redraw_game()
            pg.display.flip()
            if stand_flag == True:
                break
            print("Here2")
    pg.display.flip()

    while stand_flag:
        exit_game()
        redraw_game()
        bj.hit(dealerhand.cards, game_deck)
        dealerhand.tot, dealerhand.alt_tot = bj.get_total(dealerhand)
        if (dealerhand.tot >= 17 and dealerhand.tot <= 21) or (dealerhand.alt_tot >= 17 and dealerhand.alt_tot <= 21):
            check_winner()
            reset_game()
            print(stand_flag)
            break
    
    if (bust_flag):    
        time.sleep(1.25)
        print("Player bust.")



pg.quit()