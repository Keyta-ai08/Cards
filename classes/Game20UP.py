from classes.DeckManager import DeckManager
from classes.Game import Game
from classes.Player import Player

class Game20UP(Game):
    def __init__(self):
        self.deck_manager = DeckManager(draw_amount=5)
        self.players = []
        self.current_turn_index = 0
        self.game_over = False

    def draw_card(self):
        if self.game_over:
            return None
        current_player = self.get_current_player()
        if not current_player:
            return None
        card = self.deck_manager.draw_card()
        if card:
            current_player.add_card(card)
            if current_player.score >= 20:
                self.game_over = True
        return card

    def reset_game(self):
        for player in self.players:
            player.reset()
        self.deck_manager.reset_deck()
        self.current_turn_index = 0
        self.game_over = False

    def get_score(self):
        current_player = self.get_current_player()
        return current_player.score if current_player else 0

    def get_status(self):
        current_player = self.get_current_player()
        if not current_player:
            return "Warte auf Spieler..."
        
        score = current_player.score
        if score == 0:
            return "Ziehe eine Karte, um deinen Zug zu starten!"
        elif score >= 20:
            return f"Glückwunsch {current_player.name}! Du hast das Ziel erreicht und gewonnen!"
        else:
            return f"Noch {20 - score} Punkte bis zum Ziel!"

    @property
    def current_hand(self):
        current_player = self.get_current_player()
        return current_player.hand if current_player else []

    def add_player(self, player: Player):
        self.players.append(player)

    def next_turn(self):
        if self.game_over:
            return
        if self.players:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.players)

    def get_current_player(self):
        if self.players and 0 <= self.current_turn_index < len(self.players):
            return self.players[self.current_turn_index]
        return None

    def get_all_players(self):
        return self.players
