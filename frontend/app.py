import sys
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file if present (local development only)
if os.path.exists('.env'):
    load_dotenv()

# Configure logging
logging_level = os.environ.get('LOGGING_LEVEL', 'DEBUG')
numeric_level = getattr(logging, logging_level.upper(), logging.DEBUG)
logging.basicConfig(level=numeric_level)
logger = logging.getLogger(__name__)

# Add the parent directory to the path so we can import the backend module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, jsonify, session
from backend.game import NFLGame

app = Flask(__name__)
# Use environment variable for secret key in production
app.secret_key = os.environ.get('SECRET_KEY', 'nfl_game_secret_key')  # For session management

# Create a global game instance that persists between requests
# This avoids having to serialize/deserialize the entire players database
GAME_INSTANCES = {}

# Health check endpoint for Render
@app.route('/health')
def health_check():
    """Simple health check endpoint for monitoring."""
    return jsonify({"status": "healthy"}), 200

@app.route('/')
def index():
    """Render the main game page."""
    return render_template('index.html')

@app.route('/start_game', methods=['POST'])
def start_game():
    """Start a new game and return the initial state."""
    # Create a new game instance
    game = NFLGame()
    game_state = game.start_game()
    
    # Generate a unique session ID if not already present
    if 'session_id' not in session:
        import uuid
        session['session_id'] = str(uuid.uuid4())
    
    # Store the game instance in our server-side dictionary
    session_id = session['session_id']
    GAME_INSTANCES[session_id] = game
    
    return jsonify(game_state)

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """Submit a player name and get the result."""
    # Get the player name from the request
    player_name = request.json.get('player_name', '')
    logger.debug(f"Received answer: {player_name}")
    
    # Get the session ID
    session_id = session.get('session_id')
    if not session_id or session_id not in GAME_INSTANCES:
        logger.warning(f"No game found for session_id: {session_id}")
        return jsonify({"error": "No active game. Please start a new game."}), 400
    
    # Get the game instance
    game = GAME_INSTANCES[session_id]
    
    # Submit the answer and get the result
    try:
        result = game.submit_answer(player_name)
        logger.debug(f"Result: {result}")
        return jsonify(result)
    except Exception as e:
        logger.exception(f"Error processing answer: {e}")
        return jsonify({"error": "An error occurred processing your answer."}), 500

@app.route('/game_state', methods=['GET'])
def get_game_state():
    """Get the current game state."""
    # Get the session ID
    session_id = session.get('session_id')
    if not session_id or session_id not in GAME_INSTANCES:
        return jsonify({"error": "No active game. Please start a new game."}), 400
    
    # Get the game instance
    game = GAME_INSTANCES[session_id]
    
    return jsonify(game.get_game_state())

@app.route('/timer_expired', methods=['POST'])
def timer_expired():
    """Handle timer expiration."""
    # Get the session ID
    session_id = session.get('session_id')
    if not session_id or session_id not in GAME_INSTANCES:
        logger.warning(f"No game found for session_id: {session_id}")
        return jsonify({"error": "No active game. Please start a new game."}), 400
    
    # Get the game instance
    game = GAME_INSTANCES[session_id]
    
    # Handle timer expiration
    try:
        result = game.timer_expired()
        logger.debug(f"Timer expired result: {result}")
        return jsonify(result)
    except Exception as e:
        logger.exception(f"Error handling timer expiration: {e}")
        return jsonify({"error": "An error occurred processing the timer expiration."}), 500

if __name__ == '__main__':
    # Use environment variables for production settings
    debug_mode = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Get port from environment variable (for Render compatibility)
    port = int(os.environ.get('PORT', 5001))
    
    app.run(host='0.0.0.0', port=port, debug=debug_mode) 