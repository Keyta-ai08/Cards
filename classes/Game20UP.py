from classes.DeckManager import DeckManager
from classes.Game import Game

class Game20UP(Game):
    def __init__(self):
        self.deck_manager = DeckManager(draw_amount=5)
        self._current_hand = []

    def draw_card(self):
        card = self.deck_manager.draw_card()
        if card:
            self._current_hand.append(card)
        return card

    def reset_game(self):
        self._current_hand.clear()
        self.deck_manager.reset_deck()

    def get_score(self):
        return sum(c["value"] for c in self._current_hand)

    def get_status(self):
        score = self.get_score()
        if score == 0:
            return "Ziehe eine Karte, um das Spiel zu starten!"
        elif score >= 20:
            return "Glückwunsch! Du hast das Ziel von 20 Punkten erreicht oder überschritten!"
        else:
            return f"Noch {20 - score} Punkte bis zum Ziel!"

    @property
    def current_hand(self):
        return self._current_hand
