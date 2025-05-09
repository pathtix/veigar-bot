import os
import time
import json
import logging
from typing import Optional, Dict, Any, Union, List
import requests
from dotenv import load_dotenv

from .constants import Constants
from .exceptions import (
    RiotAPIError, RateLimitError, APIKeyError, ValidationError,
    ServiceUnavailableError, NetworkError, TimeoutError, ParseError
)

class RateLimit:
    def __init__(self, limit: int, interval: int):
        self.limit = limit
        self.interval = interval
        self.requests = []
        
    def can_make_request(self) -> bool:
        now = time.time()
        # Remove old requests outside the interval
        self.requests = [req_time for req_time in self.requests if now - req_time < self.interval]
        return len(self.requests) < self.limit
        
    def add_request(self):
        self.requests.append(time.time())
        
    def get_wait_time(self) -> float:
        if self.can_make_request():
            return 0
        now = time.time()
        oldest_request = self.requests[0]
        return max(0, self.interval - (now - oldest_request))

class RequestHandler:
    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        retry_count: int = 3,
        language: str = "en_US",
        debug_mode: bool = False
    ):
        """Initialize the request handler.
        
        Args:
            api_key: Riot API key. If not provided, will look for RIOT_API_KEY in environment
            timeout: Request timeout in seconds
            retry_count: Number of times to retry failed requests
            language: Default language for responses
            debug_mode: Whether to print API request logs to terminal
        """
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Set log level based on debug mode
        self.debug_mode = debug_mode
        if self.debug_mode:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)
        
        # Try to load API key with better error handling
        try:
            # First try the provided API key
            if api_key:
                self.api_key = api_key
                self.logger.info("Using provided API key")
                return

            # Try to load from environment variable first
            self.api_key = os.getenv('RIOT_API_KEY')
            if self.api_key:
                self.logger.info("Using API key from environment variable")
                return

            # Try to load from .env file in various locations
            env_locations = [
                '.env',  # Current directory
                '../.env',  # Parent directory
                '../../.env',  # Two levels up
                os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env'),  # Same directory as this file
                os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'),  # Parent of this file
            ]

            for env_path in env_locations:
                if os.path.exists(env_path):
                    load_dotenv(env_path)
                    self.api_key = os.getenv('RIOT_API_KEY')
                    if self.api_key:
                        self.logger.info(f"Using API key from {env_path}")
                        break

            if not self.api_key:
                raise APIKeyError(
                    "No API key found. To use this application, you need to:\n\n"
                    "1. Get a Riot Games API key from https://developer.riotgames.com\n"
                    "2. Create a file named '.env' in the application directory\n"
                    "3. Add this line to the .env file:\n"
                    "   RIOT_API_KEY=your_api_key_here\n"
                    "4. Replace 'your_api_key_here' with your actual Riot API key\n\n"
                    "If you already have an API key, make sure the .env file is in the correct location."
                )

        except Exception as e:
            self.logger.error(f"Error loading API key: {str(e)}")
            raise APIKeyError(str(e))

        self.timeout = timeout
        self.retry_count = retry_count
        self.language = language
        
        # Initialize session
        self.session = requests.Session()
        self.session.headers.update({
            'X-Riot-Token': self.api_key,
            'Accept-Language': language,
            'Accept-Charset': 'application/x-www-form-urlencoded; charset=UTF-8'
        })

        # Initialize rate limit tracking
        self.rate_limits = {
            'account-v1': RateLimit(500, 10),  # 500 requests per 10 seconds
            'match-v5': RateLimit(500, 10),    # 500 requests per 10 seconds
            'summoner-v4': RateLimit(500, 10), # 500 requests per 10 seconds
            'league-v4': {
                'default': RateLimit(500, 10),
                'by-queue': RateLimit(500, 10),
                'challenger': RateLimit(500, 10),
                'by-puuid': RateLimit(500, 10)
            }
        }

    def _handle_rate_limit(self, endpoint: str, limit_type: str = 'default') -> None:
        """Handle rate limiting for an endpoint"""
        rate_limit = self.rate_limits.get(endpoint)
        if isinstance(rate_limit, dict):
            rate_limit = rate_limit.get(limit_type, rate_limit['default'])
        
        if rate_limit:
            wait_time = rate_limit.get_wait_time()
            if wait_time > 0:
                self.logger.debug(f"Rate limit wait: {wait_time:.2f}s for {endpoint}")
                time.sleep(wait_time)
            rate_limit.add_request()

    def _handle_response(self, response: requests.Response, endpoint_info: str) -> Dict[str, Any]:
        """Handle API response and potential errors.
        
        Args:
            response: Response from API
            endpoint_info: Information about the endpoint for error messages
            
        Returns:
            Parsed JSON response
            
        Raises:
            Various RiotAPIError subclasses based on the error
        """
        try:
            if response.status_code == 200:
                return response.json()
                
            elif response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 0))
                raise RateLimitError(retry_after=retry_after)
                
            elif response.status_code == 403:
                raise APIKeyError()
                
            elif response.status_code == 400:
                raise ValidationError("request", response.text)
                
            elif response.status_code == 404:
                raise RiotAPIError(f"Resource not found: {endpoint_info}", status_code=404)
                
            elif response.status_code == 503:
                raise ServiceUnavailableError()
                
            else:
                raise RiotAPIError(
                    f"Unexpected status code {response.status_code}: {response.text}",
                    status_code=response.status_code
                )
                
        except json.JSONDecodeError as e:
            raise ParseError(f"Failed to parse response: {str(e)}")

    def request(
        self,
        method: str,
        url: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        limit_type: str = 'default'
    ) -> Dict[str, Any]:
        """Make a request to the Riot API.
        
        Args:
            method: HTTP method ('GET', 'POST', etc.)
            url: Complete API URL
            endpoint: Endpoint identifier for rate limiting (e.g., 'summoner-v4')
            params: Query parameters
            data: Request body for POST/PUT
            limit_type: Rate limit type to use
            
        Returns:
            Parsed JSON response
            
        Raises:
            Various exceptions based on the error type
        """
        retries = 0
        last_error = None
        
        # Log detailed request info in debug mode
        if self.debug_mode:
            debug_info = f"API Request: {method} {url}"
            if params:
                debug_info += f"\nParams: {params}"
            if data:
                debug_info += f"\nData: {data}"
            debug_info += f"\nEndpoint: {endpoint}, Limit type: {limit_type}"
            self.logger.debug(debug_info)
        
        while retries <= self.retry_count:
            try:
                # Handle rate limiting
                self._handle_rate_limit(endpoint, limit_type)
                
                # Make request
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=self.timeout
                )
                
                # Log response in debug mode
                if self.debug_mode:
                    self.logger.debug(f"Response status: {response.status_code}")
                    if response.status_code == 200:
                        # Log a preview of the response data (first 200 chars)
                        preview = response.text[:200] + ('...' if len(response.text) > 200 else '')
                        self.logger.debug(f"Response preview: {preview}")
                
                # Handle response
                return self._handle_response(response, f"{method} {url}")
                
            except RateLimitError as e:
                self.logger.warning(f"Rate limit hit: {str(e)}")
                if retries < self.retry_count:
                    time.sleep(e.retry_after)
                else:
                    raise
                    
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                last_error = e
                if retries < self.retry_count:
                    time.sleep(2 ** retries)  # Exponential backoff
                else:
                    if isinstance(e, requests.exceptions.Timeout):
                        raise TimeoutError(timeout=self.timeout)
                    else:
                        raise NetworkError(original_error=e)
                        
            retries += 1
            
        raise RiotAPIError(f"Request failed after {self.retry_count} retries. Last error: {str(last_error)}")

    def get(
        self,
        url: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        limit_type: str = 'default'
    ) -> Union[Dict[str, Any], List[Any], None]:
        """Make a GET request to the Riot API.
        
        Args:
            url: Complete API URL
            endpoint: Endpoint identifier for rate limiting (e.g., 'summoner-v4')
            params: Query parameters
            limit_type: Rate limit type to use
            
        Returns:
            Parsed JSON response or None if error occurs
            
        Example:
            >>> handler.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/SummonerName', 'summoner-v4')
        """
        try:
            if self.debug_mode:
                self.logger.debug(f"GET Request: {url}")
                if params:
                    self.logger.debug(f"Params: {params}")
            
            return self.request('GET', url, endpoint, params=params, limit_type=limit_type)
            
        except RiotAPIError as e:
            self.logger.error(f"GET request error: {e.message}")
            return None

    def post(self, url: str, endpoint: str, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Make a POST request.
        
        Args:
            url: API URL
            endpoint: Endpoint identifier
            data: Request body
            **kwargs: Additional arguments to pass to request()
            
        Returns:
            Parsed JSON response
        """
        try:
            if self.debug_mode:
                self.logger.debug(f"POST Request: {url}")
                self.logger.debug(f"Data: {data}")
                if kwargs:
                    self.logger.debug(f"Additional args: {kwargs}")
            
            return self.request('POST', url, endpoint, data=data, **kwargs)
            
        except RiotAPIError as e:
            self.logger.error(f"POST request error: {e.message}")
            return None 