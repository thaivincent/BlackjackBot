import random

SUITS = ["diamond","club","heart","spade"]
RANKS = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

# A class with 2 fields of type String. One stores suit and the other stores rank.
class Card:
    def __init__(self,suit,rank):
       self.suit = suit
       self.rank = rank

# A Hand is a list of Cards, with 2 fields indicating its hard and soft total. 
# A Hand only has a different soft and hard total when there is an ace.
# For the dealer, card1 is upcard while card2 is facedown.
# Hand(Listof Cards, int, int)
class Hand:
    def __init__(self,cards,tot,alt_tot):
        self.cards = cards
        self.tot = tot
        self.alt_tot = alt_tot

 # get_value is a function which returns the value of a given card. This is the numeric value for 2-9 and 10 for J,Q,K, and 1 or 11 for A           
def get_value(card):
    if card.rank == "A":
        return card.rank
    elif card.rank in RANKS[1:9]:
        return int(card.rank)
    elif card.rank in RANKS[9:]:
        return int(10)
   

# a function that updates the tot and alt tot values of a Hand class following the rules of blackjack
def get_total(hand):
    for card in hand.cards:
        if card.rank == "A":
            hand.tot += 1
            hand.alt_tot += 11
        else:
            hand.tot += get_value(card)
            hand.alt_tot = hand.tot
    return

def hit(hand,deck):
    hand.append(deck.pop(0))
    return

# For debuging hands
def print_hand(hand):
    for card in hand.cards:
        print(card.rank,"of",card.suit)
    print("Tot:",hand.tot,"\n Alt Tot: ",hand.alt_tot)
    return

def print_card(card):
    print(card.rank,"of",card.suit)
    
# Orderd new deck initalized
new_deck = []
for rank in RANKS:
    for suit in SUITS:
        card = Card(suit,rank)
        new_deck.append(card)




#playerhand = Hand([Card("Heart","9"),Card("Spade","9")],0,0)
