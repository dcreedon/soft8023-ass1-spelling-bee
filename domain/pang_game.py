from datatype.enums import GameStatus
from domain import player_record
import uuid


class PangGame:

    def __init__(self):
        self.gameid = ''
        self.players = {}
        self.total_score = 0
        self.letters = []
        self.centre_letter = ''
        self.found_words = {} #dictionary to prevent duplicates holds word and associated score
        self.invite_code = ''


    def register_player(self, playerName):
        new_player = player_record.PlayerRecord()
        new_player.playerName = playerName
        playerId = uuid.uuid4()             #unique player id
        self.players[playerId] = new_player
        return playerId

    def add_letters(self, letters):
        self.letters = list(set(letters)) # only add unique letters

    def add_centre_letter(self, letter):
        self.centre_letter = letter

    def put_centre_in_middle(self):
        centre_position = 3
        centre_letter_position = self.letters.index(self.centre_letter)
        if (self.letters[centre_position] != self.centre_letter) :
            self.letters[centre_letter_position] = self.letters[centre_position]
            self.letters[centre_position] = self.centre_letter

    def add_found_word(self, word, word_score):
        self.found_words[word] = word_score

    def is_found_word(self,word):
        check_result = self.found_words.get(word)  # caters for where no key found
        if check_result:
            return True
        return False

    def update_total_score(self, score):
        self.total_score += score

    def add_invite_code(self, invite_code):     # stores the games invite code
        self.invite_code = invite_code

    def update_player_record(self, word, total_word_score, playerId):       # update the individual player record with the word and score
        self.players[playerId].words[word]=total_word_score

    def set_gameid(self, gameid):
        self.gameid = gameid

