import logging

import grpc

import pangram_game_pb2 as pangram_game_pb2
import pangram_game_pb2_grpc as pangram_game_pb2_grpc

game_server_address = '127.0.0.1:50057'


def run():
    channel = grpc.insecure_channel(game_server_address)
    print("connecting")
    stub = pangram_game_pb2_grpc.PangramGameStub(channel)

    # New Game or join existing
    game_choice = input("New game (n) or join existing (e) : ")
    player_name = input("Enter your first name : ")

    if game_choice == "n":
        print("starting a new game")
        # Initialise new Game
        gameId = stub.CreateGame(pangram_game_pb2.GameRequest(playerName=player_name, gameType='PANG')).gameId

        # Start the new Game Loop
        print("starting new game loop")
        print("(ex) to exit game")

        print(stub.StartGame(pangram_game_pb2.StartGameRequest(gameId=gameId)).message)

        #loop while player input is not ex
        player_input = ""
        while player_input != "ex" :
            player_input = input("Enter word : ")
            if player_input != "ex":
                response = stub.CheckWord(pangram_game_pb2.CheckWordRequest(gameId=gameId, playerWord=player_input))
                print(response.wordCheckMessage)
                print(response.gameStatusMessage)
            else:
                print("\nGoodbye, Game Ended!\n" + response.gameStatusMessage)
                break

    else:
        print("join existing game not implemented yet....")


if __name__ == '__main__':
    print("Launching connection to Game Server...")
    logging.basicConfig()
    run()
