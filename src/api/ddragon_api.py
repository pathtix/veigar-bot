import requests
from typing import Optional, Dict, Any, List
import logging

class DataDragonAPI:
    BASE_URL = "https://ddragon.leagueoflegends.com"
    
    def __init__(self, language: str = "en_US"):
        """
        Initialize the Data Dragon API wrapper
        
        Args:
            language: Language code for responses (e.g., 'en_US', 'ko_KR')
        """
        self.language = language
        self.version = self._get_latest_version()
        self.champions = self._load_champion_data()
        self.items = self._load_item_data()
        self.runes = self._load_runes_data()
        self.summoner_spells = self._load_summoner_spell_data()
        self.logger = logging.getLogger(__name__)
        
    def _get_latest_version(self) -> str:
        """
        Get the latest game version from Data Dragon
        
        Returns:
            Latest version string (e.g., '15.9.1')
        """
        try:
            response = requests.get(f"{self.BASE_URL}/api/versions.json")
            response.raise_for_status()
            versions = response.json()
            return versions[0]  # First version is the latest
        except Exception as e:
            self.logger.error(f"Error fetching game version: {e}")
            return "15.9.1"  # Fallback to latest known version
            
    def _load_champion_data(self) -> Dict[str, Any]:
        """
        Load champion data from Data Dragon
        
        Returns:
            Dictionary containing champion data
        """
        try:
            url = f"{self.BASE_URL}/cdn/{self.version}/data/{self.language}/champion.json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['data']
        except Exception as e:
            self.logger.error(f"Error loading champion data: {e}")
            return {}

    def _load_item_data(self) -> Dict[str, Any]:
        """
        Load item data from Data Dragon
        
        Returns:
            Dictionary containing item data
        """
        try:
            url = f"{self.BASE_URL}/cdn/{self.version}/data/{self.language}/item.json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['data']
        except Exception as e:
            self.logger.error(f"Error loading item data: {e}")
            return {}

    def _load_runes_data(self) -> List[Dict[str, Any]]:
        """
        Load runes reforged data from Data Dragon
        
        Returns:
            List containing rune data
        """
        try:
            url = f"{self.BASE_URL}/cdn/{self.version}/data/{self.language}/runesReforged.json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            self.logger.error(f"Error loading runes data: {e}")
            return []

    def _load_summoner_spell_data(self) -> Dict[str, Any]:
        """
        Load summoner spell data from Data Dragon
        
        Returns:
            Dictionary containing summoner spell data
        """
        try:
            url = f"{self.BASE_URL}/cdn/{self.version}/data/{self.language}/summoner.json"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()['data']
        except Exception as e:
            self.logger.error(f"Error loading summoner spell data: {e}")
            return {}
            
    def get_champion_by_id(self, champion_id: int) -> Optional[Dict[str, Any]]:
        """
        Get champion information by champion ID
        
        Args:
            champion_id: Numeric champion ID
            
        Returns:
            Dictionary containing champion information or None if not found
        """
        try:
            # Find champion by key (which is the champion ID)
            for champion in self.champions.values():
                if int(champion['key']) == champion_id:
                    return champion
            return None
        except Exception as e:
            self.logger.error(f"Error getting champion by ID {champion_id}: {e}")
            return None
            
    def get_champion_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get champion information by name
        
        Args:
            name: Champion name (case-sensitive)
            
        Returns:
            Dictionary containing champion information or None if not found
        """
        return self.champions.get(name)

    def get_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """
        Get item information by item ID
        
        Args:
            item_id: Numeric item ID
            
        Returns:
            Dictionary containing item information or None if not found
        """
        return self.items.get(str(item_id))

    def get_rune_by_id(self, rune_id: int) -> Optional[Dict[str, Any]]:
        """
        Get rune information by rune ID
        
        Args:
            rune_id: Numeric rune ID
            
        Returns:
            Dictionary containing rune information or None if not found
        """
        for rune_tree in self.runes:
            # Check main runes
            if int(rune_tree['id']) == rune_id:
                return rune_tree
            # Check sub-runes
            for slot in rune_tree.get('slots', []):
                for rune in slot.get('runes', []):
                    if int(rune['id']) == rune_id:
                        return rune
        return None

    def get_summoner_spell_by_id(self, spell_id: int) -> Optional[Dict[str, Any]]:
        """
        Get summoner spell information by spell ID
        
        Args:
            spell_id: Numeric summoner spell ID
            
        Returns:
            Dictionary containing summoner spell information or None if not found
        """
        for spell in self.summoner_spells.values():
            if int(spell['key']) == spell_id:
                return spell
        return None
        
    def get_champion_square_asset(self, champion_name: str) -> str:
        """
        Get the URL for a champion's square image
        
        Args:
            champion_name: Champion name (e.g., 'Ahri', 'LeeSin')
            
        Returns:
            URL to the champion's square image
        """
        return f"{self.BASE_URL}/cdn/{self.version}/img/champion/{champion_name}.png"
        
    def get_champion_splash_art(self, champion_name: str, skin_num: int = 0) -> str:
        """
        Get the URL for a champion's splash art
        
        Args:
            champion_name: Champion name (e.g., 'Ahri', 'LeeSin')
            skin_num: Skin number (0 for default skin)
            
        Returns:
            URL to the champion's splash art
        """
        return f"{self.BASE_URL}/cdn/img/champion/splash/{champion_name}_{skin_num}.jpg"
        
    def get_champion_loading_art(self, champion_name: str, skin_num: int = 0) -> str:
        """
        Get the URL for a champion's loading screen art
        
        Args:
            champion_name: Champion name (e.g., 'Ahri', 'LeeSin')
            skin_num: Skin number (0 for default skin)
            
        Returns:
            URL to the champion's loading screen art
        """
        return f"{self.BASE_URL}/cdn/img/champion/loading/{champion_name}_{skin_num}.jpg"

    def get_item_icon(self, item_id: int) -> str:
        """
        Get the URL for an item's icon
        
        Args:
            item_id: Numeric item ID
            
        Returns:
            URL to the item's icon
        """
        return f"{self.BASE_URL}/cdn/{self.version}/img/item/{item_id}.png"

    def get_summoner_spell_icon(self, spell_name: str) -> str:
        """
        Get the URL for a summoner spell's icon
        
        Args:
            spell_name: Spell name (e.g., 'SummonerFlash')
            
        Returns:
            URL to the summoner spell's icon
        """
        return f"{self.BASE_URL}/cdn/{self.version}/img/spell/{spell_name}.png"

    def get_profile_icon(self, icon_id: int) -> str:
        """
        Get the URL for a profile icon
        
        Args:
            icon_id: Numeric profile icon ID
            
        Returns:
            URL to the profile icon
        """
        return f"{self.BASE_URL}/cdn/{self.version}/img/profileicon/{icon_id}.png"

    def get_rune_icon(self, icon_path: str) -> str:
        """
        Get the URL for a rune's icon
        
        Args:
            icon_path: Icon path from the rune data
            
        Returns:
            URL to the rune's icon
        """
        return f"{self.BASE_URL}/cdn/img/{icon_path}"
        
    def get_all_champions(self) -> Dict[str, Any]:
        """
        Get information about all champions
        
        Returns:
            Dictionary containing all champion data
        """
        return self.champions

    def get_all_items(self) -> Dict[str, Any]:
        """
        Get information about all items
        
        Returns:
            Dictionary containing all item data
        """
        return self.items

    def get_all_runes(self) -> List[Dict[str, Any]]:
        """
        Get information about all runes
        
        Returns:
            List containing all rune data
        """
        return self.runes

    def get_all_summoner_spells(self) -> Dict[str, Any]:
        """
        Get information about all summoner spells
        
        Returns:
            Dictionary containing all summoner spell data
        """
        return self.summoner_spells

    def get_champion_icon(self, champion_id: int) -> str:
        """
        Get the URL for a champion's icon by champion ID
        
        Args:
            champion_id: Numeric champion ID
            
        Returns:
            URL to the champion's square icon
        """
        champion = self.get_champion_by_id(champion_id)
        if champion:
            return self.get_champion_square_asset(champion['id'])
        return f"{self.BASE_URL}/cdn/{self.version}/img/champion/unknown.png"  # Fallback icon 