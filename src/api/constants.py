class Constants:
    PLATFORMS = {
        'br1': 'br1.api.riotgames.com',
        'eun1': 'eun1.api.riotgames.com',
        'euw1': 'euw1.api.riotgames.com',
        'jp1': 'jp1.api.riotgames.com',
        'kr': 'kr.api.riotgames.com',
        'la1': 'la1.api.riotgames.com',
        'la2': 'la2.api.riotgames.com',
        'na1': 'na1.api.riotgames.com',
        'oc1': 'oc1.api.riotgames.com',
        'tr1': 'tr1.api.riotgames.com',
        'ru': 'ru.api.riotgames.com',
        'ph2': 'ph2.api.riotgames.com',
        'sg2': 'sg2.api.riotgames.com',
        'th2': 'th2.api.riotgames.com',
        'tw2': 'tw2.api.riotgames.com',
        'vn2': 'vn2.api.riotgames.com',
    }

    REGIONS = {
        'AMERICAS': 'americas.api.riotgames.com',
        'ASIA': 'asia.api.riotgames.com',
        'EUROPE': 'europe.api.riotgames.com',
        'SEA': 'sea.api.riotgames.com',
    }

    LOCALES = {
        'cs_CZ': 'Czech (Czech Republic)',
        'el_GR': 'Greek (Greece)',
        'pl_PL': 'Polish (Poland)',
        'ro_RO': 'Romanian (Romania)',
        'hu_HU': 'Hungarian (Hungary)',
        'en_GB': 'English (United Kingdom)',
        'de_DE': 'German (Germany)',
        'es_ES': 'Spanish (Spain)',
        'it_IT': 'Italian (Italy)',
        'fr_FR': 'French (France)',
        'ja_JP': 'Japanese (Japan)',
        'ko_KR': 'Korean (Korea)',
        'es_MX': 'Spanish (Mexico)',
        'es_AR': 'Spanish (Argentina)',
        'pt_BR': 'Portuguese (Brazil)',
        'en_US': 'English (United States)',
        'en_AU': 'English (Australia)',
        'ru_RU': 'Russian (Russia)',
        'tr_TR': 'Turkish (Turkey)',
        'ms_MY': 'Malay (Malaysia)',
        'en_PH': 'English (Republic of the Philippines)',
        'en_SG': 'English (Singapore)',
        'th_TH': 'Thai (Thailand)',
        'vi_VN': 'Vietnamese (Viet Nam)',
        'id_ID': 'Indonesian (Indonesia)',
        'zh_MY': 'Chinese (Malaysia)',
        'zh_CN': 'Chinese (China)',
        'zh_TW': 'Chinese (Taiwan)'
    }

    ACCOUNT_V1_APIS = {
        'by-puuid': '/riot/account/v1/accounts/by-puuid/{puuid}',
        'by-riot-id': '/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}'
    }

    CHAMPION_V3_APIS = {
        'champion-rotations': '/lol/platform/v3/champion-rotations'
    }

    CHAMPION_MASTERY_V4_APIS = {
        'by-puuid': '/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}',
        'by-champion': '/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/by-champion/{championId}',
        'scores': '/lol/champion-mastery/v4/scores/by-puuid/{encryptedPUUID}',
        'top': '/lol/champion-mastery/v4/champion-masteries/by-puuid/{encryptedPUUID}/top'
    }

    CLASH_V1_APIS = {
        'by-team': '/lol/clash/v1/teams/{teamId}',
        'tournament': '/lol/clash/v1/tournaments/{tournamentId}',
        'tournament-team': '/lol/clash/v1/tournaments/by-team/{teamId}',
        'tournaments': '/lol/clash/v1/tournaments',
        'by-puuid': '/lol/clash/v1/players/by-puuid/{puuid}'
    }

    LEAGUE_V4_APIS = {
        'challenger': '/lol/league/v4/challengerleagues/by-queue/{queue}',
        'by-league': '/lol/league/v4/leagues/{leagueId}',
        'master': '/lol/league/v4/masterleagues/by-queue/{queue}',
        'grandmaster': '/lol/league/v4/grandmasterleagues/by-queue/{queue}',
        'by-summoner': '/lol/league/v4/entries/by-summoner/{encryptedSummonerId}',
        'by-queue': '/lol/league/v4/entries/{queue}/{tier}/{division}',
        'by-puuid': '/lol/league/v4/entries/by-puuid/{encryptedPUUID}'
    }

    LEAGUE_EXP_V4_APIS = {
        'entries': '/lol/league-exp/v4/entries/{queue}/{tier}/{division}'
    }

    LOL_STATUS_V4_APIS = {
        'platform-data': '/lol/status/v4/platform-data'
    }

    MATCH_V5_APIS = {
        'by-match': '/lol/match/v5/matches/{matchId}',
        'by-puuid': '/lol/match/v5/matches/by-puuid/{puuid}/ids',
        'timeline': '/lol/match/v5/matches/{matchId}/timeline'
    }

    SPECTATOR_V5_APIS = {
        'featured': '/lol/spectator/v5/featured-games',
        'active': '/lol/spectator/v5/active-games/by-summoner/{encryptedPUUID}'
    }

    SUMMONER_V4_APIS = {
        'by-account': '/lol/summoner/v4/summoners/by-account/{encryptedAccountId}',
        'by-summoner': '/lol/summoner/v4/summoners/{encryptedSummonerId}',
        'by-puuid': '/lol/summoner/v4/summoners/by-puuid/{encryptedPUUID}'
    }

    CHALLENGES_V1_APIS = {
        'percentiles': '/lol/challenges/v1/challenges/percentiles',
        'leaderboards': '/lol/challenges/v1/challenges/{challengeId}/leaderboards/by-level/{level}',
        'challenge-percentiles': '/lol/challenges/v1/challenges/{challengeId}/percentiles',
        'challenge-config': '/lol/challenges/v1/challenges/{challengeId}/config',
        'player-data': '/lol/challenges/v1/player-data/{puuid}',
        'config': '/lol/challenges/v1/challenges/config'
    }

    TOURNAMENT_STUB_V5_APIS = {
        'codes': '/lol/tournament-stub/v5/codes',
        'lobby-events': '/lol/tournament-stub/v5/lobby-events/by-code/{tournamentCode}',
        'tournament-codes': '/lol/tournament-stub/v5/codes/{tournamentCode}',
        'providers': '/lol/tournament-stub/v5/providers',
        'tournaments': '/lol/tournament-stub/v5/tournaments'
    }

    # Rate Limits
    RATE_LIMITS = {
        'account-v1': {
            'default': {'requests': 1000, 'seconds': 60},
            'extended': {'requests': 20000, 'seconds': 10}
        },
        'champion-v3': {
            'short': {'requests': 30, 'seconds': 10},
            'long': {'requests': 500, 'seconds': 600}
        },
        'champion-mastery-v4': {
            'default': {'requests': 20000, 'seconds': 10},
            'extended': {'requests': 1200000, 'seconds': 600}
        },
        'clash-v1': {
            'team': {'requests': 200, 'seconds': 60},
            'tournament': {'requests': 10, 'seconds': 60},
            'player': {'requests': 20000, 'seconds': 10}
        },
        'league-v4': {
            'challenger': {'requests': 30, 'seconds': 10},
            'league': {'requests': 500, 'seconds': 10},
            'entries': {'requests': 100, 'seconds': 60},
            'by-queue': {'requests': 50, 'seconds': 10},
            'by-puuid': {'requests': 20000, 'seconds': 10}
        },
        'league-exp-v4': {
            'default': {'requests': 50, 'seconds': 10}
        },
        'lol-status-v4': {
            'default': {'requests': 20000, 'seconds': 10},
            'extended': {'requests': 1200000, 'seconds': 600}
        },
        'match-v5': {
            'default': {'requests': 2000, 'seconds': 10}
        },
        'spectator-v5': {
            'default': {'requests': 20000, 'seconds': 10},
            'extended': {'requests': 1200000, 'seconds': 600}
        },
        'summoner-v4': {
            'default': {'requests': 1600, 'seconds': 60}
        },
        'challenges-v1': {
            'default': {'requests': 20000, 'seconds': 10},
            'extended': {'requests': 1200000, 'seconds': 600}
        },
        'tournament-stub-v5': {
            'default': {'requests': 20000, 'seconds': 10},
            'extended': {'requests': 1200000, 'seconds': 600}
        }
    }

    @classmethod
    def get_platform_url(cls, platform: str) -> str:
        """Get the base URL for a platform.
        
        Args:
            platform: Platform code (e.g., 'euw1', 'na1')
            
        Returns:
            Complete platform URL
            
        Raises:
            ValueError: If platform is invalid
        """
        if platform not in cls.PLATFORMS:
            raise ValueError(f"Invalid platform: {platform}. Valid platforms: {list(cls.PLATFORMS.keys())}")
        return f"https://{cls.PLATFORMS[platform]}"

    @classmethod
    def get_region_url(cls, region: str) -> str:
        """Get the base URL for a region.
        
        Args:
            region: Region code (e.g., 'AMERICAS', 'EUROPE')
            
        Returns:
            Complete region URL
            
        Raises:
            ValueError: If region is invalid
        """
        region = region.upper()
        if region not in cls.REGIONS:
            raise ValueError(f"Invalid region: {region}. Valid regions: {list(cls.REGIONS.keys())}")
        return f"https://{cls.REGIONS[region]}"

    @classmethod
    def get_rate_limit(cls, endpoint: str, limit_type: str = 'default') -> dict:
        """Get rate limit information for an endpoint.
        
        Args:
            endpoint: API endpoint (e.g., 'summoner-v4', 'match-v5')
            limit_type: Type of rate limit ('default', 'extended', 'short', 'long', etc.)
            
        Returns:
            Dictionary containing rate limit info: {'requests': int, 'seconds': int}
            
        Raises:
            ValueError: If endpoint or limit type is invalid
        """
        if endpoint not in cls.RATE_LIMITS:
            raise ValueError(f"Invalid endpoint: {endpoint}")
        
        limits = cls.RATE_LIMITS[endpoint]
        if limit_type not in limits:
            raise ValueError(f"Invalid limit type: {limit_type} for endpoint: {endpoint}")
            
        return limits[limit_type]

    @classmethod
    def format_api_url(cls, platform_or_region: str, endpoint_group: str, endpoint_name: str, **params) -> str:
        """Format a complete API URL with parameters.
        
        Args:
            platform_or_region: Platform code (e.g., 'euw1') or region (e.g., 'EUROPE')
            endpoint_group: API group (e.g., 'SUMMONER_V4_APIS', 'MATCH_V5_APIS')
            endpoint_name: Name of the specific endpoint
            **params: Parameters to format into the URL
            
        Returns:
            Complete formatted API URL
            
        Example:
            >>> Constants.format_api_url('euw1', 'SUMMONER_V4_APIS', 'by-name', summonerName='PlayerName')
            'https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/PlayerName'
        """
        # Get the endpoint group
        endpoint_group_attr = getattr(cls, endpoint_group, None)
        if endpoint_group_attr is None:
            raise ValueError(f"Invalid endpoint group: {endpoint_group}")
            
        # Get the specific endpoint
        if endpoint_name not in endpoint_group_attr:
            raise ValueError(f"Invalid endpoint name: {endpoint_name}")
        
        endpoint = endpoint_group_attr[endpoint_name]
        
        # Determine if this is a platform or region endpoint
        base_url = (cls.get_platform_url(platform_or_region) 
                   if platform_or_region.lower() in cls.PLATFORMS 
                   else cls.get_region_url(platform_or_region))
        
        # Format the URL with provided parameters
        try:
            formatted_endpoint = endpoint.format(**params)
            return f"{base_url}{formatted_endpoint}"
        except KeyError as e:
            raise ValueError(f"Missing required parameter: {e}")

    @classmethod
    def is_valid_locale(cls, locale: str) -> bool:
        """Check if a locale is valid.
        
        Args:
            locale: Locale code to check (e.g., 'en_US', 'ko_KR')
            
        Returns:
            bool: True if locale is valid, False otherwise
        """
        return locale in cls.LOCALES

    @classmethod
    def get_locale_name(cls, locale: str) -> str:
        """Get the human-readable name for a locale.
        
        Args:
            locale: Locale code (e.g., 'en_US', 'ko_KR')
            
        Returns:
            Human-readable locale name
            
        Raises:
            ValueError: If locale is invalid
        """
        if not cls.is_valid_locale(locale):
            raise ValueError(f"Invalid locale: {locale}")
        return cls.LOCALES[locale]

    @classmethod
    def get_endpoints_for_version(cls, version: str) -> list:
        """Get all endpoints for a specific API version.
        
        Args:
            version: API version (e.g., 'v4', 'v5')
            
        Returns:
            List of endpoint groups that match the version
        """
        return [attr for attr in dir(cls) 
                if attr.endswith(f'_{version}_APIS') 
                and not attr.startswith('__')]

    
