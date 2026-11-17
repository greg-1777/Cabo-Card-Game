import random


class Card: 
    def __init__(self, suit, value): 
        self.suit = suit 
        self.value = str(value) 
        self.points = self.__calculate_points(suit, self.value)    
        self.is_face_up = False

    def __calculate_points(self, suit, value): 
        if value == 'J' or value == '11': 
            return 11   
        elif value == 'Q' or value == '12': 
            return 12
        elif value == 'K' or value == '13': 
            return -1 if suit in ['Clubs', 'Spades'] else 13
        elif value == 'A' or value == '1': 
            return 1 
        try: 
            v = int(value) 
            return min(v, 10)
        except ValueError:
            return 10
        
    def __repr__(self): 
        return f"{self.value}{self.suit[0]}" 


class Deck: 
    def __init__(self, num_decks = 1):  
        self.num_decks = num_decks
        self.cards = [] 
        self.reset_and_shuffle()  

    def reset_and_shuffle(self): 
        suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'] 
        self.cards = []  
        for _ in range(self.num_decks): 
            for suit in suits: 
                for val in range (1, 14): 
                    self.cards.append(Card(suit, val))  
        random.shuffle(self.cards) 

    def draw(self): 
        if not self.cards: 
            return None
        return self.cards.pop() 

    
class CaboGameEngine: 
    def __init__(self, num_players = 2, num_decks = 1, silent = False): 
        self.num_players = num_players  
        self.silent = silent
        self.deck = Deck(num_decks = num_decks) 
        self.discard_pile = [] 
        self.players_hands = {}
        self.current_player_index = 0  
        self.cabo_caller = None 
        self.turns_remaining_after_cabo_called = 0 
        self.game_over = False   
        self.turn_count = 0 

    def log(self, message): 
        if not self.silent: 
            print(message)
    
    def setup_game(self):  
        self.deck.reset_and_shuffle() 
        for player_id in range(self.num_players): 
            player_hand = [self.deck.draw() for _ in range(4)]  
            player_hand[0].is_face_up = True 
            player_hand[1].is_face_up = True 
            self.players_hands[player_id] = player_hand 

        first_discard_card = self.deck.draw() 
        if first_discard_card: 
            first_discard_card.is_face_up = True
            self.discard_pile.append(first_discard_card) 

    def get_top_discard_card(self): 
        if not self.discard_pile: 
            return None
        return self.discard_pile[-1] 

    def execute_turn(self, player_id, action_type, hand_index = None):  
        self.turn_count += 1 

        if action_type == 'call_cabo' and self.cabo_caller is None: 
            self.cabo_caller = player_id  
            self.turns_remaining_after_cabo_called = self.num_players - 1 
            msg = f"Player {player_id} has called CABO!" 
            self.log(msg)
            return msg

        if action_type == 'draw_deck': 
            drawn_card = self.deck.draw()  
            if drawn_card is None: 
                return "Deck is empty"
            if hand_index is not None and 0 <= hand_index < 4: 
                old_card = self.players_hands[player_id][hand_index] 
                old_card.is_face_up = True 
                self.discard_pile.append(old_card) 

                drawn_card.is_face_up = False 
                self.players_hands[player_id][hand_index] = drawn_card 
            else: 
                drawn_card.is_face_up = False 
                self.discard_pile.append(drawn_card) 

        elif action_type == 'draw_discard':
            if not self.discard_pile: 
                return "Discard pile is empty. Cannot draw from it." 
            taken_card = self.discard_pile.pop() 
            if hand_index is not None and 0 <= hand_index < 4: 
                old_card = self.players_hands[player_id][hand_index] 
                old_card.is_face_up = True 
                self.discard_pile.append(old_card) 

                taken_card.is_face_up = False 
                self.players_hands[player_id][hand_index] = taken_card 

        if self.cabo_caller is not None and player_id != self.cabo_caller: 
            self.turns_remaining_after_cabo_called -= 1 
            if self.turns_remaining_after_cabo_called <= 0: 
                self.game_over = True  

    def calculate_scores(self): 
        scores = {}
        for player_id, hand in self.players_hands.items(): 
            for card in hand: 
                card.is_face_up = True 
            total_points = sum(card.points for card in hand)
            scores[player_id] = total_points
        return scores  
    def get_game_results(self): 
        scores = self.calculate_scores() 
        winner = min(scores, key=scores.get) 
        return { 
            "winner": winner, 
            "scores": scores, 
            "total_turns": self.turn_count, 
            "cabo_caller": self.cabo_caller
        }