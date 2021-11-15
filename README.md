#Pangrams
A pangram or holoalphabetic sentence is a sentence using every letter of a given alphabet at least once. 

https://en.wikipedia.org/wiki/Pangram

#Approach
- created project directory and readme file
- created github repo for project https://github.com/dcreedon/soft8023-ass1-spelling-bee
- downloaded pangrams code https://github.com/dlarkinc/Pangramsand updated words_dictionary.json file from https://github.com/dwyl/english-words
- used the darts game as a guide to structure the code, stripped out unneeded code and built pangame
- used an in memory instance of the pangram words dictionary, used static methods in the word dictionary to provide utility methods
- would be easy enough to paramaterise to use different dictionaries for different games/implementations
- also could paramaterise the scoring/bonus etc... for pangram game variations
- tried to build reusable methods into word_dictionary, pang_game
- considered upcoming multiplayer assignment when building

# command to run to create proto file for grpc
python -m grpc_tools.protoc -I../protos --python_out=. --grpc_python_out=. ../protos/pangram_game.proto

# Patterns Used
 - Singleton pattern used in the game_registry.py , dont want more than one game registry instantiated
could probably use it for the word_dictionary class also to have just one instance for the server and 
not risk multiple instances.

 - Factory pattern object_factory.py is used in the creation of the Pangram game instance PangGame(), could possibly use for dictionary 
if using more than one word dictionary. Factory pattern alows the registration of different game types that implement the 
GameManager and GameTurnTemplate and the assocaited abstract methods. the 'PANG', pang.PangGameBuilder() or other builder registered in
the object factory could be used to launch a word gae variant with different validation rules and scoring features

 - Abstract used in game_service.py for creating the Pang game and enforcing the abstract methods to be implemented.

 - Template Pattern is used in game_service.py. The pang.py class PangGameBuilder instantiates PangGame(GameManager, GameTurnTemplate). 
PangGame(GameManager, GameTurnTemplate) uses the abstract classes defined in game_service.py.


# Client Log contains a sample run of the code
# Server side console output displays the pangram used to allow you to test pangram entry and scoring