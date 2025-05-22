import unittest
import io
from contextlib import redirect_stdout
from last_will import Player, Card, GameBoard

class TestPlayer(unittest.TestCase):

    def test_player_creation(self):
        player = Player(name="Test Player")
        self.assertEqual(player.name, "Test Player")
        self.assertEqual(player.money, 50) # Default money
        self.assertEqual(player.actions, 2) # Default actions
        self.assertEqual(player.hand, [])
        self.assertEqual(player.properties, [])
        self.assertFalse(player.is_bankrupt)

    def test_draw_card(self):
        player = Player(name="Draw Test Player")
        deck = [
            Card("Card 1", "event", 0, 0, "Effect 1"),
            Card("Card 2", "helper", 0, 0, "Effect 2")
        ]
        
        # Draw one card
        card_to_draw = deck[-1] # Card that will be popped
        player.draw_card(deck)
        self.assertEqual(len(player.hand), 1)
        self.assertEqual(len(deck), 1)
        self.assertIn(card_to_draw, player.hand)
        self.assertEqual(player.hand[0].name, "Card 2") # Check specific card

        # Draw another card
        card_to_draw_2 = deck[-1]
        player.draw_card(deck)
        self.assertEqual(len(player.hand), 2)
        self.assertEqual(len(deck), 0)
        self.assertIn(card_to_draw_2, player.hand)

        # Test drawing from an empty deck
        player.draw_card(deck) # Deck is now empty
        self.assertEqual(len(player.hand), 2) # Hand size should not change
        self.assertEqual(len(deck), 0) # Deck remains empty

    def test_play_card_sufficient_funds(self):
        player = Player(name="Play Sufficient", money=50)
        card_cost = 10
        card_to_play = Card("Test Event Card", "event", card_cost, 0, "Event Effect")
        player.hand.append(card_to_play)
        
        # For this test, play_card might not need a full GameBoard if it only affects player state
        # and the card doesn't have complex effects interacting with GameBoard.
        # If play_card expects a GameBoard instance for other reasons (e.g. accessing game.deck),
        # a mock or minimal GameBoard might be needed. For now, trying with None.
        mock_game_board = None # Or GameBoard() if None causes issues
        
        result = player.play_card(0, mock_game_board)
        
        self.assertTrue(result)
        self.assertEqual(player.money, 50 - card_cost)
        self.assertEqual(len(player.hand), 0)
        self.assertNotIn(card_to_play, player.hand)

    def test_play_card_insufficient_funds(self):
        player = Player(name="Play Insufficient", money=5)
        card_cost = 10
        card_to_play = Card("Expensive Event", "event", card_cost, 0, "Expensive Effect")
        player.hand.append(card_to_play)
        
        mock_game_board = None 
        result = player.play_card(0, mock_game_board)
        
        self.assertFalse(result)
        self.assertEqual(player.money, 5) # Money should not change
        self.assertEqual(len(player.hand), 1) # Card should remain in hand
        self.assertIn(card_to_play, player.hand)

    def test_play_property_card(self):
        player = Player(name="Property Player", money=30)
        property_card = Card("Test Property", "property", 10, 2, "Property Effect")
        player.hand.append(property_card)
        
        mock_game_board = None
        result = player.play_card(0, mock_game_board)
        
        self.assertTrue(result)
        self.assertEqual(player.money, 30 - 10)
        self.assertEqual(len(player.hand), 0)
        self.assertIn(property_card, player.properties)
        self.assertEqual(len(player.properties), 1)

    def test_perform_upkeep(self):
        player = Player(name="Upkeep Player", money=30)
        prop1 = Card("Factory", "property", 0, 2, "Factory upkeep")
        prop2 = Card("Mansion", "property", 0, 3, "Mansion upkeep")
        
        player.properties.append(prop1)
        player.properties.append(prop2)
        
        player.perform_upkeep()
        
        self.assertEqual(player.money, 30 - (2 + 3))

    def test_bankruptcy_from_upkeep(self):
        player = Player(name="Bankrupt Upkeep", money=3)
        expensive_prop = Card("Expensive Place", "property", 0, 5, "High upkeep")
        player.properties.append(expensive_prop)
        
        player.perform_upkeep()
        
        self.assertEqual(player.money, 3 - 5)
        self.assertTrue(player.is_bankrupt)

    def test_play_card_makes_bankrupt(self):
        player = Player(name="Bankrupt Play", money=10)
        costly_card = Card("Very Costly Card", "event", 15, 0, "Costs a lot")
        player.hand.append(costly_card)

        mock_game_board = None
        result = player.play_card(0, mock_game_board)

        self.assertTrue(result) # Play should be successful
        self.assertEqual(player.money, 10 - 15)
        self.assertTrue(player.is_bankrupt)
        self.assertEqual(len(player.hand), 0)


