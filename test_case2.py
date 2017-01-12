import random
import itertools

# Creating a bunch of decks to trial various situations
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.ace = False
        if rank < 10 and rank > 1:
            self.value = rank
        elif rank == 1:
            self.value = 11
            self.ace = True
        else:
            self.value = 10
        facecards = {1:'A', 10:'T', 11:'J', 12:'Q', 13:'K'}
        if self.rank in facecards.keys():
            self.rank = facecards[self.rank]
        else:
            self.rank = str(self.rank)
        self.suit = str(self.suit)
        self.name = ''.join((self.rank,self.suit))
        self.facedown = False

    def deal_facedown(self):
        self.facedown = True

    def flip_card_up(self):
        self.facedown = False

    def __repr__(self):
        if self.facedown == False:
            return self.name
        else:
            return 'XX'

# The traditional deck

def create_deck(number_of_decks):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    print(ranks)
    for i in range(number_of_decks):
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    random.shuffle(deck)
    return deck
        


# Creates a deck only of aces
def aces_only_deck(number_of_decks):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [1 for x in range(1,14)]
    print(ranks)
    for i in range(number_of_decks):
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    random.shuffle(deck)
    return deck


# Creates a deck where the dealer gets a natural, and everyone else gets an 18. Creates a longer deck behind, but doesn't shuffle. (Not needed - only used to pass the appropriate length).

def dealer_natural(number_of_decks, table_size):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    print(ranks)
    print(table_size)
    end_point = 2*(table_size+1)
    print(end_point)
    for i in range(end_point):
        print(i)
        if i == table_size:
            new_card = Card(1,'S')
        elif i == 2*table_size+1:
            new_card = Card(13,'S')
        elif i < table_size:
            new_card = Card(10,'D')
        else:
            new_card = Card(9,'D')
        deck.append(new_card)
    for i in range(number_of_decks):        
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    return deck

#Player 1 gets a natural but no-one else does. Same deck rules as above. 

def player1_natural(number_of_decks, table_size):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    print(ranks)
    print(table_size)
    end_point = 2*(table_size+1)
    print(end_point)
    for i in range(end_point):
        print(i)
        if i == 0:
            new_card = Card(1,'S')
        elif i == table_size+1:
            new_card = Card(13,'S')
        elif i < table_size+1:
            new_card = Card(10,'D')
        else:
            new_card = Card(9,'D')
        deck.append(new_card)
    for i in range(number_of_decks):        
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    return deck    

#All players get a natural, but not the dealer.

def players_all_natural(number_of_decks, table_size):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    print(ranks)
    print(table_size)
    end_point = 2*(table_size+1)
    print(end_point)
    for i in range(end_point):
        print(i)
        if i < table_size:
            new_card = Card(1,'S')
        elif i > table_size and i < 2*table_size+1:
            new_card = Card(13,'S')
        elif i == table_size:
            new_card = Card(10,'D')
        else:
            new_card = Card(9,'D')
        deck.append(new_card)
    for i in range(number_of_decks):        
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    return deck

number_of_decks = 6
#current_deck = create_deck(number_of_decks)
#print(current_deck)

#aces_deck = aces_only_deck(number_of_decks)
#print(aces_deck)

number_of_players = 2 #Does not count the dealer
#ndealer_deck = dealer_natural(number_of_decks, number_of_players)
#print(ndealer_deck)

players_deck = players_all_natural(number_of_decks, number_of_players)
print(players_deck)
