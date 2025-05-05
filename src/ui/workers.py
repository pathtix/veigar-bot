from PyQt6.QtCore import QThread, pyqtSignal, Qt
from typing import Optional, Dict, Any, List
from PyQt6.QtGui import QPixmap, QImage
import requests
from PyQt6.QtWidgets import QLabel

class SearchWorker(QThread):
    finished = pyqtSignal(dict)
    error = pyqtSignal(str) 
    
    def __init__(self, riot_api, game_name: str, tag_line: str, platform: str):
        super().__init__()
        self.riot_api = riot_api
        self.game_name = game_name
        self.tag_line = tag_line
        self.platform = platform
        
    def run(self):
        try:
            # Get account information
            account_info = self.riot_api.get_account_by_riot_id(self.game_name, self.tag_line)
            
            if not account_info:
                self.error.emit("Player not found")
                return
                
            puuid = account_info.get('puuid')
            
            # Get summoner information
            summoner_info = self.riot_api.get_summoner_by_puuid(puuid, platform=self.platform)
            
            if not summoner_info:
                self.error.emit("Could not fetch summoner information")
                return
                
            # Get league entries
            league_entries = self.riot_api.get_league_entries(puuid, platform=self.platform)
            
            # Compile all results
            results = {
                'account_info': account_info,
                'summoner_info': summoner_info,
                'league_entries': league_entries or []
            }
            
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))

class MatchHistoryWorker(QThread):
    finished = pyqtSignal(list)
    error = pyqtSignal(str)
    progress = pyqtSignal(int)
    
    def __init__(self, riot_api, puuid: str, count: int, offset: int = 0):
        super().__init__()
        self.riot_api = riot_api
        self.puuid = puuid
        self.count = count
        self.offset = offset
        
    def run(self):
        try:
            self.progress.emit(10)  # Show initial progress
            
            # Get match history and details in parallel
            match_details = self.riot_api.get_match_history_batch(self.puuid, count=self.count, start=self.offset)
            
            if not match_details:
                self.progress.emit(100)
                self.finished.emit([])
                return
            
            self.progress.emit(90)  # Most of the work is done
            
            # Sort matches by game creation time (newest first)
            match_details.sort(
                key=lambda x: x.get('info', {}).get('gameCreation', 0),
                reverse=True
            )
            
            self.progress.emit(100)
            self.finished.emit(match_details)
            
        except Exception as e:
            self.error.emit(str(e)) 

class IconLoaderWorker(QThread):
    finished = pyqtSignal(QPixmap, object)  # Emits (pixmap, target_label)
    error = pyqtSignal(str, object)         # Emits (error_message, target_label)
    
    def __init__(self, url: str, size: tuple, target_label: QLabel):
        super().__init__()
        self.url = url
        self.size = size
        self.target_label = target_label
        
    def run(self):
        try:
            response = requests.get(self.url)
            image = QImage.fromData(response.content)
            pixmap = QPixmap.fromImage(image)
            scaled_pixmap = pixmap.scaled(
                self.size[0], self.size[1],
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.finished.emit(scaled_pixmap, self.target_label)
        except Exception as e:
            self.error.emit(str(e), self.target_label) 