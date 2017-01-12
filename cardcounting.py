# A game to help counting cards
# In theory, anyways

### IMPORTANT NOTE : WRITTEN IN PYTHON3 ###
# Because using languages you don't understand is always a good idea #

# The RULES:
# Current Play is with a 6 deck shoe
# Cut is 1.5 decks in
# Dealer stays on a soft 17 (for now)
# No Surrendering (early or late)


### TO DO: 
# Change Dealer play so that he hits on a soft 17
# Move all additional functions into player class and have choice pull from dictionary (some conceptualization needed)?
    # Dealer keeps seperate class?
# Clean up checking for naturals 
# Force correct selection on choice of player type
# Add in - betting values
#        - doubling down
#        - double down after splitting
#        - Insurance
# Create basic strategy player


#First, creating the card deck.
import random
import itertools

# new classes
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


class Player:
    def __init__(self,player_number, iteration = 1):
        self.player_number = player_number
        self.name = "Player_%s" % (player_number)
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False
        self.strategy = "user choice"
        self.splithand = None
        self.firstsplit = None
        self.iteration = iteration

    def get_new_card(self, card):
        self.cards.append(card)
        self.count = self.count + card.value
        if self.count > 21:
            self.count = 0
            first = True
            for i in self.cards:
                if i.ace == True and i.value != 1 and first == True:
                    i.value = 1
                    first = False
                self.count = self.count + i.value

    def reset_new_hand(self):
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False
        self.splithand = None
        self.firstsplit = None
        self.iteration = 1

    def player_choice(self):
        #Need to figure out how to run this through a second time with second card hand. 
        while self.cards[0].rank == self.cards[1].rank and self.iteration < 3:
            split_choice = ''
            while split_choice.lower() not in ['y', 'n']:                
                split_choice = input("should %s split their cards?" % (self.name))
            if split_choice.lower() == 'y':
                self.split_cards()
            else:
                break
        while self.count < 21:
            print("%s's count is %d and their cards are:" % (self.name, self.count))
            print(self.cards)
            choice = input("Should %s hit (h) or stand (s)?" % (self.name))
            if choice.lower() == "h":
                self.get_new_card(current_deck.pop(0))
                print(self.cards[-1])
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
                if self.iteration == 1:
                    print("player hit a blackjack!")
                else:
                    print("Player has 21 points.")
                self.inplay = False
            else:
                print("Player went bust!")
                self.inplay = False
                print("Dealer collects %s's wager" % (self.name))
                self.payout = True
        return
   
    def split_cards(self):
        print("You've chosen to split your cards!")
        print("You will double your bet!")
        #Remember to make new bet
        new_iteration = self.iteration + 1
        new_name = str(self.player_number) + '-' + str(new_iteration)
        if self.splithand != None:
            self.firstsplit = self.splithand
        self.splithand = Player(new_name, iteration = new_iteration)
        print('new iteration is %d' % (self.splithand.iteration))
        self.splithand.get_new_card(self.cards.pop(1))
        print('%s hand count is %d and the cards are: ' % (self.splithand.name, self.splithand.count))
        print(self.splithand.cards)
        self.splithand.get_new_card(current_deck.pop(0))
        self.count = self.cards[0].value
        self.iteration += 1
        print(self.splithand.cards)          
        self.get_new_card(current_deck.pop(0))
        self.splithand.player_choice()
        #Remember to add bet amount to new bet amount
        return

    def __repr__(self):
        return self.name



class Dealer_Mimick(Player):
    def __init__(self,player_number):
        self.player_number = player_number
        self.name = "Player_%s" % (player_number)
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False
        self.strategy = "mimicking the dealer"

    def player_choice(self):
        print("%s's count is %d and their cards are:" % (self.name, self.count))
        print(self.cards)
        while self.count <= 16:
            print("%s is choosing to hit." % (self.name))
            self.get_new_card(current_deck.pop(0))
            print(self.cards)
        print("%s's count is %d." % (self.name, self.count))
        self.inplay = False
        return

class Basic_Strategy(Player):
    def __init__(self,player_number):
        self.player_number = player_number
        self.name = "Player_%s" % (player_number)
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False
        self.strategy = "basic strategy"

class Dealer(Player):
    def __init__(self):
        self.name = "Dealer"
        self.cards = []
        self.count = 0
        self.inplay = True
        self.payout = False
        self.strategy = "Dealer"

    def player_choice(self):
        self.cards[1].flip_card_up()
        print("The Dealer's hand is: ")
        print(self.cards)
        while self.count <= 16:
            self.get_new_card(current_deck.pop(0))
        print(self.cards)
        print("The dealer's count is %s." % (self.count))
        self.inplay = False
        return

