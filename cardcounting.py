# A game to help counting cards
# In theory, anyways

### IMPORTANT NOTE : WRITTEN IN PYTHON3 ###
# Because using languages you don't understand is always a good idea #

#First, creating the card deck.
import random
import itertools

# data
class Card(object):
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        if rank < 10:
            self.value = rank
        else:
            self.value = 10
        self.ace = False
        if rank == 1:
            self.ace = True
        # Not sure if this will help the aces or not?
        facecards = {1:'A', 10:'T', 11:'J', 12:'Q', 13:'K'}
        if self.rank in facecards.keys():
            self.rank = facecards[self.rank]
        else:
            self.rank = str(self.rank)
        self.suit = str(self.suit)
        self.name = ''.join((self.rank,self.suit))
        # Note to self: have not implemented aces high function yet.

    def __repr__(self):
        return self.name

def create_deck(number_of_decks):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    for i in range(number_of_decks):
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    return deck

def dealing_the_cards(players):
    table = {}
    for player in range(players):
        player_name = 'Player %s' % (player+1)
        table[player_name] = current_deck[player]
        #current_deck.pop([player])
    table['Dealer'] = current_deck[players]
    return table


#Setting up and shuffling the deck
number_of_decks = 1
current_deck = create_deck(number_of_decks)
random.shuffle(current_deck)
print(current_deck)

#Placing the bet
# yet to be implemented...

#The cut:
#Also yet to be implemented...

#The deal:
number_of_players = 2
table = dealing_the_cards(number_of_players)
print(table)

