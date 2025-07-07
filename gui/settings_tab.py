from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt


class SettingsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the settings tab interface"""
        layout = QVBoxLayout(self)
        
        # API Settings
        self.setup_api_settings(layout)
        
        # Environment file section
        self.setup_env_info(layout)
        
        # Save settings button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def setup_api_settings(self, layout):
        """Set up the API settings section"""
        api_group = QGroupBox("RetroAchievements API Settings")
        api_layout = QGridLayout(api_group)
        
        # API Key input
        api_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.api_key_edit, 0, 1)
        
        # Show/Hide API key button
        show_key_btn = QPushButton("👁️ Show/Hide")
        show_key_btn.clicked.connect(self.toggle_api_key_visibility)
        api_layout.addWidget(show_key_btn, 0, 2)
        
        # API help text
        api_help = QLabel("Get your API key from: https://retroachievements.org/controlpanel.php")
        api_help.setStyleSheet("color: #7f8c8d; font-style: italic;")
        api_layout.addWidget(api_help, 1, 0, 1, 3)
        
        layout.addWidget(api_group)
    
    def setup_env_info(self, layout):
        """Set up the environment file information section"""
        env_group = QGroupBox("Environment File Example (.env)")
        env_layout = QVBoxLayout(env_group)
        
        env_info = QLabel(
            "The application looks for a .env file with:\n"
            "API_KEY=your_retroachievements_api_key\n"
            "DIRECTORY_PATH=your_download_directory\n"
            "DEFAULT_ROM_COUNT=10"
        )
        env_info.setStyleSheet("background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        env_layout.addWidget(env_info)
        
        layout.addWidget(env_group)
    
    def load_settings(self):
        """Load settings from parent configuration"""
        api_key = self.parent.get_api_key()
        self.api_key_edit.setText(api_key)
    
    def save_settings(self):
        """Save current settings"""
        api_key = self.api_key_edit.text().strip()
        
        if not api_key:
            QMessageBox.warning(self, "Invalid API Key", "Please enter a valid API key.")
            return
        
        # Save to parent configuration
        self.parent.set_api_key(api_key)
        
        # Save to configuration file
        self.parent.config.save_to_file()
        
        QMessageBox.information(self, "Settings Saved", "Settings have been saved successfully.")
    
    def toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.api_key_edit.echoMode() == QLineEdit.Password:
            self.api_key_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.api_key_edit.setEchoMode(QLineEdit.Password)