# functions
def players_pairs(number_of_decks, table_size):
    deck = []
    new_deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    print(ranks)
    print(table_size)
    end_point = 4*(table_size+1)
    print(end_point)
    for i in range(end_point):
        print(i)
        if i <= 2*table_size+1:
            new_card = Card(4,'S')
        else:
            new_card = Card(4,'D')
        deck.append(new_card)
    for i in range(number_of_decks):        
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            new_deck.append(new_card)
    random.shuffle(new_deck)
    deck += new_deck
    return deck

def create_deck(number_of_decks):
    deck = []
    suits = ('C', 'D', 'H', 'S')
    ranks = [x for x in range(1,14)]
    for i in range(number_of_decks):
        deck_list = itertools.product(ranks,suits)
        for elem in deck_list:
            new_card = Card(elem[0],elem[1])
            deck.append(new_card)
    random.shuffle(deck)
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
number_of_players = 2
number_of_decks = 6
#current_deck = create_deck(number_of_decks)
current_deck = players_pairs(number_of_decks, number_of_players)
print(current_deck)

player_types = { '1' : Player, '2' : Dealer_Mimick, '3' : Basic_Strategy}

#Sitting at the table:
    #This should get rewritten into an option/function to limit the number of players & Force a correct choice

table = []
print("Please select a player type:")
print("1 : User Controlled Player")
print("2 : AI (Dealer Mimicking Strategy)")
print("3 : AI (Basic Strategy) - Not Yet Operational")
for player in range(number_of_players):
    choice = input("Player_%d: " % (player+1))
    table.append(player_types[choice](player + 1))
    print('%s is using %s' % (table[player], table[player].strategy))
table.append(Dealer())
print()
print(table)
print()


#Placing the bet
# yet to be implemented...

#The cut:
#Also yet to be implemented...

#The deal:
    #Assumes the re-deal point is 1.5 decks in. 
#First card
playing = True
while (playing == True and (len(current_deck) >= 78)):
    for i in range(len(table)):
        table[i].get_new_card(current_deck.pop(0))


#Second card, face up to the tables to players,facedown to the dealer
    for i in range(len(table)-1):
        table[i].get_new_card(current_deck.pop(0))
        print(table[i])
        print(table[i].cards)
        print(table[i].count)
        print()
    current_deck[0].deal_facedown()
    table[-1].get_new_card(current_deck.pop(0))
    print(table[-1])
    print(table[-1].cards)
    print(table[-1].count)
    print()
 

#Check for Naturals in players.  
    #Checks for naturals. Will need to evaluate scoring outside of the loop.
    #This is so ugly but it works for now.
    #Need to rethink it completely. Bad implementation.
    player_naturals = False
    dealer_naturals = False
    for i in range(len(table)-1):
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
            table[i].inplay = False
            table[i].payout = True
        table[-1].inplay = False
    elif (dealer_naturals == True and player_naturals == True):
        for i in range(len(table)-1):
            if table[i].count == 21:
                print(str(table[i]) + " takes his chips back")
            else:
                print("The Dealer takes " + str(table[i]) + "'s chips")
            table[i].inplay = False
            table[i].payout = True
        table[-1].inplay = False
    elif (dealer_naturals == False and player_naturals == True):
        cont = False
        for i in range(len(table)-1):
            if table[i].count == 21:
                print("Dealer pays " + str(table[i]) + " 1.5 times the bet")
                table[i].inplay = False
                table[i].payout = True
            else:
                print(str(table[i]) + " is still in play")
                cont = True
        if cont == False:
            table[-1].inplay = False
    else:
        print("No naturals, game still in play")
    print()

   
#Here: Playing a hand.
    for i in range(len(table)):
        while table[i].inplay == True:
            table[i].player_choice()
    for i in range(len(table)-1):
        while table[i].payout == False:
            hand_payout(table[i], table[-1])
        if table[i].firstsplit != None:
            while table[i].firstsplit.payout == False:
                hand_payout(table[i].firstsplit, table[-1])
            if table[i].firstsplit.splithand != None:
                while table[i].firstsplit.splithand.payout == False:
                    hand_payout(table[i].firstsplit.splithand, table[-1])
        if table[i].splithand != None:
            while table[i].splithand.payout == False:
                hand_payout(table[i].splithand, table[-1])
    print(current_deck)
    

    
            

# Restarts the hand. Should probably put everything in a function instead of this.           
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
