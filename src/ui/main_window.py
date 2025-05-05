from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QStatusBar, QComboBox,
    QFrame, QScrollArea, QSpinBox, QSizePolicy, QProgressBar,
    QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage, QIcon
import requests
from io import BytesIO
from api.riot_api import RiotAPI
from api.ddragon_api import DataDragonAPI
from api.exceptions import APIKeyError
from .styles import MAIN_STYLE
from .workers import SearchWorker, MatchHistoryWorker, IconLoaderWorker
import os
import logging

class ProfileWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("profileWidget")
        
        layout = QHBoxLayout(self)
        
        # Profile Icon Section
        self.profile_icon = QLabel("Profile\nIcon\nHere")
        self.profile_icon.setFixedSize(100, 100)
        self.profile_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.profile_icon.setObjectName("profileIcon")
        layout.addWidget(self.profile_icon)
        
        # Right side info section
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setSpacing(8)
        
        # Player name and level section
        self.player_header = QLabel()
        self.player_header.setObjectName("playerHeader")
        info_layout.addWidget(self.player_header)
        
        # Rank Information Section
        rank_widget = QWidget()
        rank_widget.setObjectName("rankInfo")
        rank_layout = QVBoxLayout(rank_widget)
        rank_layout.setSpacing(4)
        
        # Solo/Duo Rank
        self.solo_rank_label = QLabel("Unranked")
        self.solo_rank_label.setObjectName("rankTitle")
        rank_layout.addWidget(self.solo_rank_label)
        
        self.solo_rank_stats = QLabel("")
        rank_layout.addWidget(self.solo_rank_stats)
        
        # Flex Rank
        self.flex_rank_label = QLabel("Unranked (Flex)")
        self.flex_rank_label.setObjectName("rankTitle")
        rank_layout.addWidget(self.flex_rank_label)
        
        self.flex_rank_stats = QLabel("")
        rank_layout.addWidget(self.flex_rank_stats)
        
        info_layout.addWidget(rank_widget)
        layout.addWidget(info_widget)
        layout.setStretch(1, 1)

    def update_player_info(self, game_name: str, tag_line: str, level: int, region: str):
        """Update player information display"""
        header_text = f"""
        <div style='color: #4a90e2;'>
            <span style='font-size: 24px;'>{game_name}#{tag_line}</span>
            <span style='color: #888888; margin-left: 20px;'>Region: {region}</span>
        </div>
        <div style='color: #888888;'>Level: {level}</div>
        """
        self.player_header.setText(header_text)

    def update_rank_info(self, league_entries):
        """Update rank information display"""
        for entry in league_entries:
            queue_type = entry.get('queueType', '')
            tier = entry.get('tier', 'UNRANKED')
            rank = entry.get('rank', '')
            lp = entry.get('leaguePoints', 0)
            wins = entry.get('wins', 0)
            losses = entry.get('losses', 0)
            win_rate = (wins / (wins + losses) * 100) if wins + losses > 0 else 0
            
            rank_text = f"{tier.title()} {rank}"
            stats_text = f"LP: {lp} | W: {wins} L: {losses} | Win Rate: {win_rate:.1f}%"
            
            if queue_type == 'RANKED_SOLO_5x5':
                self.solo_rank_label.setText(f"Solo/Duo: {rank_text}")
                self.solo_rank_stats.setText(stats_text)
            elif queue_type == 'RANKED_FLEX_SR':
                self.flex_rank_label.setText(f"Flex 5v5: {rank_text}")
                self.flex_rank_stats.setText(stats_text)

class MatchWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("matchWidget")
        
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        
        # Champion icon
        self.champion_icon = QLabel()
        self.champion_icon.setFixedSize(50, 50)
        self.champion_icon.setObjectName("championIcon")
        layout.addWidget(self.champion_icon)
        
        # Match details
        details_layout = QVBoxLayout()
        self.match_result = QLabel()
        self.match_result.setObjectName("matchResult")
        details_layout.addWidget(self.match_result)
        
        self.match_stats = QLabel()
        details_layout.addWidget(self.match_stats)
        layout.addLayout(details_layout)
        
        # Items
        items_widget = QWidget()
        items_layout = QHBoxLayout(items_widget)
        items_layout.setSpacing(2)
        self.item_icons = []
        for _ in range(7):  # 6 items + trinket
            item_label = QLabel()
            item_label.setFixedSize(30, 30)
            item_label.setObjectName("itemIcon")
            self.item_icons.append(item_label)
            items_layout.addWidget(item_label)
        layout.addWidget(items_widget)
        
        layout.setStretch(1, 1)

class MatchHistoryWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("matchHistoryWidget")
        
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header section
        header_layout = QHBoxLayout()
        
        # Title
        title = QLabel("Match History")
        title.setObjectName("matchHistoryTitle")
        header_layout.addWidget(title)
        
        # Match count selector
        self.match_count = QSpinBox()
        self.match_count.setRange(5, 20)
        self.match_count.setValue(5)
        self.match_count.setSingleStep(5)
        self.match_count.setObjectName("matchCount")
        header_layout.addWidget(self.match_count)
        
        # Load button
        self.load_button = QPushButton("Load Matches")
        self.load_button.setObjectName("loadButton")
        header_layout.addWidget(self.load_button)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.hide()
        header_layout.addWidget(self.progress_bar)
        
        header_layout.addStretch()
        layout.addLayout(header_layout)
        
        # Scroll area for matches
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setObjectName("matchScroll")
        
        # Container for matches
        self.matches_container = QWidget()
        self.matches_layout = QVBoxLayout(self.matches_container)
        self.matches_layout.setSpacing(8)
        self.matches_layout.addStretch()
        
        scroll.setWidget(self.matches_container)
        layout.addWidget(scroll)
        
        # Set size policy to expand
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