if __name__ == '__main__':
    unittest.main()


class TestGameBoard(unittest.TestCase):

    def setUp(self):
        """Set up a game instance and a player for tests."""
        self.game = GameBoard()
        # start_game() by default creates one player, "Player 1"
        # and current_player is set to this player.
        # Player also draws 3 cards.
        self.game.start_game() 
        self.player = self.game.players[0]

    def test_game_board_creation(self):
        """Test the initial state of a GameBoard instance."""
        game = GameBoard() # Test a fresh instance, not from setUp
        self.assertIsInstance(game.deck, list)
        if game.deck: # Deck is shuffled, so we just check type of first card
            self.assertIsInstance(game.deck[0], Card)
        self.assertEqual(game.num_rounds, 7) # Default num_rounds
        self.assertEqual(game.current_round, 0)
        self.assertEqual(game.players, []) # Players list should be empty before start_game

    def test_start_game(self):
        """Test the state after start_game is called."""
        self.assertNotEqual(len(self.game.players), 0)
        self.assertIsInstance(self.game.players[0], Player)
        self.assertEqual(self.game.current_player, self.game.players[0])
        self.assertEqual(self.game.current_player.name, "Player 1") # Default name
        self.assertEqual(len(self.player.hand), 3) # Player should have drawn 3 cards

    def test_play_single_round_and_take_turn_basic_flow(self):
        """Test a simplified flow focusing on player drawing a card during a turn."""
        self.player.money = 50 
        self.game.current_round = 1
        self.game.current_player = self.player
        self.player.actions = 1 # Set actions for one draw

        initial_hand_size = len(self.player.hand)
        initial_deck_size = len(self.game.deck)

        # Simulate the 'draw' action part of a turn
        # We are directly calling draw_card, assuming prompt_for_action would lead to this.
        if initial_deck_size > 0:
            self.player.draw_card(self.game.deck)
            self.assertEqual(len(self.player.hand), initial_hand_size + 1)
            self.assertEqual(len(self.game.deck), initial_deck_size - 1)
        else:
            # If deck is empty, hand and deck size should not change
            self.player.draw_card(self.game.deck) # Attempt to draw
            self.assertEqual(len(self.player.hand), initial_hand_size)
            self.assertEqual(len(self.game.deck), 0)
        
        # This test doesn't directly test take_turn's input loop, but a core action within it.

    def test_determine_winner_single_player(self):
        """Test determine_winner with a single player."""
        self.player.money = 100
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            self.game.determine_winner()
        output = captured_output.getvalue()
        
        self.assertIn(self.player.name, output)
        self.assertIn(str(self.player.money), output)
        self.assertIn(f"The winner is {self.player.name} with ${self.player.money} money!", output)

    def test_determine_winner_multiple_players(self):
        """Test determine_winner with multiple players."""
        game = GameBoard() # Use a fresh game instance for this test
        player1 = Player(name="Winner Player", money=10)
        player2 = Player(name="Loser Player", money=20)
        
        game.players.extend([player1, player2])
        # game.num_rounds = 1 # Not strictly necessary for this test
        
        captured_output = io.StringIO()
        with redirect_stdout(captured_output):
            game.determine_winner()
        output = captured_output.getvalue()
        
        self.assertIn(f"The winner is {player1.name} with ${player1.money} money!", output)
        self.assertNotIn(f"The winner is {player2.name}", output)
        self.assertIn(f"{player1.name}: ${player1.money}", output)
        self.assertIn(f"{player2.name}: ${player2.money}", output)
