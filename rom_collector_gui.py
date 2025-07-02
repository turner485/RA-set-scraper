import sys
import os
import json
import requests
import time
import re
import urllib.parse
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from dotenv import load_dotenv

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QLineEdit, QTextEdit, QSpinBox, QProgressBar,
    QGroupBox, QCheckBox, QComboBox, QFileDialog, QMessageBox, QTabWidget,
    QScrollArea, QFrame, QGridLayout
)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QTextCursor, QPixmap, QIcon

# Load environment variables
load_dotenv()

class ROMCollectorWorker(QThread):
    progress_update = pyqtSignal(str)
    progress_percent = pyqtSignal(int)
    download_progress = pyqtSignal(str, int, int)  # filename, current, total
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, num_roms, download_path, api_key, selected_consoles=None):
        super().__init__()
        self.num_roms = num_roms
        self.download_path = download_path
        self.api_key = api_key
        self.selected_consoles = selected_consoles or []
        self.rom_sources = {
            "PlayStation 2": ["https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation%202/"],
            "PlayStation": ["https://myrient.erista.me/files/Redump/Sony%20-%20PlayStation/"],
            "Saturn": [
                "https://myrient.erista.me/files/Internet%20Archive/chadmaster/chd_saturn/CHD-Saturn/USA/",
                "https://myrient.erista.me/files/Internet%20Archive/chadmaster/chd_saturn/CHD-Saturn/Japan/"
            ],
            "Game Boy Advance": [
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Multiboot)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(Video)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Advance%20(e-Reader)/"
            ],
            "Nintendo 64": [
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(BigEndian)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064%20(ByteSwapped)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%2064DD/"
            ],
            "Nintendo DS": [
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Decrypted)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Encrypted)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20DS%20(Download%20Play)/"
            ],
            "NES/Famicom": [
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headered)/",
                "https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Nintendo%20Entertainment%20System%20(Headerless)/"
            ],
            "Arcade": ["https://myrient.erista.me/files/Internet%20Archive/chadmaster/fbnarcade-fullnonmerged/arcade/"],
            "Game Boy Color": ["https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy%20Color/"],
            "Game Boy": ["https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Game%20Boy/"],
            "SNES/Super Famicom": ["https://myrient.erista.me/files/No-Intro/Nintendo%20-%20Super%20Nintendo%20Entertainment%20System/"],
            "Genesis/Mega Drive": ["https://myrient.erista.me/files/No-Intro/Sega%20-%20Mega%20Drive%20-%20Genesis/"],
            "Sega CD": ["https://myrient.erista.me/files/Redump/Sega%20-%20Mega%20CD%20&%20Sega%20CD/"],
            "32X": ["https://myrient.erista.me/files/No-Intro/Sega%20-%2032X/"],
            "Sega Game Gear": ["https://myrient.erista.me/files/No-Intro/Sega%20-%20Game%20Gear/"],
            "Sega Master System": ["https://myrient.erista.me/files/No-Intro/Sega%20-%20Master%20System%20-%20Mark%20III/"],
        }

    def run(self):
        try:
            # Step 1: Make API request
            self.progress_update.emit("🔄 Fetching recent claims from RetroAchievements...")
            self.progress_percent.emit(10)
            
            api_url = f"https://retroachievements.org/API/API_GetClaims.php?k=1&y={self.api_key}"
            response = requests.get(api_url)
            response.raise_for_status()
            game_data = response.json()
            
            # Step 2: Get top N recent games
            self.progress_update.emit(f"📋 Processing {self.num_roms} most recent claims...")
            self.progress_percent.emit(20)
            
            sorted_data = sorted(game_data, key=lambda entry: entry.get("DoneTime", ""), reverse=True)
            most_recent = sorted_data[:self.num_roms]
            
            # Step 3: Process game data
            self.progress_update.emit("🎮 Processing game information...")
            self.progress_percent.emit(30)
            
            game_dict = {'games': [], 'consoles': [], 'gameHashes': []}
            game_urls = []
            
            for game in most_recent:
                game_id = game['GameID']
                console_name = game['ConsoleName']
                
                # Filter by selected consoles if specified
                if self.selected_consoles and console_name not in self.selected_consoles:
                    continue
                    
                game_hash_url = f"https://retroachievements.org/API/API_GetGameHashes.php?i={game_id}&y={self.api_key}"
                game_dict['games'].append(game_id)
                game_dict['consoles'].append(console_name)
                game_dict['gameHashes'].append(game_hash_url)
                game_urls.append(game_hash_url)
                time.sleep(0.5)
            
            # Step 4: Get ROM titles
            self.progress_update.emit("🔍 Retrieving ROM titles...")
            self.progress_percent.emit(50)
            
            game_title_list = []
            for i, (url, console) in enumerate(zip(game_urls, game_dict['consoles'])):
                try:
                    r = requests.get(url)
                    r.raise_for_status()
                    data = r.json()
                    
                    results = data.get('Results', [])
                    if not results:
                        game_title_list.append('Unknown')
                        continue
                    
                    clean_results = [res for res in results if not res.get('PatchUrl')]
                    if len(clean_results) == 0:
                        selected_result = results[0]
                    else:
                        selected_result = clean_results[0]
                    
                    raw_name = selected_result.get('Name', 'Unknown Title')
                    
                    if console == "Arcade":
                        filename = raw_name.split()[0]
                        rom_base_name = re.sub(r'\.[a-z0-9]+$', '', filename, flags=re.IGNORECASE)
                    else:
                        rom_base_name = self.clean_title(raw_name)
                    
                    game_title_list.append(rom_base_name.strip())
                    self.progress_update.emit(f"📝 Found: {rom_base_name.strip()} ({console})")
                    time.sleep(0.5)
                    
                except Exception as e:
                    self.progress_update.emit(f"❌ Error processing game: {e}")
                    game_title_list.append('Error')
            
            # Step 5: Search and download ROMs
            self.progress_update.emit("⬇️ Starting ROM downloads...")
            self.progress_percent.emit(70)
            
            downloaded_count = 0
            for i, (title, console) in enumerate(zip(game_title_list, game_dict['consoles'])):
                if title in ['Unknown', 'Error']:
                    continue
                    
                success = self.find_and_download_rom(title, console)
                if success:
                    downloaded_count += 1
                
                progress = 70 + int((i / len(game_title_list)) * 25)
                self.progress_percent.emit(progress)
            
            self.progress_percent.emit(100)
            self.finished.emit(f"✅ Process completed! Downloaded {downloaded_count} ROMs")
            
        except Exception as e:
            self.error.emit(str(e))
    
    def clean_title(self, raw_title):
        title = urllib.parse.unquote(raw_title)
        title = re.sub(r'\.[a-z0-9]+$', '', title, flags=re.IGNORECASE)
        title = re.sub(r'\s+', ' ', title)
        title = re.sub(r'[-–—]\s*$', '', title).strip()
        return title
    
    def clean_filename(self, filename):
        filename = urllib.parse.unquote(filename)
        filename = re.sub(r'[ \-]+', '_', filename)
        return filename
    
    def find_and_download_rom(self, title, console):
        source_urls = self.rom_sources.get(console)
        if not source_urls:
            self.progress_update.emit(f"⚠️ No ROM source for console: {console}")
            return False
        
        if isinstance(source_urls, str):
            source_urls = [source_urls]
        
        self.progress_update.emit(f"🔍 Searching for: {title}")
        
        for url in source_urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                td_tags = soup.find_all('td', class_='link')
                
                for td in td_tags:
                    a_tag = td.find('a')
                    if a_tag:
                        link_title = a_tag.get('title') or a_tag.text
                        href = a_tag.get('href')
                        
                        if title.lower() in link_title.lower():
                            full_url = urljoin(url, href)
                            filename = os.path.basename(href)
                            filename = self.clean_filename(filename)
                            
                            return self.download_rom(full_url, filename, console)
                            
                time.sleep(0.5)
                
            except Exception as e:
                self.progress_update.emit(f"❌ Error accessing {url}: {e}")
        
        self.progress_update.emit(f"❌ No match found for {title}")
        return False
    
    def download_rom(self, full_url, filename, console):
        try:
            self.progress_update.emit(f"⬇️ Starting download: {filename}")
            response = requests.get(full_url, stream=True)
            response.raise_for_status()
            
            console_dir = os.path.join(self.download_path, "roms", console)
            os.makedirs(console_dir, exist_ok=True)
            
            filepath = os.path.join(console_dir, filename)
            
            if os.path.exists(filepath):
                self.progress_update.emit(f"⚠️ Skipped (already exists): {filename}")
                return True
            
            # Get total file size
            total_size = int(response.headers.get('Content-Length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Emit download progress
                        if total_size > 0:
                            percent = int((downloaded / total_size) * 100)
                            self.download_progress.emit(filename, downloaded, total_size)
            
            self.progress_update.emit(f"✅ Downloaded: {filename}")
            return True
            
        except Exception as e:
            self.progress_update.emit(f"❌ Failed to download {filename}: {e}")
            return False


class ROMCollectorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ROM Collector - RetroAchievements Edition")
        self.setGeometry(100, 100, 900, 700)
        
        # Initialize variables
        self.worker = None
        self.api_key = os.environ.get('API_KEY', '')
        self.download_path = os.environ.get('DIRECTORY_PATH', str(Path.home()))
        self.current_download_progress = {}  # Track individual download progress
        
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create tab widget
        tab_widget = QTabWidget()
        
        # Main tab
        main_tab = QWidget()
        tab_widget.addTab(main_tab, "ROM Collector")
        
        # Settings tab
        settings_tab = QWidget()
        tab_widget.addTab(settings_tab, "Settings")
        
        # Setup main tab
        self.setup_main_tab(main_tab)
        
        # Setup settings tab
        self.setup_settings_tab(settings_tab)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.addWidget(tab_widget)
    
    def setup_main_tab(self, parent):
        layout = QVBoxLayout(parent)
        
        # Title
        title = QLabel("RetroAchievements ROM Collector")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 10px 0;")
        layout.addWidget(title)
        
        # Input section
        input_group = QGroupBox("Collection Settings")
        input_layout = QGridLayout(input_group)
        
        # Number of ROMs
        input_layout.addWidget(QLabel("Number of recent ROMs:"), 0, 0)
        self.rom_count_spin = QSpinBox()
        self.rom_count_spin.setRange(1, 100)
        self.rom_count_spin.setValue(10)
        input_layout.addWidget(self.rom_count_spin, 0, 1)
        
        # Download path
        input_layout.addWidget(QLabel("Download Path:"), 1, 0)
        path_layout = QHBoxLayout()
        self.path_edit = QLineEdit(self.download_path)
        path_layout.addWidget(self.path_edit)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_download_path)
        path_layout.addWidget(browse_btn)
        
        input_layout.addLayout(path_layout, 1, 1)
        
        layout.addWidget(input_group)
        
        # Console filter section
        console_group = QGroupBox("Console Filter (Optional)")
        console_layout = QVBoxLayout(console_group)
        
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        
        self.console_checkboxes = {}
        consoles = [
            "PlayStation 2", "PlayStation", "Saturn", "Game Boy Advance",
            "Nintendo 64", "Nintendo DS", "NES/Famicom", "Arcade",
            "Game Boy Color", "Game Boy", "SNES/Super Famicom",
            "Genesis/Mega Drive", "Sega CD", "32X", "Sega Game Gear",
            "Sega Master System"
        ]
        
        for i, console in enumerate(consoles):
            checkbox = QCheckBox(console)
            self.console_checkboxes[console] = checkbox
            row = i // 3
            col = i % 3
            scroll_layout.addWidget(checkbox, row, col)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setMaximumHeight(150)
        console_layout.addWidget(scroll_area)
        
        # Select all/none buttons
        select_layout = QHBoxLayout()
        select_all_btn = QPushButton("Select All")
        select_all_btn.clicked.connect(self.select_all_consoles)
        select_none_btn = QPushButton("Select None")
        select_none_btn.clicked.connect(self.select_no_consoles)
        
        select_layout.addWidget(select_all_btn)
        select_layout.addWidget(select_none_btn)
        select_layout.addStretch()
        
        console_layout.addLayout(select_layout)
        layout.addWidget(console_group)
        
        # Progress section
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(200)
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("background-color: #f8f9fa; font-family: 'Courier New';")
        progress_layout.addWidget(self.status_text)
        
        layout.addWidget(progress_group)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Start Collection")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.start_btn.clicked.connect(self.start_collection)
        
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_collection)
        
        clear_btn = QPushButton("🗑️ Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def setup_settings_tab(self, parent):
        layout = QVBoxLayout(parent)
        
        # API Settings
        api_group = QGroupBox("RetroAchievements API Settings")
        api_layout = QGridLayout(api_group)
        
        api_layout.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key_edit = QLineEdit(self.api_key)
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        api_layout.addWidget(self.api_key_edit, 0, 1)
        
        show_key_btn = QPushButton("👁️ Show/Hide")
        show_key_btn.clicked.connect(self.toggle_api_key_visibility)
        api_layout.addWidget(show_key_btn, 0, 2)
        
        api_help = QLabel("Get your API key from: https://retroachievements.org/controlpanel.php")
        api_help.setStyleSheet("color: #7f8c8d; font-style: italic;")
        api_layout.addWidget(api_help, 1, 0, 1, 3)
        
        layout.addWidget(api_group)
        
        # Environment file section
        env_group = QGroupBox("Environment File")
        env_layout = QVBoxLayout(env_group)
        
        env_info = QLabel(
            "The application looks for a .env file with:\n"
            "API_KEY=your_retroachievements_api_key\n"
            "DIRECTORY_PATH=your_download_directory"
        )
        env_info.setStyleSheet("background-color: #f8f9fa; padding: 10px; border-radius: 5px;")
        env_layout.addWidget(env_info)
        
        layout.addWidget(env_group)
        
        # Save settings button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
    
    def load_settings(self):
        # Load from environment or .env file
        if os.path.exists('.env'):
            load_dotenv()
            self.api_key = os.environ.get('API_KEY', '')
            self.download_path = os.environ.get('DIRECTORY_PATH', str(Path.home()))
            self.path_edit.setText(self.download_path)
            if hasattr(self, 'api_key_edit'):
                self.api_key_edit.setText(self.api_key)
    
    def save_settings(self):
        self.api_key = self.api_key_edit.text()
        self.download_path = self.path_edit.text()
        
        # Save to .env file
        env_content = f"API_KEY={self.api_key}\nDIRECTORY_PATH={self.download_path}\n"
        with open('.env', 'w') as f:
            f.write(env_content)
        
        QMessageBox.information(self, "Settings Saved", "Settings have been saved to .env file")
    
    def toggle_api_key_visibility(self):
        if self.api_key_edit.echoMode() == QLineEdit.Password:
            self.api_key_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.api_key_edit.setEchoMode(QLineEdit.Password)
    
    def browse_download_path(self):
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.download_path)
        if path:
            self.download_path = path
            self.path_edit.setText(path)
    
    def select_all_consoles(self):
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(True)
    
    def select_no_consoles(self):
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(False)
    
    def get_selected_consoles(self):
        return [console for console, checkbox in self.console_checkboxes.items() if checkbox.isChecked()]
    
    def start_collection(self):
        if not self.api_key_edit.text().strip():
            QMessageBox.warning(self, "Missing API Key", "Please enter your RetroAchievements API key in the Settings tab.")
            return
        
        if not self.path_edit.text().strip():
            QMessageBox.warning(self, "Missing Download Path", "Please select a download directory.")
            return
        
        # Get settings
        num_roms = self.rom_count_spin.value()
        download_path = self.path_edit.text()
        api_key = self.api_key_edit.text()
        selected_consoles = self.get_selected_consoles()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        
        # Start worker thread
        self.worker = ROMCollectorWorker(num_roms, download_path, api_key, selected_consoles)
        self.worker.progress_update.connect(self.update_status)
        self.worker.progress_percent.connect(self.progress_bar.setValue)
        self.worker.download_progress.connect(self.update_download_progress)
        self.worker.finished.connect(self.on_collection_finished)
        self.worker.error.connect(self.on_collection_error)
        self.worker.start()
    
    def stop_collection(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()
            self.worker.wait()
        
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status("❌ Collection stopped by user")
    
    def update_download_progress(self, filename, current, total):
        """Update the terminal-style progress bar for individual downloads"""
        if total > 0:
            percent = (current / total) * 100
            filled = int(percent / 2)  # 50 characters wide
            bar = "█" * filled + "░" * (50 - filled)
            
            # Convert bytes to human readable
            current_mb = current / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            
            progress_line = f"📥 {filename[:30]:<30} |{bar}| {percent:5.1f}% ({current_mb:.1f}/{total_mb:.1f} MB)"
            
            # Store the current progress line for this file
            self.current_download_progress[filename] = progress_line
            
            # Find and update the existing progress line or add new one
            text = self.status_text.toPlainText()
            lines = text.split('\n')
            
            # Look for existing progress line for this file
            found_index = -1
            for i, line in enumerate(lines):
                if filename[:30] in line and '|' in line and '|' in line:
                    found_index = i
                    break
            
            if found_index >= 0:
                # Update existing line
                lines[found_index] = progress_line
            else:
                # Add new progress line
                lines.append(progress_line)
            
            # Update the text widget
            self.status_text.clear()
            self.status_text.append('\n'.join(lines))
            
            # Auto-scroll to bottom
            cursor = self.status_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.status_text.setTextCursor(cursor)
    
    def update_status(self, message):
        # Clean up progress lines when download is complete
        if message.startswith("✅ Downloaded:") or message.startswith("⚠️ Skipped"):
            filename = message.split(": ", 1)[1] if ": " in message else ""
            # Remove the progress line for completed downloads
            if filename in self.current_download_progress:
                del self.current_download_progress[filename]
        
        self.status_text.append(message)
        # Auto-scroll to bottom
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.status_text.setTextCursor(cursor)
    
    def on_collection_finished(self, message):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status(message)
        QMessageBox.information(self, "Collection Complete", message)
    
    def on_collection_error(self, error_msg):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        self.update_status(f"❌ Error: {error_msg}")
        QMessageBox.critical(self, "Error", f"An error occurred: {error_msg}")
    
    def clear_log(self):
        self.status_text.clear()
        self.current_download_progress.clear()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("ROM Collector")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyleSheet("""
        QMainWindow {
            background-color: #ecf0f1;
        }
        QGroupBox {
            font-weight: bold;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            margin: 5px 0;
            padding-top: 10px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px 0 5px;
        }
    """)
    
    window = ROMCollectorGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()