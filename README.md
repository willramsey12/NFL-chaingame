# NFL Player Guessing Game

A web-based game where users try to identify NFL players based on clues. This game tests your knowledge of NFL players across different eras, teams, and positions.

## Features

- Guess NFL players from a database of thousands of current and historical players
- Game difficulty scales with your progress
- Player database includes:
  - Current NFL players
  - Hall of Fame legends
  - Historical players from throughout NFL history
- Interactive web interface with real-time feedback
- Robust player name matching to account for variations in spelling or format

## Project Structure

```
nfl-game/
├── backend/
│   └── game.py          # Core game logic and player matching
├── data/
│   ├── nfl_players.json            # Main player database
│   ├── complete_nfl_players.json   # Comprehensive player database
│   ├── nfl_database_tools.py       # Database management and scraping tools
│   ├── backups/                    # Database backup directory
│   └── logs/                       # Logs directory
├── frontend/
│   ├── app.py           # Flask web application
│   └── templates/       # HTML templates
├── tests/               # Test files
└── requirements.txt     # Project dependencies
```

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/nfl-game.git
cd nfl-game
```

2. Install the required dependencies:
```
pip3 install -r requirements.txt
```

## Running the Game

1. Start the Flask web server:
```
cd frontend
python3 app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

## Database Management

The game includes a comprehensive database management tool that can be used to:

- Update the player database with current players
- Add missing players manually
- Create backups of the database
- Perform a comprehensive refresh of all NFL players

To use the database management tools:

```
python data/nfl_database_tools.py [command]
```


## Player Name Matching

The game uses a robust player matching system that allows for various ways to match player names:

1. Exact match (case-insensitive)
2. Matching the first letter of the first name with the exact last name
3. Fuzzy matching based on the last name

This ensures a better gaming experience even with minor typing errors or variations in player names.

## Contributing

Contributions to improve the game are welcome! Here are some ways you can contribute:

1. Add missing players to the database
2. Improve the player matching algorithm
3. Enhance the user interface
4. Add new game features or modes

## License
This project is licensed under the MIT License