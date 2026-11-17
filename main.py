from cabo_engine import CaboGameEngine
from cabo_loader import CaboLoader
from cabo_utils import CaboUtils
from cabo_visuals import zender_board


def main(): 
    print("==================================") 
    print("         CABO SIMULATOR           ") 
    print("==================================")  

    load_choice = input("Do you want to load a saved game? (y/n): ").strip().lower() 
    if load_choice == 'y': 
        game = CaboLoader.load_game() 
        if isinstance(game, CaboGameEngine): 
            print("\n[!] Game successfully loaded from file") 
        else: 
            print(f"n[!] {game}. Starting a new game instead.") 
            num_players = int(input("Enter the number of players: ")) 
            game = CaboGameEngine(num_players = num_players) 
            game.setup_game()
    else: 
        print("\n[1] Initializing Cabo Simulator...")  
        num_players = int(input("Enter the number of players: "))  
        game = CaboGameEngine(num_players = num_players) 
        game.setup_game()  
        
        print(CaboLoader.save_game(game))
    print("[2] Displaying initial game state...") 
    print("Game Setup Complete!")


if __name__ == '__main__': 
    main()