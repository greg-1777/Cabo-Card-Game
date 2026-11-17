import json

from cabo_engine import CaboGameEngine, Card


class CaboLoader: 
    @staticmethod
    def save_game(engine, filename = "cabo_save.json"): 
        game_data = { 
            "num_players": engine.num_players, 
            "current_player_index": engine.current_player_index, 
            "cabo_caller": engine.cabo_caller, 
            "turns_remaining_after_cabo_called": engine.turns_remaining_after_cabo_called, 
            "game_over": engine.game_over, 
            "discard_pile": [{"suit" : c.suit, "value" : c.value, "is_face_up" : c.is_face_up} for c in engine.discard_pile], 
            "deck": [{"suit": c.suit, "value": c.value, "is_face_up": c.is_face_up} for c in engine.deck.cards], 
            "players_hands": {
                str(p_id): [{"suit": c.suit, "value": c.value, "is_face_up": c.is_face_up} for c in hand] 
                for p_id, hand in engine.players_hands.items()
            }
        }

        try: 
            with open(filename, 'w') as f:  
                json.dump(game_data, f, indent=4) 
            return f"Game successfully saved to {filename}" 
        except (OSError, TypeError, ValueError) as e: 
            return f"Failed to save game: {e}"  

    @staticmethod
    def load_game(filename = 'cabo_save.json'): 
        try: 
            with open(filename, 'r') as f: 
                game_data = json.load(f) 
            engine = CaboGameEngine(num_players=game_data["num_players"]) 
            engine.current_player_index = game_data["current_player_index"] 
            engine.cabo_caller = game_data["cabo_caller"]
            engine.turns_remaining_after_cabo_called = game_data["turns_remaining_after_cabo_called"] 
            engine.game_over = game_data["game_over"] 

            engine.discard_pile = [] 
            for c_data in game_data["discard_pile"]: 
                card = Card(c_data["suit"], c_data["value"]) 
                card.is_face_up = c_data["is_face_up"] 
                engine.discard_pile.append(card) 

            engine.deck.cards = [] 
            for c_data in game_data["deck"]: 
                card = Card(c_data["suit"], c_data["value"]) 
                card.is_face_up = c_data["is_face_up"] 
                engine.deck.cards.append(card) 

            engine.players_hands = {} 
            for p_id_str, hand_data in game_data["players_hands"].items(): 
                p_id = int(p_id_str) 
                hand = [] 
                for c_data in hand_data: 
                    card = Card(c_data["suit"], c_data["value"])  
                    card.is_face_up = c_data["is_face_up"]  
                    hand.append(card) 
                engine.players_hands[p_id] = hand

            return engine  
        except FileNotFoundError: 
            return f"No saved file found at {filename}" 
        except (OSError, ValueError, KeyError, TypeError, AttributeError) as e: 
            return f"Failed to load game: {e}"