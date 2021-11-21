from service.game_service import GameTurnTemplate
from service.game_service import GameManager
from app.server import word_dictionary
from datatype.enums import GameStatus

class PangGame(GameManager, GameTurnTemplate):

    def __init__(self):
        super().__init__()

    def post_init(self):
        self.pangram_dictionary = self.wordDictionary.create_pangram_dict()
        self.game.add_letters(word_dictionary.GameDictionary.random_word(self.pangram_dictionary))  # choose the word/letters from the pangram dictionary
        self.game.add_centre_letter(word_dictionary.GameDictionary.random_letter(self.game.letters))     # choose the centre letter from the word
        self.game.put_centre_in_middle() # put the centre letter in the middle of the list

    def set_dictionary(self, word_dictionary):
        self.wordDictionary = word_dictionary

    def validate_word(self, playerWord, playerId):
        """
        Check
        1. 4 letters long
        2. doesn't contain an s
        3. contains centre letter
        4. contains only letters from the ones provided
        5. Is a word
        6. Is not already a used word

        if success output the result and score for the word
        if not then output the appropriate error and score

        TODO:check for non alpha chars

        """

        playerWord = playerWord.lower()  #convert all letters in word to lower case

        if len(playerWord) < 4:
            response = "Sorry the word you entered is less than 4 letters long, words of four or more letters please!"
            return response
        elif (word_dictionary.GameDictionary.letter_in_word(playerWord, "s")) :
            response = "Sorry the word you entered contains the letter S no S's please !"
            return response
        elif (word_dictionary.GameDictionary.letter_in_word(playerWord, self.game.centre_letter)) is False :
            response = "Sorry the word does not contain the centre letter : " + self.game.centre_letter.upper()
        elif (word_dictionary.GameDictionary.letters_in_word(playerWord, self.game.letters)) is False :
            response = "Sorry the word [ " + playerWord  + " ] contains letters other than these : " + str(self.game.letters)
        elif (self.wordDictionary.is_word(playerWord) is False) :
            response = "Sorry the word [ " + playerWord  + " ] is not a word in the dictionary. "
        elif (self.game.is_found_word(playerWord)) :
            response = "Sorry the word [ " + playerWord + " ] has already been found :-( "
        else:
            response = self.calculate_word_score(playerWord, playerId)

        return response

    def calculate_word_score(self, word, playerId):
        """
        If checks passed calculate score:
        1. Calculate base score
        2. Calculate bonus score - Is it a pangram?
        3. Add base + bonus and update total for game along with word and score for word

        """

        bonus_score = 0
        bonus_message = ""

        if len(word) == 4:
            base_score = 1
        else:
            base_score = len(word)

        print("Base Score: " + str(base_score))

        if (word_dictionary.GameDictionary.is_pangram(word)) :
            bonus_score = 7
            print("Bonus Score: " + str(bonus_score))
            bonus_message = "It's a Pangram! Bonus Score is: " + str(bonus_score)

        total_word_score = base_score + bonus_score
        print("Total Word Score: " + str(total_word_score))

        self.game.add_found_word(word, total_word_score)

        self.game.update_total_score(total_word_score)

        self.game.update_player_record(word, total_word_score, playerId)      # record word player played and score.

        response = bonus_message + " Valid word Score is : " + str(total_word_score)

        return response

    def game_summary(self):
        # output the letters, current score
        line_break ="\n"
        # construct the letter output and enclose the centre letter with []
        letters = "Letters : "
        for letter in self.game.letters:
            if letter == self.game.centre_letter :
                letters += "[" + letter.upper() + "]"
            else:
                letters += "  " + letter.upper() + " "

        current_score = "Total Score : " + str(self.game.total_score)

        summary = line_break + letters + line_break + current_score

        return summary

    def word_score_summary(self):
        # output the words and their score and total score
        line_break ="\n"
        # construct the output
        words = "Word Scores : " + line_break
        for word in self.game.found_words:
            words += str(word) + " scored " + str(self.game.found_words[word]) + " points" + line_break

        total_score = "Total Score : " + str(self.game.total_score) + line_break

        summary = line_break + words + total_score

        return summary

    def player_word_score_summary(self):
        # output the words and their score and total score for each player
        line_break ="\n"
        # construct the output
        player_points = 0
        words = ''
        score = ''
        summary = ''

        summary = line_break + "Total Game Score: " + str(self.game.total_score) + line_break
        for player in self.game.players:
            score += "Player: " + self.game.players[player].playerName + line_break + " scored "
            for word in self.game.players[player].words:
                words += "Word - " + str(word) + " scored " + str(self.game.players[player].words[word]) + " points" + line_break
                player_points += self.game.players[player].words[word]
            score += str(player_points) + " points" + line_break
            all_output = line_break + score + words
            score = ''
            words = ''
            player_points = 0
            summary += all_output

        return summary

    def end_game(self):
        response = "bye"
        return response


class PangGameBuilder:
    """
    This could be extended to include dynamic key-value pair parameters (see object_factory.py),
    or make it a singleton, etc.
    """
    def __init__(self):
        pass

    def __call__(self):
        return PangGame()
