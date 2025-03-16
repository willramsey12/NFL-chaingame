import unittest
import sys
import os

# Add the parent directory to the path so we can import the backend module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.game import NFLGame

class TestNFLGame(unittest.TestCase):
    def setUp(self):
        """Set up a new game instance for each test."""
        self.game = NFLGame()
        self.game.start_game()
    
    def test_start_game(self):
        """Test that a new game starts correctly."""
        # Check that a player is selected and the next letter is set
        self.assertIsNotNone(self.game.current_player)
        self.assertIsNotNone(self.game.next_required_letter)
        
        # Check that the player has 3 lives
        self.assertEqual(self.game.lives, 3)
        
        # Check that the used players list has 1 player (the starting player)
        self.assertEqual(len(self.game.used_players), 1)
    
    def test_submit_valid_answer(self):
        """Test submitting a valid player name."""
        # Get the required letter
        required_letter = self.game.next_required_letter
        
        # Find a player with a first name starting with the required letter
        valid_player = None
        for player in self.game.players:
            if player not in self.game.used_players and player['firstName'].upper().startswith(required_letter):
                valid_player = player
                break
        
        if valid_player:
            # Submit a valid answer
            result = self.game.submit_answer(f"{valid_player['firstName']} {valid_player['lastName']}")
            
            # Check that the answer was accepted
            self.assertTrue(result['valid'])
            self.assertEqual(result['message'], "Correct!")
            
            # Check that the player still has 3 lives
            self.assertEqual(self.game.lives, 3)
            
            # Check that the used players list now has 2 players
            self.assertEqual(len(self.game.used_players), 2)
        else:
            # Skip this test if no valid player can be found
            self.skipTest("No valid player found for this test")
    
    def test_submit_invalid_letter(self):
        """Test submitting a player name with the wrong first letter."""
        # Get the required letter
        required_letter = self.game.next_required_letter
        
        # Find a player with a first name NOT starting with the required letter
        wrong_player = None
        for player in self.game.players:
            if player not in self.game.used_players and not player['firstName'].upper().startswith(required_letter):
                wrong_player = player
                break
        
        if wrong_player:
            # Submit an invalid answer
            result = self.game.submit_answer(f"{wrong_player['firstName']} {wrong_player['lastName']}")
            
            # Check that the answer was rejected
            self.assertFalse(result['valid'])
            
            # Check that the player now has 2 lives
            self.assertEqual(self.game.lives, 2)
        else:
            # Skip this test if no wrong player can be found
            self.skipTest("No wrong player found for this test")
    
    def test_submit_already_used_player(self):
        """Test submitting a player name that has already been used."""
        # Use the current player (which is already in used_players)
        current_player = self.game.current_player
        
        # Submit the same player again
        result = self.game.submit_answer(f"{current_player['firstName']} {current_player['lastName']}")
        
        # Check that the answer was rejected
        self.assertFalse(result['valid'])
        self.assertIn("already been used", result['message'])
        
        # Check that the player now has 2 lives
        self.assertEqual(self.game.lives, 2)
    
    def test_game_over_after_three_wrong_answers(self):
        """Test that the game ends after three wrong answers."""
        # Make three wrong answers
        for _ in range(3):
            # Submit a non-existent player
            self.game.submit_answer("Nonexistent Player")
        
        # Check that the game is over
        self.assertTrue(self.game.game_over)
        self.assertEqual(self.game.lives, 0)


if __name__ == "__main__":
    unittest.main() 