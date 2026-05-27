class Player:
    def __init__(self, name: str, score, is_guest: bool = False):
        self.name = name
        self.is_guest = is_guest
        self.hand = []
        self.score = score  
        self.has_finished_turn = False
        self.tricks_won = 0 # Tricks won in the current round
        
    def add_card(self, card):
        self.hand.append(card)
        
    def calculate_score(self):
        # We don't recalculate based on hand values in 20-UP anymore
        pass
        
    def reset(self):
        self.hand.clear()
        self.has_finished_turn = False
        self.tricks_won = 0
        
    def reset_score(self):
        self.score = 20
