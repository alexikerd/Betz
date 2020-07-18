import numpy as np
# import torch
# import torch.nn.functional as F

from Player import Player



       
        

class CardGame():
    
    def __init__(self,deckshape,handsize,numplayers,dealer=None):
        
        
        self.game_over = False
        self.round_over = False
        
        self.deckshape = deckshape
        self.handsize = handsize
        self.numplayers = numplayers
        
        self.deck = np.ones(self.deckshape)
        self.discard = np.zeros(self.deckshape)
        self.table = np.zeros(self.deckshape)

        self.playerlist = [Player(self.deckshape) for _ in range(self.numplayers)]
        self.dealer = np.random.randint(0,4) if dealer is None else dealer
        self.turn = 0
        self.suit = None
        self.winning_round = None
        
        for player in self.playerlist:
            
            player.hearts = 0
            player.qos = 0
        
                

 
    def reset(self):
        
        self.deck = np.ones(self.deckshape)
        self.discard = np.zeros(self.deckshape)
        self.suit = None
        self.round_over = False

        for player in self.playerlist:

            player.reset()        
   
        self.game_specific_reset()
    
            
            
    def deal(self,dealing_player):
        
        for i in range(self.handsize * self.numplayers):
            
            a,b = self.random_card(self.deck)
            
            self.playerlist[(i+dealing_player)%self.numplayers].hand[a,b] = 1
            self.deck[a,b] = 0
            
            self.playerlist[(i+dealing_player)%self.numplayers].cards += 1
    
    def game_specific_reset():
        
        pass
            
            
    def random_card(self,pile):
        
        available_cards = np.nonzero(pile)
        pulled_card = np.random.randint(0,len(available_cards[0]))
        
        return available_cards[0][pulled_card], available_cards[1][pulled_card]
    
 
    def get_pile(self,pile):
    
        available_cards = np.nonzero(pile)
        
        return np.array((available_cards[0],available_cards[1]))


class Hearts(CardGame):
    
    def __init__(self):
        super().__init__((4,13),13,4)
        
        self.hearts_broken = False
        self.first_round = True
        self.shoot_the_moon = None
        
        for player in self.playerlist:
            
            player.hearts = 0
            player.queen_of_spades = 0
        
        
    def game_specific_reset(self):
        
        self.hearts_broken = False
        self.first_round = True
        self.shoot_the_moon = None
        
        
    def check_for_2clubs(self):
        
        for i,player in enumerate(self.playerlist):
            
            if player.hand[3,0]==1:
                
                return i
            
        
        return None
    
    
    def choose_card(self,player):
        
        
        if player.human:
            
            pass
        
        else:
            
            if self.suit==None:

                return self.random_card(player.hand)

            else:

                if np.sum(player.hand[self.suit])==0:

                    return self.random_card(player.hand)

                else:

                    available_moves = player.hand.copy()
                    available_moves[:self.suit] = 0
                    available_moves[self.suit+1:] = 0

                    return self.random_card(available_moves)
   
    
    
    def play_round(self):
        
       
        previous_b = -1
        self.winning_round = None
        
        
        if self.first_round:
            
            self.deal(self.dealer)
            self.dealer = (self.dealer + 1)%self.numplayers
            
            self.turn = self.check_for_2clubs()

            self.playerlist[self.turn].hand[3,0] = 0
            self.table[3,0] = 1
            
            self.first_round = False
            self.suit = 3
            previous_b = 0
            self.winning_round = self.turn
            
            self.turn = (self.turn + 1)%self.numplayers
            
        while np.sum(self.table)<self.numplayers:
            
            
            a,b = self.choose_card(self.playerlist[self.turn])
            
            if self.suit==None:
                
                self.suit = a
        
            self.playerlist[self.turn].hand[a,b] = 0
            self.table[a,b] = 1
            
            if a==self.suit:
                
                if b>previous_b:
                    
                    previous_b = b
                    self.winning_round = self.turn
                    

                    
                    
            
            self.turn = (self.turn + 1)%self.numplayers
            
        self.playerlist[self.winning_round].reserve += self.table
        self.table = np.zeros(self.deckshape)
        self.turn = self.winning_round
        self.winning_round = None  
        self.suit = None
        
        if np.sum(self.playerlist[0].hand)==0:
            
            self.score_round()
            
            self.round_over = True
            
            
            
    def score_round(self):
        

        for i,player in enumerate(self.playerlist):
            
            player.hearts += np.sum(player.reserve[2])
            player.qos += player.reserve[1,10]
            player.round_points = np.sum(player.reserve[2]) + 13*player.reserve[1,10]
            
            if player.round_points==26:
                
                self.shoot_the_moon = i
                
        if self.shoot_the_moon!=None:
            
            for i,player in enumerate(self.playerlist):
                
                if i==self.shoot_the_moon:
                    
                    pass
                
                else:
                    
                    player.points += 26
                    
        else:
            
            for player in self.playerlist:
                
                player.points += player.round_points
            
            
        
        
        
                
        