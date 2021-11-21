import threading
import uuid


class GameRegistry:
    """ Simple in-memory implementation for now; thread-safe

    """
    __instance = None

    def __init__(self):
        if GameRegistry.__instance is not None:
            raise Exception("This is a singleton!")
        else:
            GameRegistry.__instance = self
        self.lock = threading.Lock()
        self.games = {}
        self.invite_codes = {}      #list of invite codes per game
        self.instance = None

    @staticmethod
    def get_instance():
        if GameRegistry.__instance is None:
            with threading.Lock():
                if GameRegistry.__instance is None:  # Double locking mechanism
                    GameRegistry()
        return GameRegistry.__instance

    def add_game(self, game):
        self.lock.acquire()
        game_id = uuid.uuid4()  # generate what will almost certainly be a unique id (may need to investigate SafeUUID)
        self.games[game_id] = game
        self.lock.release()
        return game_id

    def add_invite_code(self, invite_code, game_id):
        self.invite_codes[invite_code] = game_id  # generate four digit code to send to other players to join game

    def get_game(self, game_id):
        return self.games[uuid.UUID(bytes=game_id)]

    def get_game_from_invite_code(self, game_id):
        return self.games[game_id]

    def get_invite_code(self, game_id):
        return self.invite_codes[game_id]

    def get_game_id_with_invite_code(self, inviteCode):
        return self.invite_codes[inviteCode]
