from secrets import randbelow as rb
from os import system as sys


SHUFFLE_COUNT = 7
GREETINGS = '\t\tWelcome to Jacks or Better Draw Poker\n' +\
            '\t\t\t  Created by Arlo Gittings\n'
COMMANDS = ['\t\t   Press (D)eal, (E)xit ', '\t\tPress (H)old, (D)raw, (E)xit']
BET = 5

score = 200
card_deck = [\
    'A \u2664', 'K \u2664', 'Q \u2664', 'J \u2664', '10 \u2664', '9 \u2664', '8 \u2664', '7 \u2664', '6 \u2664','5 \u2664', '4 \u2664', '3 \u2664', '2 \u2664',\
    'A \u2665', 'K \u2665', 'Q \u2665', 'J \u2665', '10 \u2665', '9 \u2665', '8 \u2665', '7 \u2665', '6 \u2665','5 \u2665', '4 \u2665', '3 \u2665', '2 \u2665',\
    'A \u2666', 'K \u2666', 'Q \u2666', 'J \u2666', '10 \u2666', '9 \u2666', '8 \u2666', '7 \u2666', '6 \u2666','5 \u2666', '4 \u2666', '3 \u2666', '2 \u2666',\
    'A \u2667', 'K \u2667', 'Q \u2667', 'J \u2667', '10 \u2667', '9 \u2667', '8 \u2667', '7 \u2667', '6 \u2667','5 \u2667', '4 \u2667', '3 \u2667', '2 \u2667',\
    ]

class Card(object):
    def __init__(self, pips, suit):
        self.pips = pips
        self.suit = suit
        self.hold = False

    def get_pips(self):
        if len(self.pips) == 1:
            self.pips += ' '
        return self.pips

    def get_suit(self):
        return self.suit

    def get_value(self, pip):
        face_values = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}
        if pip in face_values:
            return face_values[pip]
        else:
            return int(pip)

    def __str__(self):

        return self.get_pips() + self.get_suit()

def seed_deck(card_deck):
    '''
    Description:
        Randomize cards
    Expects:
        card_deck: (list) all cards in a particular order.
    Reutrns:
        cd: (list) all cards after randomization. 
    '''    
    
    cd=[]
    for card in card_deck:
        v=tuple(card.split())
        cd.append(Card(v[0],v[1]))
    
    deck_size = len(cd)
    for i in range(SHUFFLE_COUNT):
        for element in range(deck_size):
            swap_element=rb(deck_size)
            cd[swap_element], cd[element] = cd[element], cd[swap_element]
    return cd

