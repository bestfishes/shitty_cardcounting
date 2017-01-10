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
        # Note to self: have not implemented aces high function yet.

    def deal_facedown(self):
        self.facedown = True

    def flip_card_up(self):
        self.facedown = False

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
        self.inplay = True
        self.payout = False

    def get_new_card(self, card):
        self.cards.append(card)
        self.count = self.count + card.value
        if self.count > 21:
            self.count = 0
            for i in self.cards:
                if i.ace == True:
                    i.value = 1
                self.count = self.count + i.value
              

    def reset_new_hand(self):
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False

    def player_choice(self):
        while self.count < 21:
            print("%s's count is %s and their cards are:" % (str(self.name), str(self.count)))
            print(self.cards)
            choice = input("Should %s hit (h) or stand (s)?" % (str(self.name)))
            if choice.lower() == "h":
                self.get_new_card(current_deck[0])
                print(self.cards[-1])
                current_deck.pop(0)
                continue
                #Double check this continue
            elif choice.lower() == "s":
                self.inplay = False
                return
            else:
                print("Not a valid choice")
                continue 
        else:
            if self.count == 21:
                print("player hit a blackjack!")
                self.inplay = False
            else:
                print("Player went bust!")
                self.inplay = False
                print("Dealer collects %s's wager" % (str(self.name)))
                self.payout = True
        return

    def __repr__(self):
        return self.name



class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False

    def player_choice(self):
        self.cards[1].flip_card_up()
        print("The Dealer's hand is: ")
        print(self.cards)
        while self.count <= 16:
            self.get_new_card(current_deck[0])
            current_deck.pop(0)
        print(self.cards)
        print("The dealer's count is %s." % (self.count))
        self.inplay = False
        return

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

    
def hand_payout(player, dealer):
    if player.count > 21:
        print("Player busts. Dealer collects %s's wager" % (str(player)))
    elif dealer.count >21:
        print("Dealer busts, pays %s the amount of their bet" % (str(player)))
    elif player.count < dealer.count:
        print("Dealer wins, and collects %s's wager" % (str(player)))
    elif player.count > dealer.count:
        print("Dealer loses. %s wins their wager amount" % (str(player)))
    else: 
        print("Dealer and %s tie. No money is exchanged" % (str(player)))
    player.payout = True
    return

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
playing = True
while (playing == True and (len(current_deck) >= 4*len(table))):
    for i in range(len(table)):
        table[i].get_new_card(current_deck[0])
        current_deck.pop(0)
        print(table[i])
        print(table[i].cards)
        print(table[i].count)

#Second card, face up to the tables to players,facedown to the dealer
    for i in range(len(table)-1):
        table[i].get_new_card(current_deck[0])
        current_deck.pop(0)
        print(table[i])
        print(table[i].cards)
        print(table[i].count)
    current_deck[0].deal_facedown()
    table[-1].get_new_card(current_deck[0])
    current_deck.pop(0)
    print(table[-1])
    print(table[-1].cards)
    print(table[-1].count)
 

#Check for Naturals in players. Check dealer only if first card is face or ace. 
# So far doesn't do anything. Just checks.



    #Checks for naturals. Breaks if there are any. Will need to evaluate scoring outside of the loop.
    player_naturals = False
    dealer_naturals = False
    for i in range(len(table)-1):
        print(table[i].count)
        if table[i].count == 21:
            print(str(table[i]) + " has a natural")
            player_naturals = True
    if table[-1].count == 21:
        print(str(table[-1]) + " has a natural")
        dealer_naturals = True

    if (dealer_naturals == True and player_naturals == False):
        print("dealer takes all the chips")
        for i in range(len(table)-1):
            print("Dealer takes %s's wager" % (str(table[i])))
            table[i].payout = True
        for i in range(len(table)):
            table[i].reset_new_hand()
        continue
    elif (dealer_naturals == True and player_naturals == True):
        for i in range(len(table)-1):
            if table[i].count == 21:
                print(str(table[i]) + " takes his chips back")
                table[i].payout = True
            else:
                print("The Dealer takes " + str(table[i]) + "'s chips")
                table[i].payout = True
        for i in range(len(table)):
            table[i].reset_new_hand()
        continue
    elif (dealer_naturals == False and player_naturals == True):
        for i in range(len(table)-1):
            if table[i].count == 21:
                print("Dealer pays " + str(table[i]) + " 1.5 times the bet")
                table[i].inplay = False
                table[i].payout = True
            else:
                print(str(table[i]) + " is still in play")
    else:
        print("No naturals, game still in play")

   
#Here: Playing a hand.
    for i in range(len(table)):
        while table[i].inplay == True:
            table[i].player_choice()
    #dealer's hand:

    for i in range(len(table)-1):
        while table[i].payout == False:
            hand_payout(table[i], table[-1])
    print(current_deck)
    

    
            

# Restarts the hand. Doesn't clear the players cards. Should probably put everything in a function instead of this.           
    choice = input("Do you want to play a hand? Enter y/n: ")
    print(choice.lower())
    if choice.lower() == "n":
        playing = False
        print("Goodbye!")
    elif choice.lower() == "y":
        print("Good choice!")
        for i in range(len(table)):
            table[i].reset_new_hand()
    else:
        print("Incorrect choice. Exiting Game")
        playing = False
        


        

#Evaluating the loop:
#dealer_score = table[-1].count
#player_scores = {}
#for i in range(len(table)-1):
#    player_scores[table[i].name] = table[i].count
#print(dealer_score)
#print(player_scores)
