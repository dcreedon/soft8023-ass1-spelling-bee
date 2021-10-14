import random
from random import randint

import json


class GameDictionary:

    def __init__(self):
        super().__init__()

    def post_init(self):
        pass

    def load_words(self, dictionary_file):
        with open(dictionary_file) as json_file:
            self.words = json.load(json_file)

            print("Loading word file...")

    def create_pangram_file(self, words, pangram_file):
        pangrams = {}
        for word in words:
            if self.is_pangram(self, word):
                pangrams[word] = ""

        with open(pangram_file, "w") as pangram_file:
            json.dump(pangrams, pangram_file)
            print("Writing Pangram file...")

    def create_pangram_dict(self):
        pangrams = {}
        for word in self.words:
            if self.is_pangram(word):
                pangrams[word] = ""

        return pangrams

    def is_word(self, word):
        check_result = self.words.get(word)  # caters for where no key found
        if check_result:
            return True
        return False

    @staticmethod
    def letter_in_word(word, letter):
        if letter in word:
            return True
        return False

    @staticmethod
    def letters_in_word(word, letters):

        for letter in set(word):
            if letter in letters:
                check = True
            else:
                return False
        return check

    @staticmethod
    def random_word(word_list):
        rand_num = randint(0, len(word_list))
        random_word = list(word_list.keys())[rand_num]
        print("Random Word : " + random_word)
        return random_word

    @staticmethod
    def random_letter(word):
        random_letter= random.choice(word)
        print("Random Letter : " + random_letter)
        return random_letter

    @staticmethod
    def is_pangram(word_in):
        if len(set(word_in)) == 7 and 's' not in word_in:  # set provides a unique list of letters
            return True
        else:
            return False
