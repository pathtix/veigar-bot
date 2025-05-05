# Veigar Bot - League of Legends Stats Tracker

A desktop application built with Python and PyQt6 that allows users to track League of Legends player statistics, match history, and rankings.

## Features

- **Player Search**: Look up players by their Riot ID (game name and tag line)
- **Profile Information**: View summoner level and profile icon
- **Rank Display**: See Solo/Duo and Flex queue rankings with detailed statistics
- **Match History**: Browse through recent matches with detailed performance statistics
  - **Detailed Queue Information**: Clear display of game modes (Ranked Solo/Duo, Normal Draft, ARAM, etc.)
- **Champion & Item Display**: Visual representation of champions played and items built
- **Multi-Region Support**: Access player data from all major League of Legends regions
- **Centralized Constants**: All game-related constants (regions, queue types) maintained in a single location
- **Debug Mode**: Optional logging of API requests to the terminal for debugging

## Prerequisites

- Python 3.8 or higher
- A Riot Games API Key (get one from [Riot Developer Portal](https://developer.riotgames.com))

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/veigar-bot.git
cd veigar-bot
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root and add your Riot API key:
```
RIOT_API_KEY=your_api_key_here
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Enter a player's Riot ID (game name and tag) in the search fields
3. Select the appropriate region from the dropdown menu
4. Click "Search" to view the player's statistics
5. Use the match history controls to load more or fewer matches

## Project Structure

```
veigar-bot/
├── src/
│   ├── api/
│   │   ├── constants.py
│   │   ├── ddragon_api.py
│   │   ├── exceptions.py
│   │   ├── request_handler.py
│   │   └── riot_api.py
│   ├── ui/
│   │   ├── main_window.py
│   │   ├── settings_dialog.py
│   │   ├── styles.py
│   │   └── workers.py
│   ├── utils/
│   │   └── settings.py
│   ├── assets/
│   │   └── application_icon.ico
│   └── main.py
├── requirements.txt
├── .env
└── README.md
```

## Dependencies

- PyQt6: Modern GUI framework
- Requests: HTTP library for API calls
- python-dotenv: Environment variable management
- Additional dependencies listed in requirements.txt

## Rate Limiting

The application respects Riot Games API rate limits:
- 20 requests per 1 second
- 100 requests per 2 minutes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Disclaimer

Veigar Bot isn't endorsed by Riot Games and doesn't reflect the views or opinions of Riot Games or anyone officially involved in producing or managing Riot Games properties. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc. 