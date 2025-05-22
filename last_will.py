import random # Import random for shuffling the deck

class Player:
    def __init__(self, name: str, money: int = 50, actions: int = 2): # Default money to 50, actions to 2
        self.name = name
        self.money = money
        self.actions = actions
        self.cards: list = [] 
        self.hand: list[Card] = [] 
        self.properties: list = []
        self.is_bankrupt: bool = False

    def display_status(self):
        """Prints a formatted summary of the player's current state."""
        print("\n" + "-" * 30)
        print(f"Player: {self.name}")
        print(f"Money: ${self.money}")
        print(f"Actions: {self.actions}")
        print(f"Bankrupt: {'Yes' if self.is_bankrupt else 'No'}")
        
        print("Properties:")
        if not self.properties:
            print("  None")
        else:
            for prop in self.properties:
                print(f"  - {prop.name} (Upkeep: ${prop.upkeep_cost})")
        
        print("Hand:")
        if not self.hand:
            print("  (empty)")
        else:
            for i, card in enumerate(self.hand):
                print(f"  {i}: {card}") # Uses Card.__str__
        print("-" * 30)

    def draw_card(self, deck: list['Card']):
        if deck:
            card = deck.pop()
            self.hand.append(card)
            print(f"{self.name} drew '{card.name}'.") # Refined output
        else:
            print("Deck is empty. Cannot draw a card.")

    def play_card(self, card_index: int, game_board: 'GameBoard'):
        if 0 <= card_index < len(self.hand):
            card_to_play = self.hand[card_index] # Get card before potentially popping
            if self.money >= card_to_play.cost:
                self.money -= card_to_play.cost
                played_card = self.hand.pop(card_index)
                print(f"{self.name} played '{played_card.name}' for {played_card.cost} money. Money left: ${self.money}") # Refined output
                
                if played_card.type == "property":
                    self.properties.append(played_card)
                    print(f"{self.name} acquired '{played_card.name}'.") # Refined output

                # print(f"Card {played_card.name} effect happens here. {played_card.effect}") # Placeholder
                
                if self.money < 0 and not self.is_bankrupt:
                    self.is_bankrupt = True
                    print(f"Playing '{played_card.name}' made {self.name} go bankrupt!")
                return True
            else:
                print(f"Not enough money to play {card.name}. Cost: {card.cost}, Money: {self.money}")
                return False
        else:
            print("Invalid card index.")
            return False

    def perform_upkeep(self):
        """Handles upkeep costs for properties owned by the player."""
        print(f"\n--- {self.name}'s Upkeep Phase ---")
        if not self.properties:
            print("  No properties to maintain.")
        total_upkeep_paid = 0
        for prop in self.properties:
            if prop.upkeep_cost > 0:
                self.money -= prop.upkeep_cost
                total_upkeep_paid += prop.upkeep_cost
                print(f"  Paid ${prop.upkeep_cost} upkeep for '{prop.name}'. Money left: ${self.money}")
        if total_upkeep_paid > 0:
             print(f"  Total upkeep paid: ${total_upkeep_paid}")
        print(f"  Money after upkeep: ${self.money}")
        if self.money < 0 and not self.is_bankrupt: # Check if already bankrupt to avoid repeated messages
            self.is_bankrupt = True
            print(f"  {self.name} has gone bankrupt due to upkeep costs!")
        print("-" * 20) # Separator for end of upkeep phase

    def buy_property(self, property_card):
        pass

    def use_action(self):
        pass


class Card:
    def __init__(self, name: str, type: str, cost: int = 0, upkeep_cost: int = 0, effect: str = ""):
        self.name = name
        self.type = type  # e.g., "property", "event", "helper"
        self.cost = cost
        self.upkeep_cost = upkeep_cost
        self.effect = effect

    def __str__(self):
        details = f"'{self.name}' (Type: {self.type}, Cost: ${self.cost}"
        if self.type == "property" and self.upkeep_cost > 0: # Show upkeep only for properties with upkeep > 0
            details += f", Upkeep: ${self.upkeep_cost}"
        elif self.type == "property": # Properties with 0 upkeep
             details += f", Upkeep: $0"
        details += ")"
        return details

    # Placeholder for methods related to card effects or usage
    def apply_effect(self, player, game_board):
        pass


