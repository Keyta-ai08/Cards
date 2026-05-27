from classes.DeckManager import DeckManager
from classes.Game import Game
from classes.Player import Player
from classes.CardUtils import get_card_suit_and_value, is_trump, compare_cards

class Game20UP(Game):
    # Game States
    DEALING_3 = "DEALING_3"
    WAITING_FOR_TRUMP = "WAITING_FOR_TRUMP"
    DEALING_2 = "DEALING_2"
    PLAYING_TRICK = "PLAYING_TRICK"
    ROUND_EVALUATION = "ROUND_EVALUATION"
    GAME_OVER = "GAME_OVER"

    def __init__(self):
        # Wir brauchen nur 32 Karten (7 bis Ass), der DeckManager hat vermutlich mehr. 
        # Wir behelfen uns hier: Beim Deck reset filtern wir aus, falls nötig.
        self.deck_manager = DeckManager(draw_amount=5)
        self.players = []
        self.current_turn_index = 0
        
        self.state = self.DEALING_3
        self.dealer_index = 0
        self.vorhand_index = 0
        
        self.trump_suit = None
        self.current_trick = [] # List of tuples: (player, card)
        self.lead_suit = None
        
        self.winner = None

    def _get_active_players(self):
        return [p for p in self.players if p.score > 0]

    def start_round(self):
        if self.state == self.GAME_OVER:
            return
            
        for player in self.players:
            player.reset()
            
        # Filtern auf 32 Karten (ohne 2,3,4,5,6)
        self.deck_manager.reset_deck()
        self.deck_manager.available_cards = [
            c for c in self.deck_manager.all_cards 
            if not c["name"].split(" ")[1] in ["2", "3", "4", "5", "6"]
        ]
        
        # Vorhand ermitteln (nächster aktiver Spieler nach Geber)
        self.vorhand_index = (self.dealer_index + 1) % len(self.players)
        
        self.current_trick = []
        self.lead_suit = None
        self.trump_suit = None
        
        # Gebe 3 Karten an alle
        for _ in range(3):
            for i in range(len(self.players)):
                # Wir geben von Vorhand aus
                p_idx = (self.vorhand_index + i) % len(self.players)
                card = self.deck_manager.draw_card()
                if card:
                    self.players[p_idx].add_card(card)
                    
        self.state = self.WAITING_FOR_TRUMP
        self.current_turn_index = self.vorhand_index

    def set_trump(self, suit: str):
        if self.state != self.WAITING_FOR_TRUMP:
            return
            
        self.trump_suit = suit
        self.state = self.DEALING_2
        
        # Gebe restliche 2 Karten
        for _ in range(2):
            for i in range(len(self.players)):
                p_idx = (self.vorhand_index + i) % len(self.players)
                card = self.deck_manager.draw_card()
                if card:
                    self.players[p_idx].add_card(card)
                    
        self.state = self.PLAYING_TRICK
        self.current_turn_index = self.vorhand_index

    def can_play_card(self, player: Player, card) -> bool:
        if not self.current_trick:
            return True # Ausspielen: alles erlaubt
            
        card_suit, val = get_card_suit_and_value(card["name"])
        is_card_trump = is_trump(card["name"], self.trump_suit)
        
        # Wenn die Karte Trumpf ist, behandeln wir sie wie die Trumpffarbe
        effective_suit = self.trump_suit if is_card_trump else card_suit
        
        # Was wurde angespielt?
        lead_card = self.current_trick[0][1]
        lead_suit, lead_val = get_card_suit_and_value(lead_card["name"])
        is_lead_trump = is_trump(lead_card["name"], self.trump_suit)
        effective_lead_suit = self.trump_suit if is_lead_trump else lead_suit
        
        # Wenn man bedienen kann
        if effective_suit == effective_lead_suit:
            return True
            
        # Hat der Spieler die angespielte Farbe auf der Hand?
        has_lead_suit = False
        for c in player.hand:
            c_suit, c_val = get_card_suit_and_value(c["name"])
            c_is_trump = is_trump(c["name"], self.trump_suit)
            c_eff_suit = self.trump_suit if c_is_trump else c_suit
            if c_eff_suit == effective_lead_suit:
                has_lead_suit = True
                break
                
        # Wenn er sie hat, MUSS er sie spielen (und das hat er laut vorherigem if nicht getan)
        if has_lead_suit:
            return False
            
        # Wenn er sie nicht hat, darf er abwerfen/stechen
        return True

    def play_card(self, player: Player, card):
        if self.state != self.PLAYING_TRICK:
            return False
            
        if player != self.get_current_player():
            return False
            
        if not self.can_play_card(player, card):
            return False
            
        player.hand.remove(card)
        self.current_trick.append((player, card))
        
        if len(self.current_trick) == len(self.players):
            self.state = self.ROUND_EVALUATION
            return True
            
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        return True

    def evaluate_trick(self):
        """Called by UI after a short delay"""
        if self.state != self.ROUND_EVALUATION:
            return
            
        lead_card = self.current_trick[0][1]
        lead_suit, lead_val = get_card_suit_and_value(lead_card["name"])
        if is_trump(lead_card["name"], self.trump_suit):
            lead_suit = self.trump_suit
            
        best_player = self.current_trick[0][0]
        best_card = self.current_trick[0][1]
        
        for p, c in self.current_trick[1:]:
            if compare_cards(c["name"], best_card["name"], lead_suit, self.trump_suit) > 0:
                best_card = c
                best_player = p
                
        best_player.tricks_won += 1
        
        self.current_trick.clear()
        
        # Nächster Stich oder Rundenende?
        if not self.players[0].hand:
            self.evaluate_round()
        else:
            self.state = self.PLAYING_TRICK
            # Gewinner spielt aus
            self.current_turn_index = self.players.index(best_player)
            
    def evaluate_round(self):
        multiplier = 2 if self.trump_suit == "Kreuz" else 1
        
        for p in self.players:
            if p.tricks_won == 0:
                p.score += 5 * multiplier
            else:
                p.score -= p.tricks_won * multiplier
                
            if p.score <= 0:
                self.state = self.GAME_OVER
                if not self.winner or p.score < self.winner.score:
                    self.winner = p
                    
        if self.state != self.GAME_OVER:
            self.dealer_index = (self.dealer_index + 1) % len(self.players)
            self.start_round()

    def draw_card(self):
        pass # Not used anymore

    def reset_game(self):
        for player in self.players:
            player.reset_score()
        self.winner = None
        self.dealer_index = 0
        self.state = self.DEALING_3
        self.start_round()

    def get_score(self):
        current_player = self.get_current_player()
        return current_player.score if current_player else 0

    def get_status(self):
        if self.state == self.GAME_OVER:
            return f"Spiel beendet! Gewinner: {self.winner.name}"
        if self.state == self.WAITING_FOR_TRUMP:
            return "Vorhand muss den Trumpf wählen!"
        if self.state == self.PLAYING_TRICK:
            return "Wähle eine Karte zum Ausspielen."
        if self.state == self.ROUND_EVALUATION:
            return "Stich wird ausgewertet..."
        return "..."

    @property
    def current_hand(self):
        current_player = self.get_current_player()
        return current_player.hand if current_player else []

    def add_player(self, player: Player):
        self.players.append(player)

    def next_turn(self):
        pass # Removed as manual turn progression is not needed in trick taking.

    def get_current_player(self):
        if self.players and 0 <= self.current_turn_index < len(self.players):
            return self.players[self.current_turn_index]
        return None

    def get_all_players(self):
        return self.players