class MainWindow(QMainWindow):
    # Define platform mappings
    REGIONS = {
        'BR': ('AMERICAS', 'br1'),
        'EUN': ('EUROPE', 'eun1'),
        'EUW': ('EUROPE', 'euw1'),
        'JP': ('ASIA', 'jp1'),
        'KR': ('ASIA', 'kr'),
        'LA1': ('AMERICAS', 'la1'),
        'LA2': ('AMERICAS', 'la2'),
        'NA': ('AMERICAS', 'na1'),
        'OC': ('SEA', 'oc1'),
        'PH': ('SEA', 'ph2'),
        'RU': ('EUROPE', 'ru'),
        'SG': ('SEA', 'sg2'),
        'TH': ('SEA', 'th2'),
        'TR': ('EUROPE', 'tr1'),
        'TW': ('SEA', 'tw2'),
        'VN': ('SEA', 'vn2')
    }

    def __init__(self):
        super().__init__()
        
        # Set up logging
        self.logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
        
        try:
            # Initialize APIs
            self.riot_api = RiotAPI()
            self.ddragon = DataDragonAPI()
            
            # Set window properties
            self.setWindowTitle("Veigar Bot")
            self.setMinimumSize(800, 1000)
            
            # Set application icon
            self.set_application_icon()
            
            # Set stylesheet
            self.setStyleSheet(MAIN_STYLE)
            
            # Create central widget and layout
            self._setup_ui()
            
        except APIKeyError as e:
            QMessageBox.critical(
                self,
                "API Key Error",
                "Could not find a valid Riot API key. To use this application:\n\n"
                "1. Get a Riot Games API key from https://developer.riotgames.com\n"
                "2. Create a file named '.env' in the application directory\n"
                "3. Add this line to the .env file:\n"
                "   RIOT_API_KEY=your_api_key_here\n"
                "4. Replace 'your_api_key_here' with your actual Riot API key\n\n"
                "The application will now close."
            )
            raise
            
    def _setup_ui(self):
        """Set up the main UI components"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Search section
        search_frame = QFrame()
        search_frame.setObjectName("searchFrame")
        search_layout = QHBoxLayout(search_frame)
        search_layout.setSpacing(10)
        main_layout.addWidget(search_frame)
        
        # Region selector
        self.region_selector = QComboBox()
        self.region_selector.addItems(self.REGIONS.keys())
        self.current_platform = self.REGIONS[self.region_selector.currentText()][1]
        
        self.region_selector.currentTextChanged.connect(self.on_region_changed)
        self.region_selector.setMaximumWidth(100)
        search_layout.addWidget(self.region_selector)
        
        # Game name input
        self.game_name_input = QLineEdit()
        self.game_name_input.setPlaceholderText("Summoner Name")
        search_layout.addWidget(self.game_name_input)
        
        # Tag line input
        self.tag_line_input = QLineEdit()
        self.tag_line_input.setPlaceholderText("#TAG")
        self.tag_line_input.setMaximumWidth(100)
        search_layout.addWidget(self.tag_line_input)
        
        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_player)
        search_layout.addWidget(search_button)
        
        # Profile section
        self.profile_widget = ProfileWidget()
        self.profile_widget.hide()
        main_layout.addWidget(self.profile_widget)
        
        # Match history section
        self.match_history = MatchHistoryWidget()
        self.match_history.hide()
        self.match_history.load_button.clicked.connect(self.load_match_history)
        main_layout.addWidget(self.match_history, 1)
        
        # Add status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Store current summoner PUUID
        self.current_puuid = None
        
        # Initialize workers
        self.search_worker = None
        self.match_worker = None
        self.icon_workers = []  # List to keep track of icon loading workers

    def on_region_changed(self, region_code: str):
        """Handle region change"""
        region_info = self.REGIONS.get(region_code)
        if region_info:
            self.current_platform = region_info[1]
            self.status_bar.showMessage(f"Region changed to {region_code}")
    
    def closeEvent(self, event):
        """Handle application closure"""
        # Stop and clean up search worker
        if self.search_worker is not None:
            self.search_worker.quit()
            self.search_worker.wait()
            self.search_worker.deleteLater()

        # Stop and clean up match worker
        if self.match_worker is not None:
            self.match_worker.quit()
            self.match_worker.wait()
            self.match_worker.deleteLater()

        # Stop and clean up all icon workers
        for worker in self.icon_workers[:]:  # Create a copy of the list to iterate
            worker.quit()
            worker.wait()
            worker.deleteLater()
            self.icon_workers.remove(worker)

        super().closeEvent(event)

    def cleanup_icon_worker(self, worker):
        """Safely clean up an icon worker"""
        if worker in self.icon_workers:
            worker.quit()
            worker.wait()
            self.icon_workers.remove(worker)
            worker.deleteLater()

    def load_profile_icon(self, icon_id: int):
        """Load and display profile icon"""
        try:
            icon_url = self.ddragon.get_profile_icon(icon_id)
            worker = IconLoaderWorker(icon_url, (100, 100), self.profile_widget.profile_icon)
            worker.finished.connect(lambda pixmap, label: (
                self.on_icon_loaded(pixmap, label),
                self.cleanup_icon_worker(worker)
            ))
            worker.error.connect(lambda error, label: (
                self.on_icon_error(error, label),
                self.cleanup_icon_worker(worker)
            ))
            self.icon_workers.append(worker)
            worker.start()
        except Exception as e:
            self.status_bar.showMessage(f"Error loading profile icon: {str(e)}")
    
    def load_champion_icon(self, champion_id: int, label: QLabel):
        """Load and display champion icon"""
        try:
            self.status_bar.showMessage(f"Loading champion icon for ID: {champion_id}")
            icon_url = self.ddragon.get_champion_icon(champion_id)
            self.status_bar.showMessage(f"Champion icon URL: {icon_url}")
            worker = IconLoaderWorker(icon_url, (50, 50), label)
            worker.finished.connect(lambda pixmap, label: (
                self.on_icon_loaded(pixmap, label),
                self.cleanup_icon_worker(worker)
            ))
            worker.error.connect(lambda error, label: (
                self.on_icon_error(error, label),
                self.cleanup_icon_worker(worker)
            ))
            self.icon_workers.append(worker)
            worker.start()
        except Exception as e:
            self.status_bar.showMessage(f"Error loading champion icon: {str(e)}")
            label.clear()

    def load_item_icon(self, item_id: int, label: QLabel):
        """Load and display item icon"""
        try:
            if item_id > 0:
                icon_url = self.ddragon.get_item_icon(item_id)
                worker = IconLoaderWorker(icon_url, (30, 30), label)
                worker.finished.connect(lambda pixmap, label: (
                    self.on_icon_loaded(pixmap, label),
                    self.cleanup_icon_worker(worker)
                ))
                worker.error.connect(lambda error, label: (
                    self.on_icon_error(error, label),
                    self.cleanup_icon_worker(worker)
                ))
                self.icon_workers.append(worker)
                worker.start()
            else:
                label.clear()
        except Exception as e:
            self.status_bar.showMessage(f"Error loading item icon: {str(e)}")

    def on_icon_loaded(self, pixmap: QPixmap, label: QLabel):
        """Handle icon loading completion"""
        label.setPixmap(pixmap)

    def on_icon_error(self, error_message: str, label: QLabel):
        """Handle icon loading error"""
        label.clear()
        self.status_bar.showMessage(f"Error loading icon: {error_message}")

    def search_player(self):
        """Handle player search"""
        game_name = self.game_name_input.text().strip()
        tag_line = self.tag_line_input.text().strip().lstrip('#')
        
        if not game_name or not tag_line:
            self.status_bar.showMessage("Please enter both Game Name and Tag")
            return
        
        # Disable search button and show loading status
        self.status_bar.showMessage(f"Searching for {game_name}#{tag_line}...")
        self.game_name_input.setEnabled(False)
        self.tag_line_input.setEnabled(False)
        self.region_selector.setEnabled(False)
        
        # Create and start worker thread
        self.search_worker = SearchWorker(
            self.riot_api,
            game_name,
            tag_line,
            self.current_platform
        )
        self.search_worker.finished.connect(self.on_search_complete)
        self.search_worker.error.connect(self.on_search_error)
        self.search_worker.start()

    def on_search_complete(self, results):
        """Handle search completion"""
        try:
            account_info = results['account_info']
            summoner_info = results['summoner_info']
            league_entries = results['league_entries']
            
            self.current_puuid = account_info.get('puuid')
            
            # Update player information
            self.profile_widget.update_player_info(
                game_name=self.game_name_input.text().strip(),
                tag_line=self.tag_line_input.text().strip(),
                level=summoner_info.get('summonerLevel'),
                region=self.region_selector.currentText()
            )
            
            # Load profile icon
            self.load_profile_icon(summoner_info.get('profileIconId', 0))
            
            # Update rank information
            if league_entries:
                self.profile_widget.update_rank_info(league_entries)
            
            # Show widgets
            self.profile_widget.show()
            self.match_history.show()
            
            # Load initial match history
            self.load_match_history()
            
            self.status_bar.showMessage("Player found!")
            
        except Exception as e:
            self.status_bar.showMessage(f"Error processing results: {str(e)}")
        
        finally:
            # Re-enable inputs
            self.game_name_input.setEnabled(True)
            self.tag_line_input.setEnabled(True)
            self.region_selector.setEnabled(True)
            
            # Clean up worker
            self.search_worker.deleteLater()
            self.search_worker = None

    def on_search_error(self, error_message):
        """Handle search error"""
        self.status_bar.showMessage(error_message)
        
        # Re-enable inputs
        self.game_name_input.setEnabled(True)
        self.tag_line_input.setEnabled(True)
        self.region_selector.setEnabled(True)
        
        # Clean up worker
        self.search_worker.deleteLater()
        self.search_worker = None

    def load_match_history(self):
        """Load match history for current player"""
        if not self.current_puuid:
            self.status_bar.showMessage("No player selected")
            return
        
        count = self.match_history.match_count.value()
        
        # Show progress bar and disable load button
        self.match_history.progress_bar.setValue(0)
        self.match_history.progress_bar.show()
        self.match_history.load_button.setEnabled(False)
        self.status_bar.showMessage(f"Loading {count} matches...")
        
        # Clear existing matches
        while self.match_history.matches_layout.count() > 1:
            item = self.match_history.matches_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Create and start worker thread
        self.match_worker = MatchHistoryWorker(self.riot_api, self.current_puuid, count)
        self.match_worker.finished.connect(self.on_matches_loaded)
        self.match_worker.error.connect(self.on_match_load_error)
        self.match_worker.progress.connect(self.update_match_progress)
        self.match_worker.start()

    def update_match_progress(self, value):
        """Update match loading progress"""
        self.match_history.progress_bar.setValue(value)

    def on_matches_loaded(self, match_details):
        """Handle match loading completion"""
        try:
            if match_details:
                for details in match_details:
                    self.add_match_widget(details)
                self.status_bar.showMessage("Match history loaded")
            else:
                self.status_bar.showMessage("No matches found")
        
        except Exception as e:
            self.status_bar.showMessage(f"Error processing matches: {str(e)}")
        
        finally:
            # Hide progress bar and re-enable load button
            self.match_history.progress_bar.hide()
            self.match_history.load_button.setEnabled(True)
            
            # Clean up worker
            self.match_worker.deleteLater()
            self.match_worker = None

    def on_match_load_error(self, error_message):
        """Handle match loading error"""
        self.status_bar.showMessage(error_message)
        
        # Hide progress bar and re-enable load button
        self.match_history.progress_bar.hide()
        self.match_history.load_button.setEnabled(True)
        
        # Clean up worker
        self.match_worker.deleteLater()
        self.match_worker = None

    def add_match_widget(self, match_details):
        """Add a match widget to the match history"""
        match_widget = MatchWidget()
        
        # Find player in match
        for participant in match_details.get('info', {}).get('participants', []):
            if participant.get('puuid') == self.current_puuid:
                # Load champion icon
                self.load_champion_icon(participant.get('championId'), match_widget.champion_icon)
                
                # Set match result and stats
                victory = participant.get('win', False)
                kills = participant.get('kills', 0)
                deaths = participant.get('deaths', 0)
                assists = participant.get('assists', 0)
                cs = participant.get('totalMinionsKilled', 0) + participant.get('neutralMinionsKilled', 0)
                duration = match_details.get('info', {}).get('gameDuration', 0)
                cs_per_min = (cs * 60 / duration) if duration > 0 else 0
                
                # Set victory property for color-coding
                match_widget.match_result.setProperty("victory", "true" if victory else "false")
                match_widget.match_result.setStyle(match_widget.match_result.style())
                
                match_widget.match_result.setText(
                    f"{'Victory' if victory else 'Defeat'} - {match_details.get('info', {}).get('gameMode', 'Unknown')}"
                )
                match_widget.match_stats.setText(
                    f"KDA: {kills}/{deaths}/{assists} - CS: {cs} ({cs_per_min:.1f}/min)"
                )
                
                # Load item icons
                for i in range(7):
                    item_id = participant.get(f'item{i}', 0)
                    self.load_item_icon(item_id, match_widget.item_icons[i])
                
                break
        
        self.match_history.matches_layout.insertWidget(
            self.match_history.matches_layout.count() - 1,
            match_widget
        )

    def set_application_icon(self):
        """Set the application icon"""
        try:
            # Get the absolute path to the icon file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            icon_path = os.path.abspath(os.path.join(current_dir, '..', 'assets', 'application_icon.ico'))
            
            if not os.path.exists(icon_path):
                self.logger.error(f"Icon file not found at: {icon_path}")
                return
                
            icon = QIcon(icon_path)
            if icon.isNull():
                self.logger.error("Failed to load icon - QIcon is null")
                return
                
            self.setWindowIcon(icon)
            self.logger.info(f"Successfully set application icon from: {icon_path}")
            
        except Exception as e:
            self.logger.error(f"Error setting application icon: {str(e)}") 