from abc import ABC, abstractmethod


class GameManager(ABC):

    def __init__(self):
        self.game = None

    def set_game(self, game):
        self.game = game
        self.post_init()    # initialise whatever is specific to the match type

    @abstractmethod
    def set_dictionary(self, word_dictionary):
        self.wordDictionary = word_dictionary

    @abstractmethod
    def post_init(self):
        pass

    @abstractmethod
    def end_game(self):
        self.game.status = Finished


class GameTurnTemplate(ABC):

    @abstractmethod
    def validate_word(self, playerWord):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def calculate_word_score(self, word):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass

    @abstractmethod
    def game_summary(self):
        """Primitive operation. You HAVE TO override me, I'm a placeholder."""
        pass