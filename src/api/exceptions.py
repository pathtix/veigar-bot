class RiotAPIError(Exception):
    """Base exception class for Riot API errors"""
    def __init__(self, message: str, status_code: int = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class RateLimitError(RiotAPIError):
    """Raised when API rate limits are exceeded"""
    def __init__(self, retry_after: int = None):
        self.retry_after = retry_after
        message = f"Rate limit exceeded. Retry after {retry_after} seconds" if retry_after else "Rate limit exceeded"
        super().__init__(message, status_code=429)

class APIKeyError(RiotAPIError):
    """Raised when there are issues with the API key"""
    def __init__(self):
        super().__init__("Invalid or expired API key", status_code=403)

class SummonerNotFoundError(RiotAPIError):
    """Raised when a summoner is not found"""
    def __init__(self, summoner_name: str):
        super().__init__(f"Summoner '{summoner_name}' not found", status_code=404)

class RegionError(RiotAPIError):
    """Raised when an invalid region is specified"""
    def __init__(self, region: str):
        super().__init__(f"Invalid region: {region}")

class MatchNotFoundError(RiotAPIError):
    """Raised when a match is not found"""
    def __init__(self, match_id: str):
        super().__init__(f"Match '{match_id}' not found", status_code=404)

class ValidationError(RiotAPIError):
    """Raised when request parameters fail validation"""
    def __init__(self, field: str, reason: str):
        super().__init__(f"Validation error for {field}: {reason}", status_code=400)

class ServiceUnavailableError(RiotAPIError):
    """Raised when the Riot API service is unavailable"""
    def __init__(self):
        super().__init__("Riot API service is currently unavailable", status_code=503)

class DataNotFoundError(RiotAPIError):
    """Raised when requested data is not found"""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(f"{resource_type} '{resource_id}' not found", status_code=404)

class TournamentError(RiotAPIError):
    """Raised when there are issues with tournament operations"""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(f"Tournament error: {message}", status_code=status_code)

class ChampionMasteryError(RiotAPIError):
    """Raised when there are issues with champion mastery data"""
    def __init__(self, summoner_id: str, champion_id: str = None):
        message = f"Champion mastery data not found for summoner '{summoner_id}'"
        if champion_id:
            message += f" and champion '{champion_id}'"
        super().__init__(message, status_code=404)

class LeagueError(RiotAPIError):
    """Raised when there are issues with league data"""
    def __init__(self, queue: str = None, tier: str = None, division: str = None):
        message = "League data error"
        if queue:
            message += f" for queue '{queue}'"
        if tier:
            message += f" tier '{tier}'"
        if division:
            message += f" division '{division}'"
        super().__init__(message, status_code=404)

class SpectatorError(RiotAPIError):
    """Raised when there are issues with spectator data"""
    def __init__(self, summoner_id: str = None):
        message = "Spectator data error"
        if summoner_id:
            message += f": No active game found for summoner '{summoner_id}'"
        super().__init__(message, status_code=404)

class ChallengesError(RiotAPIError):
    """Raised when there are issues with challenges data"""
    def __init__(self, challenge_id: str = None, level: str = None):
        message = "Challenges data error"
        if challenge_id:
            message += f" for challenge '{challenge_id}'"
        if level:
            message += f" at level '{level}'"
        super().__init__(message, status_code=404)

class NetworkError(RiotAPIError):
    """Raised when there are network connectivity issues"""
    def __init__(self, original_error: Exception = None):
        message = "Network error occurred while connecting to Riot API"
        if original_error:
            message += f": {str(original_error)}"
        super().__init__(message, status_code=None)

class TimeoutError(RiotAPIError):
    """Raised when the API request times out"""
    def __init__(self, timeout: float = None):
        message = "Request timed out"
        if timeout:
            message += f" after {timeout} seconds"
        super().__init__(message, status_code=None)

class ParseError(RiotAPIError):
    """Raised when there are issues parsing API response"""
    def __init__(self, detail: str = None):
        message = "Failed to parse API response"
        if detail:
            message += f": {detail}"
        super().__init__(message, status_code=None)
