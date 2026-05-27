class Player:
    def __init__(self, name: str, is_guest: bool = False):
        self.name = name
        self.is_guest = is_guest
        self.hand = []
        self.score = 0
        self.has_finished_turn = False
        
    def add_card(self, card):
        self.hand.append(card)
        self.calculate_score()
        
    def calculate_score(self):
        self.score = sum(c["value"] for c in self.hand)
        
    def reset(self):
        self.hand.clear()
        self.score = 0
        self.has_finished_turn = False