class Hand(object):
    def __init__(self):
        self.hand = []
        self.hold = []
        self.score = score
        self.size = 5
        self.draws = 0
        self.top_card = 0

    def get_score(self):
        return self.score        
    
    def clear_held(self):
        self.hold = []

    def get_held(self):
        return self.hold

    def deal (self, card_deck):
        '''
        Description:
            create a list that is loaded with cards from a card_deck
        Expects:
            card_deck: (list) a randomized list of cards
            hand_size: (int) the number of cards to be dealt per hand.
            num_hands: (int) the number of hands to be dealt.
        Returns:
            hands: (list) a list of lists containing each of the hands dealt. 
        '''
        if self.score == 0:
            self.score = 200
        self.score-=BET
        self.hand = []
        for card in range(self.size):
            self.hand.append(card_deck[self.top_card])
            self.top_card += 1

        
    def hold_selection(self):
        select = True
        while select:
            try:
                response=int(input('Select card to toggle hold: 0-4\nLeave blank to draw').strip())
            except ValueError:
                    select = False
            else:
                print(response)
                if response < 5 and response > -1 and response not in self.hold:
                    self.hold.append(response)
                elif response > 4 or response < 0:
                    print('That input is out of range.')
                elif response in self.hold:
                    self.hold.remove(response)
            show_score(self.get_held(), self.get_score())
            self.show()
        self.draws += 1
        

    def draw(self, card_deck):
        for i in range(self.size):
            print(i not in self.hold, end='\t')
            sys('sleep 3')
            print(self.hand[i],end=' ')
            if i not in self.hold:
                self.hand[i]=card_deck[self.top_card]
                self.top_card += 1
            print(self.hand[i])

    def show(self):
        print('|   ', end='')
        for card in self.hand:
            print(card, end='   |   ')
        print('\n|',end='')
        for i in range(len(self.hand)):
            print('___ {} ___|' .format(i), end='')
        print('\n')
    
    def update_score(self):
        suits=[]
        pips={}
        face='JQKA'
        winners = {
            'pair': False,
            'jacks_or_better': False,
            'two_pair': False,
            'three_of_a_kind': False,
            'straight': False,
            'flush': False,
            'full_house': False,
            'four_of_a_kind': False,
            'straight_flush': False,
            'royal_flush': False
            }
        payouts = {
            'royal_flush': ('Royal Flush: ', 800),
            'straight_flush': ('Straight Flush: ', 50),
            'four_of_a_kind': ('Four of a Kind: ', 25),
            'full_house': ('Full House: ', 9),
            'flush': ('Flush: ', 6),
            'straight': ('Straight: ', 4),
            'three_of_a_kind': ('Three of a Kind: ', 3),
            'two_pair': ('Two Pair: ', 2),
            'jacks_or_better': ('Jacks or Better: ', 1)
            }    

        values=[]
        for card in self.hand:
            if card.get_suit() not in suits:
                suits.append(card.get_suit())
            if card.get_pips() not in pips:
                pips[card.get_pips()] = 1
            else:
                pips[card.get_pips()] += 1
        for pip in pips:
            values.append(card.get_value(pip.strip()))
            if pips[pip] == 4:
                winners['four_of_a_kind'] = True
            elif pips[pip] == 3:
                if winners['pair'] or winners['jacks_or_better']:
                    winners['pair'] = False
                    winners['jacks_or_better'] = False
                    winners['full_house'] = True
                else:
                    winners['three_of_a_kind'] = True
            elif pips[pip] == 2:
                if winners['pair'] or winners['jacks_or_better']:
                    winners['pair'] = False
                    winners['jacks_or_better'] = False
                    winners['two_pair'] = True
                elif pip.strip() in face:
                    winners['jacks_or_better'] = True
                else:
                    winners['pair'] = True
            elif len(values) == 5:
                if max(values)-min(values) == 4:
                    winners['straight'] = True
                elif 14 in values:
                    values.sort()
                    values[-1]=1
                    if max(values)-min(values) == 4:
                        winners['straight'] = True
        if len(suits) == 1:
            if  winners['straight']:
                winners['straight'] = False
                if min(values) == 10:
                    winners['royal_flush'] = True
                else:
                    winners['straight_flush'] = True
            else:
                winners['flush'] = True

        for win in winners:
            if winners[win]:
                if win in payouts:
                    self.score+=payouts[win][1]*BET
                    print(payouts[win][0], payouts[win][1]*BET)
        
                


def show_score(held,score):
    '''
    Description:
        clear the screen and print the current available tokens
    Expects:
        score: (int) number of tokens
    Returns:
        None
    '''
    goopy = sys('clear')
    for count in range(5):
        if count in held:
            print('|   HOLD  ', end='')
        else:
            print('|         ', end='')
    print('| Credits: {}\n'.format(score)+'|_________'*5+'|')

def play_game():
    print(GREETINGS)
    response='D'
    hand = Hand()
    while response.upper() != 'E':
        deck = seed_deck(card_deck)
        
        hand.deal(deck)
        show_score(hand.get_held(), hand.get_score())
        hand.show()
        
        if hand.draws:
            response=input(COMMANDS[0])
        else:
            response=input(COMMANDS[1])
        if response.upper() == 'H' and not hand.draws:
            hand.clear_held()
            show_score(hand.get_held(), hand.get_score())
            hand.show()
            hand.hold_selection()
            hand.draw(deck)
            hand.update_score()
            show_score(hand.get_held(), hand.get_score())
            hand.show()
            
        else:
            hand.update_score()
        

play_game()