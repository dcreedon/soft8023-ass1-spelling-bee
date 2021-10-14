import logging
import time
from concurrent import futures

import grpc
import uuid

from app.gameimpl import pang
from domain import pang_game

from pangram_game_pb2 import GameResponse, CheckWordResponse, StartGameResponse

from pangram_game_pb2_grpc import PangramGameServicer, add_PangramGameServicer_to_server
from pattern import object_factory

from app.server.game_registry import GameRegistry
from app.server.word_dictionary import GameDictionary


class GameServer(PangramGameServicer):

    def __init__(self):

        self.game_type = "PANG"
        self.factory = object_factory.ObjectFactory()
        self.factory.register_builder('PANG', pang.PangGameBuilder())
        self.registry = GameRegistry.get_instance()
        self.word_dictionary = GameDictionary()
        self.word_dictionary.load_words("words_dictionary.json")

    def CreateGame(self, request, context):
        """
        setup the game instance store it inthe registry, set the game dictionary
        """
        print("Creating Game")
        new_game = self.factory.create(request.gameType)
        game = pang_game.PangGame()  #game instance for game registry to hold game state
        game.register_player(request.playerName)
        new_game.set_dictionary(self.word_dictionary)
        new_game.set_game(game)
        game_id = self.registry.add_game(new_game)  #add the new game instance to the registry and get a unique game id
        print("Game Id : " + str(game_id.bytes))
        return GameResponse(gameId=game_id.bytes)  #return the unique game id to the client

    def StartGame(self, request, context):
        """
        return the starting state of the game, starting score and letters
        """
        new_game = self.registry.get_game(request.gameId)

        response = new_game.game_summary()
        print("Start Game Response : " + response)

        return StartGameResponse(message=response)

    def CheckWord(self, request, context):
        """
        Checks if a word is valid, isn't already used, calculates the score for the word
        """
        print("Player entered word : " + request.playerWord)

        new_game = self.registry.get_game(request.gameId)

        word_check = new_game.validate_word(request.playerWord)
        print("Word Check Response : " + word_check)

        game_summary = new_game.game_summary()
        print("Game Status Response : " + game_summary)

        return CheckWordResponse(gameStatusMessage=game_summary, wordCheckMessage=word_check)

    def EndGame(self, request, context):
        return

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PangramGameServicer_to_server(GameServer(), server)
    server.add_insecure_port('[::]:50057')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Launching Game Server...")
    logging.basicConfig()
    serve()