import time
from concurrent import futures

import grpc
import uuid
import pika

from app.gameimpl import pang
from domain import pang_game

from pangram_game_pb2 import GameResponse, CheckWordResponse, StartGameResponse, JoinGameResponse, GameScoreResponse, EndGameResponse

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
        #setup rabbit MQ
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='mid-game-stats')


    def CreateGame(self, request, context):
        """
        setup the game instance store it in the registry, set the game dictionary
        generate the invite code for the game and store it in the registry
        """
        print("Creating Game")
        new_game = self.factory.create(request.gameType)
        game = pang_game.PangGame()  #game instance for game registry to hold game state
        player_id = game.register_player(request.playerName)
        new_game.set_dictionary(self.word_dictionary)
        new_game.set_game(game)
        game_id = self.registry.add_game(new_game)  #add the new game instance to the registry and get a unique game id
        game.set_gameid(game_id)                    # set the game ID in the game instance
        #generate invite code, store in game and also in registry for lookup
        invite_code  = str(game_id)[0:4]       # first four chars of game_id/uuid as the invite code
        game.add_invite_code(invite_code)       # store the invite code in the game instance
        self.registry.add_invite_code(invite_code, game_id)     # put the invite code in the regsitry along with the game id to allow lookup of associated game id

        print("Game Id : " + str(game_id))
        print("Invite Code: " + str(invite_code))
        return GameResponse(gameId=game_id.bytes, inviteCode=str(invite_code), playerId=player_id.bytes)  #return the unique game id and invite code to the client

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
        playerId = uuid.UUID(bytes=request.playerId)
        word_check = new_game.validate_word(request.playerWord,playerId)
        print("Word Check Response : " + word_check)

        game_summary = new_game.game_summary()
        print("Game Status Response : " + game_summary)

        return CheckWordResponse(gameStatusMessage=game_summary, wordCheckMessage=word_check)

    def JoinGame(self, request, context):
        game_id = self.registry.get_game_id_with_invite_code(request.inviteCode)

        new_game = self.registry.get_game_from_invite_code(game_id)
        player_id = new_game.game.register_player(request.playerName)
        response = new_game.game_summary()
        print("Start Game Response : " + response)
        return JoinGameResponse(gameId=game_id.bytes, message=response, playerId=player_id.bytes)

    def GameScore(self, request, context):
        new_game = self.registry.get_game(request.gameId)
        message = new_game.player_word_score_summary()
        gamestats = new_game.game_stats()
        #send stats to rabbit message queue - easier to test

        print("Game Status sent to RabbitMQ: " +  gamestats)
        self.channel.basic_publish(exchange='', routing_key='mid-game-stats', body=gamestats)
        #close rabbit mq connection
        #self.connection.close()
        return GameScoreResponse(message=message)

    def EndGame(self, request, context):
        new_game = self.registry.get_game(request.gameId)
        message = new_game.player_word_score_summary()

        return EndGameResponse(message=message)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_PangramGameServicer_to_server(GameServer(), server)
    server.add_insecure_port('[::]:50057')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Launching Game Server...")
    serve()