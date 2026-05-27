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

    @abstractmethod
    def add_player(self, player):
        """Adds a player to the game."""
        pass

    @abstractmethod
    def next_turn(self):
        """Advances to the next turn/player."""
        pass

    @abstractmethod
    def get_current_player(self):
        """Returns the player whose turn it currently is."""
        pass

    @abstractmethod
    def get_all_players(self):
        """Returns a list of all players."""
        pass
