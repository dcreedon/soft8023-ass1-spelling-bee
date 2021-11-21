import grpc

import pangram_game_pb2 as pangram_game_pb2
import pangram_game_pb2_grpc as pangram_game_pb2_grpc

game_server_address = '127.0.0.1:50057'

def run():
    channel = grpc.insecure_channel(game_server_address)

    stub = pangram_game_pb2_grpc.PangramGameStub(channel)

    # New Game or join existing
    game_choice = input("New game (n) or join existing (e) : ")
    player_name = input("Enter your name : ")

    if game_choice == "n":
        print("starting a new game")
        try:
            # Initialise new Game
            response = stub.CreateGame(pangram_game_pb2.GameRequest(playerName=player_name, gameType='PANG'))
            gameId = response.gameId
            inviteCode = response.inviteCode
            playerId = response.playerId
            print("Your unique game invite code is : " + str(inviteCode))

            print(stub.StartGame(pangram_game_pb2.StartGameRequest(gameId=gameId)).message)

        except grpc.RpcError as e:
                print("Check your server is running" + str(e))

    elif game_choice == "e":
        player_input = input("Enter your invite code: ")
        try:
            response = stub.JoinGame(pangram_game_pb2.JoinGameRequest(inviteCode=player_input, playerName=player_name))
            gameId = response.gameId
            playerId = response.playerId

            print(response.message)

        except grpc.RpcError as e:
                print("Check your server is running" + str(e))
    else:
        print("option not implemented yet....")

    # Start the Game Loop

    print("(ex) to exit game or (sco) to get game score")

    # loop while player input is not ex or sco
    player_input = ""
    while player_input != "ex":
        player_input = input("Enter word : ")
        if player_input == "sco":       # get the word score for all players
            response = stub.GameScore(pangram_game_pb2.GameScoreRequest(gameId=gameId))
            print(response.message)
        elif player_input == "ex":
            # TODO: send end game to server for the player
            response = stub.EndGame(pangram_game_pb2.EndGameRequest(gameId=gameId))
            print("\nGoodbye, Game Ended!\n" + response.message)
            break
        else:
            response = stub.CheckWord(pangram_game_pb2.CheckWordRequest(gameId=gameId, playerWord=player_input, playerId=playerId))
            print(response.wordCheckMessage)
            print(response.gameStatusMessage)


if __name__ == '__main__':
    print("Launching connection to Game Server...")
    run()
