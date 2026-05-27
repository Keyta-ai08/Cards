import json
import random

from pathlib import Path


CARD_FILE = Path("assets/cards.json")

class DeckManager:
    def __init__(self, draw_amount: int = 5):
        self.draw_amount = draw_amount
        self.all_cards = []
        self.available_cards = []
        self.load_cards()

    def load_cards(self) -> dict:
        try:
            with open(CARD_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "cards" in data:
                    self.all_cards = data["cards"]
                    self.available_cards = list(self.all_cards)
                    print(f"Cards geladen! {len(self.all_cards)} Karten vorhanden.")
                    return data
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Keine cards.json gefunden oder ungültig! {e}")
        self.all_cards = []
        self.available_cards = []
        return {"cards": []}

    def draw_card(self):
        if not self.available_cards:
            self.reset_deck()
        if self.available_cards:
            card = random.choice(self.available_cards)
            self.available_cards.remove(card)
            return card
        return None

    def reset_deck(self):
        self.available_cards = list(self.all_cards)

    def deck_event_manager(self, availible_cards=None, cards=None, card=None, event="draw"):
        if event == "draw":
            return self.draw_card()
        print(f"Error: Unbekanntes Event {event}\n")
        return None