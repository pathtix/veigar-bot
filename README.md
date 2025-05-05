# League of Legends Desktop App

A desktop application for tracking League of Legends profiles and match history using Python and PyQt6.

## Setup Instructions

1. Ensure you have Python 3.8+ installed
2. Activate the virtual environment:
   ```
   # On Windows
   .venv\Scripts\activate
   
   # On Unix/MacOS
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the root directory and add your Riot API key:
   ```
   RIOT_API_KEY=your_api_key_here
   ```

## Project Structure

```
.
├── .env                    # Environment variables (create this file)
├── requirements.txt        # Project dependencies
├── src/                   
│   ├── main.py            # Application entry point
│   ├── api/               # Riot API integration
│   ├── ui/                # PyQt UI components
│   └── utils/             # Utility functions
```

## Features (Planned)
- Summoner profile lookup
- Match history tracking
- Detailed match statistics
- Performance analytics 