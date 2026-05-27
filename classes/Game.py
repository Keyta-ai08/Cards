from abc import ABC, abstractmethod

class Game(ABC):
    @abstractmethod
    def draw_card(self):
        """Draws a card and processes game rules."""
        pass

    @abstractmethod
    def reset_game(self):
        """Resets the game state to its initial configuration."""
        pass

    @abstractmethod
    def get_score(self):
        """Returns the current score."""
        pass

    @abstractmethod
    def get_status(self):
        """Returns the current game status message."""
        pass
    
    @property
    @abstractmethod
    def current_hand(self):
        """Returns the current hand of cards."""
        pass
