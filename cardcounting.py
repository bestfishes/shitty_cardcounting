# A game to help counting cards
# In theory, anyways

### IMPORTANT NOTE : WRITTEN IN PYTHON3 ###
# Because using languages you don't understand is always a good idea #

#First, creating the card deck.
import random
import itertools

# new classes
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
        self.facedown = False
        # Note to self: have not implemented aces high function yet.

    def deal_facedown(self):
        self.facedown = True

    def __repr__(self):
        if self.facedown == False:
            return self.name
        else:
            return 'XX'

class Player(object):
    def __init__(self,player_number):
        self.player_number = player_number
        self.name = "Player%s" % (player_number)
        self.cards = []
        self.count = 0

    def get_new_card(self, card):
        self.cards.append(card)
        self.count = self.count + card.value

    def __repr__(self):
        return self.name

class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        self.cards = []
        self.count = 0
    

# functions

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


#Setting up and shuffling the deck
number_of_decks = 1
current_deck = create_deck(number_of_decks)
random.shuffle(current_deck)
print(current_deck)

#Sitting at the table:
number_of_players = 2
table = []
for player in range(number_of_players):
    table.append(Player(player + 1))
    print(str(player))
    print(table[player])
    print(table[player].count)
table.append(Dealer())

print(table)
print(table[1].count)
print(table[1].cards)

#Placing the bet
# yet to be implemented...

#The cut:
#Also yet to be implemented...

#The deal:
#First card
 # Most of this should go in a function
for i in range(len(table)):
    table[i].get_new_card(current_deck[0])
    current_deck.pop(0)
    print(table[i])
    print(table[i].cards)

#Second card, face up to the tables to players,facedown to the dealer
for i in range(len(table)-1):
    table[i].get_new_card(current_deck[0])
    current_deck.pop(0)
    print(table[i])
    print(table[i].cards)
current_deck[0].deal_facedown()
table[-1].get_new_card(current_deck[0])
current_deck.pop(0)
print(table[-1])
print(table[-1].cards)


