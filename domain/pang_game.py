from datatype.enums import GameStatus


class PangGame:

    def __init__(self):
        self.status = GameStatus.INVALID
        self.players = []
        self.total_score = 0
        self.letters = []
        self.centre_letter = ''
        self.found_words = {} #dictionary to prevent duplicates holds word and associated score

    def register_player(self, username):
        if username not in self.players:
            index = len(self.players)
            self.players.append(username)
            return index
        else:
            return -1

    def add_letters(self, letters):
        self.letters = list(set(letters)) # only add unique letters


    def add_centre_letter(self, letter):
        self.centre_letter = letter

    def add_found_word(self, word, word_score):
        self.found_words[word] = word_score

    def is_found_word(self,word):
        check_result = self.found_words.get(word)  # caters for where no key found
        if check_result:
            return True
        return False

    def update_total_score(self, score):
        self.total_score += score
