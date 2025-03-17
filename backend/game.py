import json
import random
import os
import logging

# Configure logging
logging_level = os.environ.get('LOGGING_LEVEL', 'DEBUG')
numeric_level = getattr(logging, logging_level.upper(), logging.DEBUG)
logging.basicConfig(level=numeric_level)
logger = logging.getLogger(__name__)

class NFLGame:
    def __init__(self):
        self.players = self.load_players()
        logger.info(f"Loaded {len(self.players)} NFL players")
        self.used_players = []
        self.lives = 3
        self.current_player = None
        self.next_required_letter = None
        self.game_over = False
    
    def load_players(self):
        """Load NFL player data from the JSON file."""
        script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_path = os.environ.get('PLAYER_DATA_PATH', 
                                   os.path.join(script_dir, 'data', 'players.json'))
        
        try:
            with open(data_path, 'r') as file:
                players = json.load(file)
                logger.info(f"Successfully loaded {len(players)} players from {data_path}")
                return players
        except Exception as e:
            logger.error(f"Error loading player data from {data_path}: {e}")
            # Return a minimal set of players so the game can at least run
            return [
                {"firstName": "Tom", "lastName": "Brady", "position": "QB", "team": "TB", "college": "Michigan"},
                {"firstName": "Patrick", "lastName": "Mahomes", "position": "QB", "team": "KC", "college": "Texas Tech"},
                {"firstName": "Aaron", "lastName": "Donald", "position": "DT", "team": "LAR", "college": "Pittsburgh"}
            ]
    
    def start_game(self):
        """Start a new game with a random NFL player."""
        self.used_players = []
        self.lives = 3
        self.game_over = False
        
        # Select a random player to start
        self.current_player = random.choice(self.players)
        self.used_players.append(self.current_player)
        
        # The next player's first name must start with the first letter of the current player's last name
        self.next_required_letter = self.current_player["lastName"][0].upper()
        
        return {
            "current_player": f"{self.current_player['firstName']} {self.current_player['lastName']} ({self.current_player['position']})",
            "next_required_letter": self.next_required_letter,
            "lives": self.lives,
            "used_players": len(self.used_players),
            "game_over": self.game_over,
            "team": self.current_player.get("team", ""),
            "college": self.current_player.get("college", "Unknown")
        }
    
    def _is_player_used(self, player):
        """Check if a player has already been used in this game.
        Players with the same name but different teams/positions are considered different players."""
        for used_player in self.used_players:
            # If first and last name match, check if team/position also match
            if (used_player['firstName'].lower() == player['firstName'].lower() and
                used_player['lastName'].lower() == player['lastName'].lower()):
                
                # Get team and position for additional comparison
                used_team = used_player.get('team', '').lower()
                player_team = player.get('team', '').lower()
                used_position = used_player.get('position', '').lower()
                player_position = player.get('position', '').lower()
                used_college = used_player.get('college', '').lower()
                player_college = player.get('college', '').lower()
                
                # If we have detailed info and it matches exactly, it's the same player
                if (used_team and player_team and used_team == player_team and
                    used_position and player_position and used_position == player_position):
                    # If college info is available and it matches, definitely the same player
                    if (used_college and player_college and used_college == player_college):
                        return True
                    
                    # If team and position match (and we have both), likely the same player
                    return True
                
                # If neither team nor position is available, fall back to just name comparison
                if (not used_team and not player_team and 
                    not used_position and not player_position):
                    return True
                
                # Different team or position means different player with same name
                # Continue checking other used players
                continue
            
        # If we get here, no match was found
        return False

    def submit_answer(self, answer):
        """Submit a player name as an answer."""
        logger.debug(f"submit_answer called with: {answer}")
        
        if self.game_over:
            logger.debug("Game is already over")
            return {"error": "Game is over. Start a new game."}
        
        # Parse the input to get first and last name
        parts = answer.strip().split()
        logger.debug(f"Split answer into parts: {parts}")
        
        if len(parts) < 2:
            logger.debug("Not enough name parts provided")
            return {
                "valid": False,
                "message": "Please enter both first and last name.",
                "lives": self.lives,
                "game_over": self.game_over,
                "error_type": "format"
            }
        
        first_name = parts[0]
        logger.debug(f"First name: {first_name}, Required letter: {self.next_required_letter}")
        
        # Check if the first name starts with the required letter
        if not first_name.upper().startswith(self.next_required_letter):
            logger.debug(f"First name does not start with required letter: {self.next_required_letter}")
            return {
                "valid": False,
                "message": f"First name must start with '{self.next_required_letter}'.",
                "lives": self.lives,
                "game_over": self.game_over,
                "error_type": "wrong_letter"
            }
        
        # Find the player in our database - improved matching algorithm
        found_player = self._find_player_in_database(parts)
        
        if not found_player:
            logger.debug(f"Player not found in database: {answer}")
            return {
                "valid": False,
                "message": "Player not found. Either the name is misspelled or the player doesn't exist in our database.",
                "lives": self.lives,
                "game_over": self.game_over,
                "error_type": "not_found"
            }
        
        # Check if player has already been used
        if self._is_player_used(found_player):
            logger.debug(f"Player has already been used: {found_player['firstName']} {found_player['lastName']}")
            
            return {
                "valid": False,
                "message": "This player has already been used.",
                "lives": self.lives,
                "game_over": self.game_over,
                "error_type": "already_used"
            }
        
        # Valid answer
        self.current_player = found_player
        self.used_players.append(found_player)
        self.next_required_letter = found_player["lastName"][0].upper()
        
        return {
            "valid": True,
            "message": "Correct!",
            "current_player": f"{found_player['firstName']} {found_player['lastName']} ({found_player['position']})",
            "next_required_letter": self.next_required_letter,
            "lives": self.lives,
            "used_players": len(self.used_players),
            "game_over": self.game_over,
            "team": found_player.get("team", ""),
            "college": found_player.get("college", "Unknown")
        }
    
    def _find_player_in_database(self, name_parts):
        """
        Enhanced player lookup with smarter matching strategies.
        Returns the player dict if found, None otherwise.
        
        Supports formats:
        - "First Last"
        - "First Last Team" (for players with same names)
        """
        # Check if a team identifier was provided (usually as a third part)
        team_identifier = None
        if len(name_parts) > 2:
            team_identifier = name_parts[2].upper()  # Team identifiers are typically uppercase
        
        # Try exact match first (case insensitive)
        name_to_match = ' '.join(name_parts[:2]).lower()
        
        # Debug the search
        logger.debug(f"Searching for player: {name_to_match} with team identifier: {team_identifier}")
        
        # Strategy 1: Exact match with team if provided
        if team_identifier:
            matches = []
            for player in self.players:
                player_name = f"{player['firstName']} {player['lastName']}".lower()
                if (name_to_match == player_name and 
                    player.get('team', '').upper() == team_identifier):
                    logger.debug(f"Found exact match with team: {player['firstName']} {player['lastName']} ({player['team']})")
                    matches.append(player)
            
            if matches:
                return matches[0]  # Return the first match
        
        # Strategy 2: Exact match (case insensitive) without team consideration
        matches = []
        for player in self.players:
            player_name = f"{player['firstName']} {player['lastName']}".lower()
            if name_to_match == player_name:
                logger.debug(f"Found exact match: {player['firstName']} {player['lastName']}")
                matches.append(player)
        
        # If exactly one match was found, return it
        if len(matches) == 1:
            return matches[0]
        # If multiple matches found and no team specified, return the first one
        elif len(matches) > 1 and not team_identifier:
            logger.debug(f"Found multiple matches, returning first: {matches[0]['firstName']} {matches[0]['lastName']}")
            return matches[0]
        # If multiple matches found but none match the team, return the first
        elif len(matches) > 1:
            logger.debug(f"Found multiple matches but none for team {team_identifier}, returning first")
            return matches[0]
        
        # Strategy 3: Common nickname match
        nicknames = {
            'mike': 'michael',
            'chris': 'christopher',
            'rob': 'robert',
            'bob': 'robert',
            'bobby': 'robert',
            'will': 'william',
            'bill': 'william',
            'billy': 'william',
            'jim': 'james',
            'jimmy': 'james',
            'joe': 'joseph',
            'joey': 'joseph',
            'dan': 'daniel',
            'danny': 'daniel',
            'tony': 'anthony',
            'nick': 'nicholas',
            'ben': 'benjamin',
            'matt': 'matthew',
            'gabe': 'gabriel',
            'sam': 'samuel',
            'alex': 'alexander',
            'josh': 'joshua',
            'zach': 'zachary',
            'jake': 'jacob',
            'andy': 'andrew',
            'drew': 'andrew',
            'tom': 'thomas',
            'tommy': 'thomas',
            'steve': 'steven',
            'stevie': 'steven',
            'ed': 'edward',
            'eddie': 'edward',
            'ted': 'theodore',
            'rick': 'richard',
            'dick': 'richard',
            'rich': 'richard'
        }
        
        first_name = name_parts[0].lower()
        if first_name in nicknames:
            formal_name = nicknames[first_name]
            matches = []
            
            for player in self.players:
                # Check if nickname matches with team filter if provided
                if player['firstName'].lower() == formal_name and player['lastName'].lower() == name_parts[1].lower():
                    if team_identifier and player.get('team', '').upper() == team_identifier:
                        logger.debug(f"Found nickname match with team: {player['firstName']} {player['lastName']} ({player['team']})")
                        return player
                    matches.append(player)
            
            # If matches found, return first one
            if matches:
                logger.debug(f"Found nickname match: {matches[0]['firstName']} {matches[0]['lastName']}")
                return matches[0]
        
        # Strategy 4: First initial + exact last name match (only if first name is one character)
        if len(name_parts[0]) == 1:
            first_initial = name_parts[0].lower()
            last_name = name_parts[1].lower()
            
            matches = []
            for player in self.players:
                if (player['firstName'][0].lower() == first_initial and
                    player['lastName'].lower() == last_name):
                    # Filter by team if provided
                    if team_identifier and player.get('team', '').upper() == team_identifier:
                        logger.debug(f"Found initial+lastname match with team: {player['firstName']} {player['lastName']} ({player['team']})")
                        return player
                    matches.append(player)
            
            if len(matches) == 1:  # Only return if there's exactly one match
                logger.debug(f"Found initial+lastname match: {matches[0]['firstName']} {matches[0]['lastName']}")
                return matches[0]
            elif len(matches) > 1 and team_identifier is None:
                # If multiple matches and no team specified, return first
                logger.debug(f"Found multiple initial+lastname matches, returning first: {matches[0]['firstName']} {matches[0]['lastName']}")
                return matches[0]
        
        # Strategy 5: Exact last name match with similar first name start
        # Only if first name is at least 3 characters
        if len(name_parts[0]) >= 3:
            first_name_start = name_parts[0].lower()
            last_name = name_parts[1].lower()
            
            matches = []
            for player in self.players:
                if (player['lastName'].lower() == last_name and
                    (player['firstName'].lower().startswith(first_name_start) or
                     first_name_start.startswith(player['firstName'].lower()))):
                    # Filter by team if provided
                    if team_identifier and player.get('team', '').upper() == team_identifier:
                        logger.debug(f"Found partial first name match with team: {player['firstName']} {player['lastName']} ({player['team']})")
                        return player
                    matches.append(player)
            
            if len(matches) == 1:  # Only return if there's exactly one match
                logger.debug(f"Found partial first name match: {matches[0]['firstName']} {matches[0]['lastName']}")
                return matches[0]
            elif len(matches) > 1 and team_identifier is None:
                # If multiple matches and no team specified, return first
                logger.debug(f"Found multiple partial first name matches, returning first: {matches[0]['firstName']} {matches[0]['lastName']}")
                return matches[0]
        
        # If we get here, no match was found
        return None
    
    def _find_players_with_same_name(self, player):
        """Find all players with the same first and last name."""
        return [
            p for p in self.players 
            if p['firstName'].lower() == player['firstName'].lower() 
            and p['lastName'].lower() == player['lastName'].lower()
        ]
    
    def lose_life(self):
        """Reduce player's life by one and check if game is over."""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True
    
    def get_game_state(self):
        """Return the current game state."""
        return {
            "current_player": f"{self.current_player['firstName']} {self.current_player['lastName']} ({self.current_player['position']})",
            "next_required_letter": self.next_required_letter,
            "lives": self.lives,
            "used_players": len(self.used_players),
            "game_over": self.game_over,
            "team": self.current_player.get("team", ""),
            "college": self.current_player.get("college", "Unknown")
        }
    
    def to_dict(self):
        """Convert game state to a dictionary for session storage."""
        return {
            "players": self.players,
            "used_players": [self._player_to_dict(p) for p in self.used_players],
            "lives": self.lives,
            "current_player": self._player_to_dict(self.current_player) if self.current_player else None,
            "next_required_letter": self.next_required_letter,
            "game_over": self.game_over
        }
    
    def _player_to_dict(self, player):
        """Convert a player dict to a safe format for serialization."""
        if player is None:
            return None
        return {
            "firstName": player["firstName"],
            "lastName": player["lastName"],
            "position": player["position"],
            "team": player["team"],
            "college": player.get("college", "Unknown")
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a game instance from a dictionary."""
        game = cls()
        game.players = data.get("players", [])
        game.lives = data.get("lives", 3)
        game.current_player = data.get("current_player")
        game.next_required_letter = data.get("next_required_letter")
        game.game_over = data.get("game_over", False)
        
        # Rebuild the used_players list
        game.used_players = []
        for player_dict in data.get("used_players", []):
            game.used_players.append(player_dict)
        
        return game

    def timer_expired(self):
        """Called when the 2-minute timer expires without a valid answer."""
        self.lose_life()
        return {
            "valid": False,
            "message": "Time's up! You have 2 minutes to name a player.",
            "lives": self.lives,
            "game_over": self.game_over,
            "error_type": "timeout"
        } 