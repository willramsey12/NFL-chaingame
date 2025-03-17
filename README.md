# NFL Player Chain

A web-based game where users name NFL players in a chain, with each player's first name starting with the first letter of the previous player's last name. Test your NFL knowledge in this fast-paced name game!

## Features

- Name NFL players in a chain where each player's first name must start with the first letter of the previous player's last name
- 2-minute timer for each turn adds excitement and challenge
- Player database includes:
  - Current NFL players
  - Hall of Fame legends
  - Historical players from throughout NFL history
- Interactive web interface with real-time feedback
- Robust player name matching to account for variations in spelling or format
- College information for each player
- Streak counter and game statistics tracking

## Project Structure

```
nfl-game/
├── backend/
│   └── game.py          # Core game logic and player matching
├── data/
│   ├── players.json     # Player database
│   ├── backups/         # Database backup directory
│   └── logs/            # Logs directory
├── frontend/
│   ├── app.py           # Flask web application
│   └── templates/       # HTML templates
├── tests/               # Test files
└── requirements.txt     # Project dependencies
```

## Installation

1. Clone the repository:
```
git clone https://github.com/willramsey12/NFL-chaingame.git
cd NFL-chaingame
```

2. Install the required dependencies:
```
pip3 install -r requirements.txt
```

## Running the Game Locally

1. Start the Flask web server:
```
cd frontend
python3 app.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5001
```

## Deployment Options

### Render.com (Recommended, One-Click Deploy)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/willramsey12/NFL-chaingame)

1. Click the "Deploy to Render" button above
2. Follow the prompts to create your Render account if you don't have one
3. Render will automatically configure your application based on the render.yaml file
4. Your application will be available at a URL like `https://nfl-player-chain.onrender.com`

### Render.com (Manual Setup)

1. Sign up at [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure deployment settings:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn frontend.app:app`

### PythonAnywhere (Beginner-friendly)

1. Sign up at [pythonanywhere.com](https://www.pythonanywhere.com/)
2. Upload your code
3. Create a new web app and select Flask
4. Configure WSGI file to point to your app

### Heroku (Developer-focused)

1. Sign up at [heroku.com](https://www.heroku.com)
2. Install the Heroku CLI
3. Create a Procfile in your project root:
```
web: gunicorn frontend.app:app
```
4. Deploy using Git:
```
heroku login
heroku create nfl-player-chain
git push heroku main
```

## Environment Variables

The application supports the following environment variables:

- `DEBUG`: Set to "True" to enable debug mode (default: "True")
- `PORT`: The port to run the application on (default: 5001)
- `PLAYER_DATA_PATH`: Custom path to the player data JSON file
- `LOGGING_LEVEL`: Set the logging level (default: "DEBUG")

## Player Name Matching

The game uses a robust player matching system that allows for various ways to match player names:

1. Exact match (case-insensitive)
2. Common nickname matching (e.g., "Mike" for "Michael")
3. First initial + last name matching
4. Fuzzy first name matching with exact last name

## Contributing

Contributions to improve the game are welcome! Here are some ways you can contribute:

1. Add missing players to the database
2. Improve the player matching algorithm
3. Enhance the user interface
4. Add new game features or modes

## License
This project is licensed under the MIT License