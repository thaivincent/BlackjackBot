import random

suits = ["diamond","club","heart","spade"]
ranks = ["2","3","4","5","6","7","8","9","10","J","Q","K","A" ]

# A class with 2 fields of type String. One stores suit and the other stores rank.
class Card:
    def __init__(self,suit,rank):
       self.suit = suit
       self.rank = rank

# A Hand is a set of 2 cards, with 2 fields indicating its hard and soft total. 
# A Hand only has a different soft and hard total when there is an ace.
# For the dealer, card1 is upcard while card2 is facedown.
class Hand:
    def __init__(self,card1,card2,tot,alt_tot) -> None:
        self.card1 = card1
        self.card2 = card2
        if card1.rank == "A" or card2.rank == "A":
            tot = get_value(card1) + 1
            alt_tot = get_value(card1) + 11
        else:
            tot, alt_tot = get_value(card1) + get_value(card2)

 # get_value is a function which returns the value of a given card. This is the numeric value for 2-9 and 10 for J,Q,K, and 1 or 11 for A           
def get_value(card):
    if card.rank in ranks[:8]:
        return card.rank
    elif card.rank in ranks[9:11]:
        return "10"
    else:
        return "A"

# Orderd new deck initalized
new_deck = []
for rank in ranks:
    for suit in suits:
        card = Card(suit,rank)
        new_deck.append(card)


    