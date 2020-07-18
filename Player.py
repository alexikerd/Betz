import numpy as np


class Player():
    
    def __init__(self,deckshape,human=False):
        
        self.wins = 0
        self.cards = 0
        self.points = 0
        self.round_points = 0
        self.human = human

        
        self.deckshape = deckshape
        self.hand = np.zeros(self.deckshape)
        self.reserve = np.zeros(self.deckshape)


        
    def reset(self):
        
        self.cards = 0
        self.round_points = 0
        
        self.hand = np.zeros(self.deckshape)
        self.reserve = np.zeros(self.deckshape)