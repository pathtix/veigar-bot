from typing import Optional, Dict, Any, List
from concurrent.futures import ThreadPoolExecutor, as_completed
from .request_handler import RequestHandler
from .constants import Constants
from .exceptions import RiotAPIError

class RiotAPI:
    def __init__(
        self,
        api_key: Optional[str] = None,
        region: str = 'EUROPE',
        language: str = 'en_US',
        max_workers: int = 4,  # Number of concurrent requests
        debug_mode: bool = False
    ):
        """
        Initialize the Riot API wrapper
        
        Args:
            api_key: Riot API key (optional, will use environment variable if not provided)
            region: Default region to use (e.g., 'EUROPE', 'AMERICAS')
            language: Default language for responses
            max_workers: Maximum number of concurrent requests
            debug_mode: Whether to print API request logs to terminal
        """
        self.handler = RequestHandler(
            api_key=api_key, 
            language=language, 
            debug_mode=debug_mode
        )
        self.region = region.upper()
        self.max_workers = max_workers
        
    def get_account_by_riot_id(self, game_name: str, tag_line: str) -> Optional[Dict[str, Any]]:
        """
        Fetch account details using Riot ID (game name and tagline)
        
        Args:
            game_name: The game name (e.g., 'pathrix')
            tag_line: The tag line (e.g., 'tr1')
            
        Returns:
            Dictionary containing account information or None if not found
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=self.region,
                endpoint_group='ACCOUNT_V1_APIS',
                endpoint_name='by-riot-id',
                gameName=game_name,
                tagLine=tag_line
            )
            
            return self.handler.get(url, endpoint='account-v1')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching account: {e.message}")
            return None
            
    def get_account_by_puuid(self, puuid: str) -> Optional[Dict[str, Any]]:
        """
        Fetch account details using PUUID
        
        Args:
            puuid: Player Universally Unique IDentifier
            
        Returns:
            Dictionary containing account information or None if not found
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=self.region,
                endpoint_group='ACCOUNT_V1_APIS',
                endpoint_name='by-puuid',
                puuid=puuid
            )
            
            return self.handler.get(url, endpoint='account-v1')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching account: {e.message}")
            return None

    def get_summoner_by_puuid(self, puuid: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Fetch summoner details using PUUID
        
        Args:
            puuid: Player Universally Unique IDentifier
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Dictionary containing summoner information or None if not found
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='SUMMONER_V4_APIS',
                endpoint_name='by-puuid',
                encryptedPUUID=puuid
            )
            
            return self.handler.get(url, endpoint='summoner-v4')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching summoner: {e.message}")
            return None

    def get_match_history(
        self,
        puuid: str,
        start: int = 0,
        count: int = 20,
        queue_type: Optional[int] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
    ) -> Optional[List[str]]:
        """
        Fetch match history for a player
        
        Args:
            puuid: Player Universally Unique IDentifier
            start: Start index for pagination
            count: Number of matches to retrieve (max 100)
            queue_type: Queue type ID to filter matches
            start_time: Epoch timestamp in seconds - filter games after this time
            end_time: Epoch timestamp in seconds - filter games before this time
            
        Returns:
            List of match IDs or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=self.region,
                endpoint_group='MATCH_V5_APIS',
                endpoint_name='by-puuid',
                puuid=puuid
            )
            
            params = {
                'start': start,
                'count': min(count, 100)  # API limit is 100
            }
            
            if queue_type is not None:
                params['queue'] = queue_type
            if start_time is not None:
                params['startTime'] = start_time
            if end_time is not None:
                params['endTime'] = end_time
            
            return self.handler.get(url, endpoint='match-v5', params=params)
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching match history: {e.message}")
            return None

    def get_match_details(self, match_id: str) -> Optional[Dict[str, Any]]:
        """
        Fetch detailed information about a specific match
        
        Args:
            match_id: Match ID to fetch details for
            
        Returns:
            Dictionary containing match details or None if not found
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=self.region,
                endpoint_group='MATCH_V5_APIS',
                endpoint_name='by-match',
                matchId=match_id
            )
            
            return self.handler.get(url, endpoint='match-v5')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching match details: {e.message}")
            return None

    def get_champion_masteries(self, puuid: str, platform: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get all champion mastery entries for a player
        
        Args:
            puuid: Player Universally Unique IDentifier
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            List of champion mastery entries or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='CHAMPION_MASTERY_V4_APIS',
                endpoint_name='by-puuid',
                encryptedPUUID=puuid
            )
            
            return self.handler.get(url, endpoint='champion-mastery-v4')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching champion masteries: {e.message}")
            return None

    def get_champion_mastery(self, puuid: str, champion_id: int, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get champion mastery for a specific champion
        
        Args:
            puuid: Player Universally Unique IDentifier
            champion_id: Champion ID to get mastery for
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Champion mastery information or None if not found
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='CHAMPION_MASTERY_V4_APIS',
                endpoint_name='by-champion',
                encryptedPUUID=puuid,
                championId=champion_id
            )
            
            return self.handler.get(url, endpoint='champion-mastery-v4')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching champion mastery: {e.message}")
            return None

    def get_total_mastery_score(self, puuid: str, platform: str) -> Optional[int]:
        """
        Get total champion mastery score
        
        Args:
            puuid: Player Universally Unique IDentifier
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Total mastery score or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='CHAMPION_MASTERY_V4_APIS',
                endpoint_name='scores',
                encryptedPUUID=puuid
            )
            
            return self.handler.get(url, endpoint='champion-mastery-v4')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching total mastery score: {e.message}")
            return None

    def get_league_entries(self, puuid: str, platform: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get league entries for a player
        
        Args:
            puuid: Player Universally Unique IDentifier
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            List of league entries or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='LEAGUE_V4_APIS',
                endpoint_name='by-puuid',
                encryptedPUUID=puuid
            )
            
            return self.handler.get(url, endpoint='league-v4', limit_type='by-puuid')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching league entries: {e.message}")
            return None

    def get_challenger_league(self, queue: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get challenger league for a specific queue
        
        Args:
            queue: Queue type (e.g., 'RANKED_SOLO_5x5')
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Challenger league information or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='LEAGUE_V4_APIS',
                endpoint_name='challenger',
                queue=queue
            )
            
            return self.handler.get(url, endpoint='league-v4', limit_type='challenger')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching challenger league: {e.message}")
            return None

    def get_grandmaster_league(self, queue: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get grandmaster league for a specific queue
        
        Args:
            queue: Queue type (e.g., 'RANKED_SOLO_5x5')
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Grandmaster league information or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='LEAGUE_V4_APIS',
                endpoint_name='grandmaster',
                queue=queue
            )
            
            return self.handler.get(url, endpoint='league-v4', limit_type='challenger')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching grandmaster league: {e.message}")
            return None

    def get_master_league(self, queue: str, platform: str) -> Optional[Dict[str, Any]]:
        """
        Get master league for a specific queue
        
        Args:
            queue: Queue type (e.g., 'RANKED_SOLO_5x5')
            platform: Platform to query (e.g., 'euw1', 'na1')
            
        Returns:
            Master league information or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='LEAGUE_V4_APIS',
                endpoint_name='master',
                queue=queue
            )
            
            return self.handler.get(url, endpoint='league-v4', limit_type='challenger')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching master league: {e.message}")
            return None

    def get_league_entries_by_rank(
        self,
        queue: str,
        tier: str,
        division: str,
        platform: str,
        page: int = 1
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Get league entries for a specific rank
        
        Args:
            queue: Queue type (e.g., 'RANKED_SOLO_5x5')
            tier: Tier (e.g., 'DIAMOND', 'PLATINUM')
            division: Division (e.g., 'I', 'II')
            platform: Platform to query (e.g., 'euw1', 'na1')
            page: Page number for pagination
            
        Returns:
            List of league entries or None if error occurs
        """
        try:
            url = Constants.format_api_url(
                platform_or_region=platform,
                endpoint_group='LEAGUE_V4_APIS',
                endpoint_name='by-queue',
                queue=queue,
                tier=tier,
                division=division
            )
            
            params = {'page': page}
            return self.handler.get(url, endpoint='league-v4', params=params, limit_type='by-queue')
            
        except RiotAPIError as e:
            self.handler.logger.error(f"Error fetching league entries: {e.message}")
            return None

    def get_match_history_batch(self, puuid: str, count: int = 20, start: int = 0) -> List[Dict[str, Any]]:
        """
        Fetch match history with details in one batch operation
        
        Args:
            puuid: Player Universally Unique IDentifier
            count: Number of matches to retrieve
            start: Start index for pagination
            
        Returns:
            List of match details
        """
        # Get match history IDs
        match_ids = self.get_match_history(puuid, count=count, start=start)
        
        if not match_ids:
            return []
            
        # Create a thread pool to fetch match details in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit tasks for each match ID
            future_to_match = {
                executor.submit(self.get_match_details, match_id): match_id
                for match_id in match_ids
            }
            
            # Collect results as they complete
            match_details = []
            for future in as_completed(future_to_match):
                match_id = future_to_match[future]
                try:
                    data = future.result()
                    if data:
                        match_details.append(data)
                except Exception as e:
                    self.handler.logger.error(f"Error processing match {match_id}: {str(e)}")
            
        return match_details 