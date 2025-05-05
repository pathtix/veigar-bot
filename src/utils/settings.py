import json
import os
import logging
from pathlib import Path

class Settings:
    """Handles application settings storage and retrieval"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Define default settings
        self.defaults = {
            "default_player_name": "",
            "default_tag_line": "",
            "default_region": "NA",
            "auto_search_on_startup": False
        }
        
        # Current settings (loaded from file or defaults)
        self.current = self.defaults.copy()
        
        # Settings file location
        self.settings_dir = Path.home() / ".veigar_bot"
        self.settings_file = self.settings_dir / "settings.json"
        
        # Create directory if it doesn't exist
        self.settings_dir.mkdir(exist_ok=True)
        
        # Load settings
        self.load()
    
    def load(self):
        """Load settings from file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    loaded_settings = json.load(f)
                    
                # Update current settings with loaded values
                for key, value in loaded_settings.items():
                    if key in self.defaults:  # Only accept known settings
                        self.current[key] = value
                        
                self.logger.info("Settings loaded successfully")
            else:
                self.logger.info("No settings file found, using defaults")
                self.save()  # Create default settings file
        except Exception as e:
            self.logger.error(f"Error loading settings: {str(e)}")
            # Reset to defaults if loading fails
            self.current = self.defaults.copy()
    
    def save(self):
        """Save current settings to file"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.current, f, indent=4)
            self.logger.info("Settings saved successfully")
            return True
        except Exception as e:
            self.logger.error(f"Error saving settings: {str(e)}")
            return False
    
    def get(self, key, default=None):
        """Get a setting value"""
        return self.current.get(key, default)
    
    def set(self, key, value):
        """Set a setting value and save to file"""
        if key in self.defaults:
            self.current[key] = value
            return self.save()
        return False
    
    def reset(self):
        """Reset settings to defaults"""
        self.current = self.defaults.copy()
        return self.save() 