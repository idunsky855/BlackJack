import random

suits = ("Hearts", "Clubs", "Spades", "Diamonds")
ranks = ("Two", "Three", "Four", "Five", "Six", "Seven","Eight","Nine","Ten","Jack", "Queen", "King", "Ace" )
values = {"Two":2 , "Three": 3, "Four": 4, "Five": 5, "Six" : 6, "Seven":7, "Eight":8, "Nine":9 , "Ten": 10, "Jack":10, "Queen" : 10, "King":10, "Ace":11 }

playing = True

class Card:
    '''
    Card represnts a playing card
    Attributes: rank - string, suit - string
    '''
    def __init__(self, rank : str, suit : str) -> None:
        '''
        initialize a new card with a rank and suit
        params: rank - string, suit - string
        '''
        self.rank = rank 
        self.suit = suit
        self.value = values[rank]

    def __str__(self) -> str:
        return self.rank + " of " + self.suit
    

class Deck:
    '''
    represents a deck of cards
    attributes: deck - list of cards
    '''
    def __init__(self) -> None:
        '''
        initialize a new playing cards deck
        '''
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(rank,suit))
            
    def __str__(self) -> str:
        deckStr = "Deck cards:\n"
        for card in self.deck:
            deckStr = deckStr + "\t" + card.__str__() + "\n"
        
        return deckStr
    
    def shuffle(self):
        '''
        shuffles the deck
        '''
        random.shuffle(self.deck)

    def deal(self):
        '''
        pops and returns a card from the deck
        '''
        return self.deck.pop()


class Hand:
    '''
    A blackjack hand
    attributes:
        cards - Card list
        value - total value of a deck
        aces -  total number of aces in hand
    '''
    def __init__(self) -> None:
        '''
        initialize an empty hand
        '''
        self.cards = []
        self.value = 0
        self.aces = 0
        
    def add_card(self, card : Card) -> None:
        '''
        add a card to the hand, and calulates it's value
        '''
        self.cards.append(card)
        self.value += card.value
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self) -> None:
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:
    '''
    players chips and bets
    attributes:
        total - total balance - int
        bet - current bet - int
    '''
    def __init__(self, total = 100) -> None:
        self.total = total
        self.bet = 0

    def win_bet(self) -> None:
        self.total += self.bet

    def lose_bet(self) -> None:
        self.total -= self.bet


def take_bet(chips : Chips) -> None:
    '''
    take a bet from player
    params:
        chips - player's chips - Chips
    '''
    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except ValueError:
            print("Sorry, a bet must be an integer ")
        else: 
            if chips.bet > chips.total:
                print("Your bet can't exceed ", chips.total)
            else:
                break

def hit(deck : Deck, hand : Hand) -> None:
    '''
    gets a new card from the deck
    '''
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck : Deck, hand : Hand) -> None:
    global playing 

    while True:
        x = input("Do you want to hit or stand? - type 'h' for hit and 's' for stand: ")
        if x[0].lower() == 'h':
            hit(deck, hand)
        elif x[0].lower() == 's':
            print("Player stands, dealer is playing")
            playing = False
        else:
            print("Sorry wrong input")
            continue
        break

def show_some(player : Hand, dealer : Hand ):
    print("\nDealer's Hand:")
    print(" <card hidden>")
    print('', dealer.cards[1])
    print("\nPlayer's Hand:", *player.cards, sep='\n ')

def show_all(player : Hand, dealer : Hand):
    print("\nDealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =",dealer.value)
    print("\nPlayer's Hand:", *player.cards, sep='\n ')
    print("Player's Hand =",player.value)

def player_busts(player : Hand, dealer : Hand, chips : Chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player : Hand, dealer : Hand, chips : Chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player : Hand, dealer : Hand, chips : Chips):
    print("Dealer busts!")
    chips.win_bet()

def dealer_wins(player : Hand, dealer : Hand, chips : Chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player : Hand, dealer : Hand):
    print("Dealer and Player tie! It's a push.")


if __name__ == "__main__":
    while True:
        print("Welcome to BlackJack! Get as close to 21 as you can without going over!\n\
            Dealer hits until he reaches 17. Aces count as either 1 or 11.")

        # initialize game card deck
        deck = Deck()
        deck.shuffle()

        # deal player's hand
        player_hand = Hand()
        player_hand.add_card(deck.deal())
        player_hand.add_card(deck.deal())
        player_chips = Chips()

        # deal dealer's hand
        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # take player's bet
        take_bet(player_chips)        

        # show cards
        show_some(player_hand, dealer_hand)

        while playing:

            # prompt for player to hit or stand
            hit_or_stand(deck, player_hand)

            # show cards 
            show_some(player_hand, dealer_hand)

            # if player's hand exceed's 21, run player_busts and break
            if player_hand.value > 21:
                player_busts(player_hand, dealer_hand)
                break
        
        # if player didn't bust
        if player_hand.value <= 21:

            # while dealer's hand < 17 keep hittin
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)
            
            # show all cards
            show_all(player_hand, dealer_hand)

            if dealer_hand.value > 21:
                dealer_busts(player_hand, dealer_hand, player_chips)
            
            elif dealer_hand.value > player_hand.value:
                dealer_wins(player_hand, dealer_hand, player_chips)
            
            elif dealer_hand.value < player_hand.value: 
                player_wins(player_hand, dealer_hand, player_chips)

            else:
                push(player_hand, dealer_hand)

        # Inform player of their total chips
        print("\nPlayer's winnings stand at", player_chips.total)

        # ask to play again
        new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
        while new_game.lower() not in ['y','n']:
            new_game = input("Would you like to play another hand? Enter 'y' or 'n' ")
        
        if new_game[0].lower() == 'y':
            playing = True
            continue
        else:
            print("Thanks for playing!")
            break