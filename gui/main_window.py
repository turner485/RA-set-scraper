import os
from pathlib import Path
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QTabWidget, QMessageBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer

from gui.main_tab import MainTab
from gui.settings_tab import SettingsTab
from gui.rom_search.rom_search_tab import ROMSearchTab
from core.config import Config


class ROMCollectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RetroAchievements Game Collector v1.1.8-Beta")
        self.setGeometry(100, 100, 900, 700)

        # Initialize configuration
        self.config = Config()

        # Initialize variables
        self.worker = None
        self.current_download_progress = {}

        self.setup_ui()
        self.load_settings()

    def setup_ui(self):
        """Set up the main user interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create tab widget
        tab_widget = QTabWidget()

        # Create tabs
        self.main_tab = MainTab(self)
        self.rom_search_tab = ROMSearchTab(self)
        self.settings_tab = SettingsTab(self)

        # Add tabs
        tab_widget.addTab(self.main_tab, "Most Recent Sets")
        tab_widget.addTab(self.rom_search_tab, "ROM Search")
        tab_widget.addTab(self.settings_tab, "Settings")

        # Layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(tab_widget)

    def load_settings(self):
        """Load settings from configuration"""
        self.settings_tab.load_settings()
        self.main_tab.load_settings()

    def save_settings(self):
        """Save current settings to configuration"""
        self.settings_tab.save_settings()
        self.main_tab.save_settings()

    # 🔧 API Key access
    def set_api_key(self, api_key):
        self.config.api_key = api_key

    def get_api_key(self):
        return self.config.get_api_key()

    # 🔧 Download path access
    def set_download_path(self, path):
        self.config.download_path = path

    def get_download_path(self):
        return self.config.get_download_path()

    def start_collection(self, num_roms, selected_consoles):
        """Start the ROM collection process"""
        if not self.get_api_key().strip():
            QMessageBox.warning(self, "Missing API Key", "Please enter your RetroAchievements API key in the Settings tab.")
            return False

        if not self.get_download_path().strip():
            QMessageBox.warning(self, "Missing Download Path", "Please select a download directory in the Settings tab.")
            return False

        from workers.collector_worker import ROMCollectorWorker

        self.worker = ROMCollectorWorker(
            num_roms,
            self.get_download_path(),
            self.get_api_key(),
            selected_consoles
        )

        self.worker.progress_update.connect(self.main_tab.update_status)
        self.worker.progress_percent.connect(self.main_tab.update_progress_bar)
        self.worker.download_progress.connect(self.main_tab.update_download_progress)
        self.worker.finished.connect(self.on_collection_finished)
        self.worker.error.connect(self.on_collection_error)

        self.worker.start()
        return True

    def stop_collection(self):
        """Stop the ROM collection process"""
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()

        self.main_tab.on_collection_stopped()
        self.main_tab.update_status("❌ Collection stopped by user")

    def on_collection_finished(self, message):
        """Handle collection completion"""
        self.main_tab.on_collection_finished()
        self.main_tab.update_status(message)
        QMessageBox.information(self, "Collection Complete", message)

    def on_collection_error(self, error_msg):
        """Handle collection errors"""
        self.main_tab.on_collection_error()
        self.main_tab.update_status(f"❌ Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")

    def clear_download_progress(self):
        """Clear download progress tracking"""
        self.current_download_progress.clear()
