from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QCheckBox, QComboBox, QFormLayout, QDialogButtonBox,
    QFrame
)
from PyQt6.QtCore import Qt
from api.constants import Constants

class SettingsDialog(QDialog):
    """Dialog for changing application settings"""
    
    def __init__(self, settings, regions=None, parent=None):
        """Initialize the settings dialog
        
        Args:
            settings: The Settings instance
            regions: Dictionary of available regions (deprecated, using Constants.REGION_MAPPINGS)
            parent: Parent widget
        """
        super().__init__(parent)
        self.settings = settings
        self.regions = Constants.REGION_MAPPINGS # Use Constants instead of parameter
        
        self.setWindowTitle("Settings")
        self.setMinimumWidth(400)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Default player section
        default_player_frame = QFrame()
        default_player_frame.setObjectName("settingsFrame")
        default_player_layout = QFormLayout(default_player_frame)
        
        # Default region
        self.region_selector = QComboBox()
        self.region_selector.addItems(self.regions.keys())
        current_region = self.settings.get("default_region")
        if current_region in self.regions:
            self.region_selector.setCurrentText(current_region)
        default_player_layout.addRow("Default Region:", self.region_selector)
        
        # Default player name
        self.player_name_input = QLineEdit()
        self.player_name_input.setText(self.settings.get("default_player_name", ""))
        self.player_name_input.setPlaceholderText("Enter default player name")
        default_player_layout.addRow("Default Player Name:", self.player_name_input)
        
        # Default tag line
        self.tag_line_input = QLineEdit()
        self.tag_line_input.setText(self.settings.get("default_tag_line", ""))
        self.tag_line_input.setPlaceholderText("Enter default tag (e.g. NA1)")
        default_player_layout.addRow("Default Tag Line:", self.tag_line_input)
        
        # Auto search on startup
        self.auto_search_checkbox = QCheckBox("Auto search on startup")
        self.auto_search_checkbox.setChecked(self.settings.get("auto_search_on_startup", False))
        default_player_layout.addRow("", self.auto_search_checkbox)
        
        layout.addWidget(default_player_frame)
        
        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel | 
            QDialogButtonBox.StandardButton.Reset
        )
        button_box.accepted.connect(self.save_settings)
        button_box.rejected.connect(self.reject)
        button_box.button(QDialogButtonBox.StandardButton.Reset).clicked.connect(self.reset_settings)
        layout.addWidget(button_box)
    
    def save_settings(self):
        """Save settings and close dialog"""
        self.settings.set("default_region", self.region_selector.currentText())
        self.settings.set("default_player_name", self.player_name_input.text().strip())
        self.settings.set("default_tag_line", self.tag_line_input.text().strip().lstrip('#'))
        self.settings.set("auto_search_on_startup", self.auto_search_checkbox.isChecked())
        self.accept()
    
    def reset_settings(self):
        """Reset settings to defaults"""
        self.settings.reset()
        
        # Update UI to match defaults
        self.region_selector.setCurrentText(self.settings.get("default_region"))
        self.player_name_input.setText(self.settings.get("default_player_name", ""))
        self.tag_line_input.setText(self.settings.get("default_tag_line", ""))
        self.auto_search_checkbox.setChecked(self.settings.get("auto_search_on_startup", False)) 