class GameBoard:
    def __init__(self):
        self.deck: list[Card] = [
            Card("Helper Friend", "helper", 5, 0, "Placeholder effect: Gain 1 action next turn"),
            Card("Cheap Property", "property", 10, 1, "Placeholder effect: Lose 1 money per turn"),
            Card("Expensive Meal", "event", 3, 0, "Placeholder effect: Spend money quickly"),
            Card("Surprise Windfall", "event", 0, 0, "Placeholder effect: Gain 20 money"),
            Card("Decrepit Factory", "property", 5, 2, "A constant drain on finances."),
            Card("Grand Mansion", "property", 20, 5, "Costs a fortune in upkeep."),
            Card("Risky Investment", "property", 15, 0, "Placeholder effect: 50% chance to double money, 50% chance to lose it all"), # upkeep 0 for now
            Card("Generous Grant", "helper", 0, 0, "Placeholder effect: All players gain 5 money"),
            Card("Tax Audit", "event", 15, 0, "Placeholder effect: Pay 15 money or lose a property")
        ]
        random.shuffle(self.deck)
        self.property_deck: list[Card] = [] 
        self.event_deck: list[Card] = [] 
        self.helper_deck: list[Card] = [] 
        self.available_properties: list[Card] = []
        # self.current_turn: int = 0 # Replaced by current_round
        self.current_phase: str = ""  # e.g., "draw", "action", "discard"
        
        self.players: list[Player] = []
        self.current_player: Player | None = None
        self.num_rounds: int = 7 # Default number of rounds
        self.current_round: int = 0


    # Placeholder for methods related to game progression
    def setup_game(self, num_players: int = 1): # Default to 1 player for now
        pass

    def start_game(self):
        """Initializes the game state."""
        # Create a single player for now
        player1 = Player(name="Player 1")
        self.players.append(player1)
        self.current_player = self.players[0] 

        print("\n" + "=" * 40)
        print(f"Game started with {self.current_player.name}.")
        print(f"Total rounds: {self.num_rounds}")
        print("=" * 40 + "\n")
        
        # Player draws initial hand
        for _ in range(3): 
            if self.deck: 
                 self.current_player.draw_card(self.deck)
            else:
                print("Deck ran out during initial draw.")
                break
        # Initial status display after drawing hand
        if self.current_player:
            self.current_player.display_status()


    def play_single_round(self):
        """Simulates a single round of the game for all players."""
        print(f"\n\n{'=' * 15} Playing Round {self.current_round} of {self.num_rounds} {'=' * 15}")
        for player_obj in self.players:
            self.current_player = player_obj 
            print("\n" + "*" * 40)
            print(f"Starting turn for {player_obj.name}.")
            print("*" * 40)


            if player_obj.is_bankrupt:
                print(f"{player_obj.name} is bankrupt and skips their turn.")
                continue 

            player_obj.actions = 2 # Replenish actions
            print(f"{player_obj.name} gets {player_obj.actions} actions.")
            
            self.take_turn() 

            if player_obj.is_bankrupt: 
                print(f"{player_obj.name} ended their turn bankrupt.")
            
            print(f"--- End of turn for {player_obj.name} ---")

    def display_help(self):
        """Prints a list of available commands and their syntax."""
        print("\n" + "=" * 10 + " Help " + "=" * 10)
        print("Available commands:")
        print("  play <card_index> - Plays the card at the specified index from your hand.")
        print("                      Example: 'play 0'")
        print("  draw              - Draws a card from the deck.")
        print("  pass              - Ends your current turn.")
        print("  help              - Displays this help message.")
        print("\nGame Objective: Be the player with the least amount of money at the end of the game!")
        print("=" * 26)

    def prompt_for_action(self) -> bool | str:
        """
        Prompts the current player for an action, parses it, and executes it.
        Returns True if an action was successfully performed and consumed an action point.
        Returns 'pass' if the player chose to pass.
        Returns False if the command was 'help', invalid, or a playable action failed (e.g. not enough money).
        """
        if not self.current_player:
            print("Error: No current player for prompt_for_action.")
            return False

        action_input = input(f"Enter action for {self.current_player.name} ('help' for commands): ").strip().lower()

        if action_input == "help":
            self.display_help()
            return False # Help displayed, no action point consumed
        elif action_input == "draw":
            if self.deck:
                self.current_player.draw_card(self.deck)
                return True # Draw action performed
            else:
                print("Deck is empty. Cannot draw.")
                return True # Still counts as an action attempt as per previous logic
        elif action_input.startswith("play "):
            try:
                card_idx_str = action_input.split(" ", 1)[1] # Ensure only one split
                card_idx = int(card_idx_str)
                # Check if card_idx is valid for the current hand size.
                # play_card itself also checks, but good to have a check here too.
                if not (0 <= card_idx < len(self.current_player.hand)):
                    print(f"Invalid card index: {card_idx}. Hand size is {len(self.current_player.hand)}.")
                    print("Use 'play <index_number_from_your_hand>'. Example: 'play 0'")
                    return False

                played_successfully = self.current_player.play_card(card_idx, self)
                return played_successfully # True if successful, False otherwise
            except IndexError: # Catches if split(" ")[1] fails (no argument after "play")
                print("Invalid play command. Use 'play <card_index>'. Example: 'play 0'")
                return False
            except ValueError: # Catches if int(card_idx_str) fails
                print("Invalid card index. Must be a number after 'play '. Example: 'play 0'")
                return False
        elif action_input == "pass":
            print(f"{self.current_player.name} chooses to pass.")
            return "pass" # Special return value for pass
        else:
            print("Invalid command. Type 'help' for a list of commands.")
            return False # Invalid command, no action point consumed

    def take_turn(self):
        """Simulates a single player's turn including upkeep and actions."""
        if not self.current_player:
            print("Error: No current player set for take_turn().")
            return

        print("\n--- Status before Upkeep ---")
        self.current_player.display_status()

        self.current_player.perform_upkeep()

        print("\n--- Status after Upkeep ---")
        self.current_player.display_status()

        if self.current_player.is_bankrupt:
            print(f"{self.current_player.name} is bankrupt after upkeep and cannot take actions.")
            return

        print(f"\n--- {self.current_player.name}'s Action Phase ---")
        while self.current_player.actions > 0 and not self.current_player.is_bankrupt:
            # Display status before each prompt inside the loop, as hand/money might change
            print("\n--- Current Status before action ---")
            self.current_player.display_status() 
            
            action_result = self.prompt_for_action()

            if action_result is True:
                self.current_player.actions -= 1
                print(f"Action performed. Actions remaining: {self.current_player.actions}")
            elif action_result == "pass":
                self.current_player.actions = 0 # End turn
            # If action_result is False (help, invalid, or failed play), loop continues, actions not decremented

            if self.current_player.is_bankrupt:
                print(f"{self.current_player.name} became bankrupt during their action phase.")
                break # Exit action loop if player becomes bankrupt
            
            if self.current_player.actions <= 0:
                print(f"{self.current_player.name}'s actions are depleted.")
                break # Exit loop if actions run out

        print(f"\n--- End of Action Phase for {self.current_player.name} ---")
        self.current_player.display_status() # Final status for the turn


    def determine_winner(self):
        """Determines and prints the winner based on the lowest money."""
        print("\n\n" + "=" * 40)
        print("--- Game Over ---")
        print("=" * 40)

        if not self.players:
            print("No players in the game to determine a winner.")
            return

        # Filter out bankrupt players if they are not eligible to win,
        # or include them if the goal is simply lowest score among all.
        # For now, considering all players, bankrupt or not.
        
        winner = self.players[0] # Assume first player is winner initially
        # Consider only non-bankrupt players if that's a rule, otherwise lowest score wins.
        # Current logic: lowest score wins, even if bankrupt.
        for player in self.players[1:]: 
            if player.money < winner.money:
                winner = player
        
        print(f"\nThe winner is {winner.name} with ${winner.money} money!")
        
        print("\n--- Final Scores ---")
        for player in self.players:
            status = "Bankrupt" if player.is_bankrupt else "Playing"
            print(f"  {player.name}: ${player.money} ({status})")
        print("=" * 40)


    def next_turn(self): # This method seems unused, keeping for now.
        pass

    def change_phase(self, new_phase: str): # This method seems unused, keeping for now.
        pass


if __name__ == "__main__":
    game = GameBoard()
    game.start_game() # Sets up players, initial draw, and initial status
    
    # Main game loop
    while game.current_round < game.num_rounds:
        game.current_round += 1
        active_players = [p for p in game.players if not p.is_bankrupt]
        if not active_players:
            print("\nNo active players left. Ending game early.")
            break
        
        game.play_single_round() 

    game.determine_winner()
