import asyncio
import re
import aiohttp
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox, 
                             QLineEdit, QPushButton, QListWidget, QListWidgetItem,
                             QLabel, QProgressBar, QSplitter, QTextEdit, QCheckBox,
                             QGroupBox, QGridLayout, QMessageBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont
import json
import os
from urllib.parse import urljoin, unquote
from bs4 import BeautifulSoup
import requests
from core.rom_sources import ROM_SOURCES, get_supported_consoles, get_console_sources

class ROMSearchTab(QWidget):
    """Tab for searching and downloading individual ROMs"""
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rom_data = {}  # Store ROM data by console
        self.filtered_roms = []  # Currently displayed ROMs
        self.search_thread = None
        self.download_thread = None
        self.rom_loader_thread = None
        
        self.setup_ui()
        self.setup_connections()
        self.populate_consoles()
        
    def setup_ui(self):
        """Setup the user interface"""
        layout = QVBoxLayout()
        
        # Top section - Console selection and search
        top_section = self.create_search_section()
        layout.addWidget(top_section)
        
        # Middle section - ROM list and details
        middle_section = self.create_rom_list_section()
        layout.addWidget(middle_section)
        
        # Bottom section - Download controls
        bottom_section = self.create_download_section()
        layout.addWidget(bottom_section)
        
        self.setLayout(layout)
        
    def create_search_section(self):
        """Create the search controls section"""
        group = QGroupBox("Search ROMs")
        layout = QGridLayout()
        
        # Console dropdown
        layout.addWidget(QLabel("Console:"), 0, 0)
        self.console_combo = QComboBox()
        self.console_combo.addItem("Select Console...", None)
        self.console_combo.setMinimumWidth(200)
        layout.addWidget(self.console_combo, 0, 1)
        
        # Refresh button for console list
        self.refresh_consoles_btn = QPushButton("🔄 Refresh")
        self.refresh_consoles_btn.setStyleSheet(self.get_secondary_button_style())
        layout.addWidget(self.refresh_consoles_btn, 0, 2)
        
        # Search box
        layout.addWidget(QLabel("Search (Regex):"), 1, 0)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter game name or regex pattern...")
        layout.addWidget(self.search_input, 1, 1, 1, 2)
        
        # Search options
        search_options = QHBoxLayout()
        self.case_sensitive_cb = QCheckBox("Case Sensitive")
        self.whole_word_cb = QCheckBox("Whole Word")
        search_options.addWidget(self.case_sensitive_cb)
        search_options.addWidget(self.whole_word_cb)
        search_options.addStretch()
        
        layout.addLayout(search_options, 2, 1, 1, 2)
        
        # Load progress
        self.load_progress = QProgressBar()
        self.load_progress.setVisible(False)
        layout.addWidget(self.load_progress, 3, 0, 1, 3)
        
        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label, 4, 0, 1, 3)
        
        group.setLayout(layout)
        return group
        
    def create_rom_list_section(self):
        """Create the ROM list and details section"""
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - ROM list
        left_widget = QWidget()
        left_layout = QVBoxLayout()
        
        # ROM count label
        self.rom_count_label = QLabel("No ROMs loaded")
        self.rom_count_label.setFont(QFont("Arial", 10))
        left_layout.addWidget(self.rom_count_label)
        
        # ROM list
        self.rom_list = QListWidget()
        self.rom_list.setMinimumHeight(300)
        left_layout.addWidget(self.rom_list)
        
        left_widget.setLayout(left_layout)
        splitter.addWidget(left_widget)
        
        # Right side - ROM details
        right_widget = QWidget()
        right_layout = QVBoxLayout()
        
        right_layout.addWidget(QLabel("ROM Details:"))
        self.rom_details = QTextEdit()
        self.rom_details.setReadOnly(True)
        self.rom_details.setMaximumHeight(200)
        right_layout.addWidget(self.rom_details)
        
        right_layout.addWidget(QLabel("Available Sources:"))
        self.sources_list = QListWidget()
        self.sources_list.setMaximumHeight(150)
        right_layout.addWidget(self.sources_list)
        
        right_widget.setLayout(right_layout)
        splitter.addWidget(right_widget)
        
        # Set splitter proportions
        splitter.setSizes([400, 300])
        
        return splitter
        
    def create_download_section(self):
        """Create the download controls section"""
        group = QGroupBox("Download")
        layout = QHBoxLayout()
        
        # Selected ROM info
        self.selected_rom_label = QLabel("No ROM selected")
        layout.addWidget(self.selected_rom_label)
        
        layout.addStretch()
        
        # Download button
        self.download_btn = QPushButton("⬇️ Download Selected ROM")
        self.download_btn.setEnabled(False)
        self.download_btn.setStyleSheet(self.get_primary_button_style())
        layout.addWidget(self.download_btn)
        
        # Download progress
        self.download_progress = QProgressBar()
        self.download_progress.setVisible(False)
        layout.addWidget(self.download_progress)
        
        group.setLayout(layout)
        return group
        
    def setup_connections(self):
        """Setup signal connections"""
        self.console_combo.currentTextChanged.connect(self.on_console_changed)
        self.search_input.textChanged.connect(self.on_search_changed)
        self.case_sensitive_cb.toggled.connect(self.on_search_changed)
        self.whole_word_cb.toggled.connect(self.on_search_changed)
        self.rom_list.itemSelectionChanged.connect(self.on_rom_selected)
        self.download_btn.clicked.connect(self.download_selected_rom)
        self.refresh_consoles_btn.clicked.connect(self.populate_consoles)
        
        # Setup search delay timer
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        
    def populate_consoles(self):
        """Populate the console dropdown with supported consoles"""
        self.console_combo.clear()
        self.console_combo.addItem("Select Console...", None)
        
        supported_consoles = get_supported_consoles()
        for console in sorted(supported_consoles):
            self.console_combo.addItem(console, console)
        
        self.status_label.setText(f"Loaded {len(supported_consoles)} consoles")
        
    def on_console_changed(self):
        """Handle console selection change"""
        console_name = self.console_combo.currentData()
        if console_name is None:
            self.clear_rom_list()
            return
            
        # Load ROMs for selected console
        self.load_progress.setVisible(True)
        self.load_progress.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText(f"Loading ROMs for {console_name}...")
        
        # Cancel any existing ROM loading thread
        if self.rom_loader_thread and self.rom_loader_thread.isRunning():
            self.rom_loader_thread.terminate()
            self.rom_loader_thread.wait()
        
        self.rom_loader_thread = AsyncROMLoaderThread(console_name)
        self.rom_loader_thread.roms_loaded.connect(self.on_roms_loaded)
        self.rom_loader_thread.progress_update.connect(self.on_loading_progress)
        self.rom_loader_thread.error_occurred.connect(self.on_loading_error)
        self.rom_loader_thread.start()
        
    def on_roms_loaded(self, console_name, roms):
        """Handle loaded ROM list"""
        self.rom_data[console_name] = roms
        self.filtered_roms = roms.copy()
        self.update_rom_list()
        self.load_progress.setVisible(False)
        self.status_label.setText(f"Loaded {len(roms)} ROMs for {console_name}")
        
    def on_loading_progress(self, message):
        """Handle loading progress updates"""
        self.status_label.setText(message)
        
    def on_loading_error(self, console_name, error_message):
        """Handle loading errors"""
        self.load_progress.setVisible(False)
        self.status_label.setText(f"Error loading {console_name}: {error_message}")
        QMessageBox.warning(self, "Loading Error", f"Failed to load ROMs for {console_name}:\n{error_message}")
        
    def on_search_changed(self):
        """Handle search text change with delay"""
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms delay
        
    def perform_search(self):
        """Perform the actual search"""
        search_text = self.search_input.text().strip()
        console_name = self.console_combo.currentData()
        
        if console_name is None or console_name not in self.rom_data:
            return
            
        all_roms = self.rom_data[console_name]
        
        if not search_text:
            self.filtered_roms = all_roms.copy()
        else:
            try:
                # Build regex pattern
                pattern = search_text
                if self.whole_word_cb.isChecked():
                    pattern = r'\b' + pattern + r'\b'
                    
                flags = 0 if self.case_sensitive_cb.isChecked() else re.IGNORECASE
                regex = re.compile(pattern, flags)
                
                # Filter ROMs
                self.filtered_roms = [
                    rom for rom in all_roms 
                    if regex.search(rom['name']) or regex.search(rom.get('extension', ''))
                ]
                
            except re.error:
                # Invalid regex, show all ROMs
                self.filtered_roms = all_roms.copy()
                
        self.update_rom_list()
        
    def update_rom_list(self):
        """Update the ROM list display"""
        self.rom_list.clear()
        
        for rom in self.filtered_roms:
            display_name = f"{rom['name']} ({rom['extension']})"
            item = QListWidgetItem(display_name)
            item.setData(Qt.UserRole, rom)
            self.rom_list.addItem(item)
            
        # Update count
        console_name = self.console_combo.currentData()
        total_count = len(self.rom_data.get(console_name, []))
        filtered_count = len(self.filtered_roms)
        self.rom_count_label.setText(f"Showing {filtered_count} of {total_count} ROMs")
        
    def clear_rom_list(self):
        """Clear the ROM list"""
        self.rom_list.clear()
        self.filtered_roms = []
        self.rom_count_label.setText("No ROMs loaded")
        self.clear_rom_details()
        
    def on_rom_selected(self):
        """Handle ROM selection"""
        current_item = self.rom_list.currentItem()
        if current_item is None:
            self.clear_rom_details()
            return
            
        rom_data = current_item.data(Qt.UserRole)
        self.show_rom_details(rom_data)
        
    def show_rom_details(self, rom_data):
        """Show details for selected ROM"""
        details = f"""
Name: {rom_data['name']}
Extension: {rom_data['extension']}
Console: {self.console_combo.currentData()}
        """.strip()
        
        self.rom_details.setText(details)
        self.selected_rom_label.setText(f"Selected: {rom_data['name']}")
        self.download_btn.setEnabled(True)
        
        # Show available sources
        self.sources_list.clear()
        for source in rom_data.get('sources', []):
            item = QListWidgetItem(f"Source: {source['base_url']}")
            item.setData(Qt.UserRole, source)
            self.sources_list.addItem(item)
        
    def clear_rom_details(self):
        """Clear ROM details"""
        self.rom_details.clear()
        self.sources_list.clear()
        self.selected_rom_label.setText("No ROM selected")
        self.download_btn.setEnabled(False)
        
    def download_selected_rom(self):
        """Download the selected ROM"""
        current_item = self.rom_list.currentItem()
        if current_item is None:
            return
            
        rom_data = current_item.data(Qt.UserRole)
        
        # Start download
        self.download_btn.setEnabled(False)
        self.download_progress.setVisible(True)
        self.download_progress.setRange(0, 100)
        
        # Use the first available source for download
        if rom_data.get('sources'):
            source = rom_data['sources'][0]
            self.download_thread = ROMDownloadThread(rom_data, source)
            self.download_thread.progress.connect(self.download_progress.setValue)
            self.download_thread.finished.connect(self.on_download_finished)
            self.download_thread.start()
        else:
            self.on_download_finished(False, "No download sources available")
        
    def on_download_finished(self, success, message):
        """Handle download completion"""
        self.download_btn.setEnabled(True)
        self.download_progress.setVisible(False)
        
        if success:
            self.selected_rom_label.setText(f"Downloaded: {message}")
            QMessageBox.information(self, "Download Complete", f"Successfully downloaded: {message}")
        else:
            self.selected_rom_label.setText(f"Error: {message}")
            QMessageBox.warning(self, "Download Error", f"Download failed: {message}")
            
    def get_primary_button_style(self):
        """Get primary button style"""
        return """
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
        """
        
    def get_secondary_button_style(self):
        """Get secondary button style"""
        return """
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: bold;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """


class AsyncROMLoaderThread(QThread):
    """Thread for asynchronously loading ROM lists from multiple sources"""
    roms_loaded = pyqtSignal(str, list)
    progress_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str, str)
    
    def __init__(self, console_name):
        super().__init__()
        self.console_name = console_name
        
    def run(self):
        """Load ROMs asynchronously from all sources for the console"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            roms = loop.run_until_complete(self.fetch_roms_async(self.console_name))
            self.roms_loaded.emit(self.console_name, roms)
            
        except Exception as e:
            self.error_occurred.emit(self.console_name, str(e))
        finally:
            loop.close()
            
    async def fetch_roms_async(self, console_name):
        """Fetch ROMs from all sources for a console asynchronously"""
        sources = get_console_sources(console_name)
        if not sources:
            return []
            
        all_roms = []
        
        # Create HTTP session
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = []
            
            for source_url in sources:
                task = self.fetch_rom_list_from_source(session, source_url, console_name)
                tasks.append(task)
                
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.progress_update.emit(f"Failed to load from source {i+1}: {str(result)}")
                    continue
                    
                source_roms = result
                for rom in source_roms:
                    # Add source information to ROM data
                    rom['sources'] = rom.get('sources', [])
                    rom['sources'].append({
                        'base_url': sources[i],
                        'full_url': rom['url']
                    })
                    
                all_roms.extend(source_roms)
                self.progress_update.emit(f"Loaded {len(source_roms)} ROMs from source {i+1}")
                
        # Remove duplicates based on ROM name
        unique_roms = {}
        for rom in all_roms:
            name = rom['name']
            if name not in unique_roms:
                unique_roms[name] = rom
            else:
                # Merge sources if ROM already exists
                existing_sources = unique_roms[name].get('sources', [])
                new_sources = rom.get('sources', [])
                unique_roms[name]['sources'] = existing_sources + new_sources
                
        return list(unique_roms.values())
        
    async def fetch_rom_list_from_source(self, session, source_url, console_name):
        """Fetch ROM list from a single source"""
        try:
            async with session.get(source_url) as response:
                if response.status != 200:
                    raise Exception(f"HTTP {response.status}")
                    
                content = await response.text()
                return self.parse_rom_list(content, source_url)
                
        except Exception as e:
            raise Exception(f"Failed to fetch from {source_url}: {str(e)}")
            
    def parse_rom_list(self, html_content, base_url):
        """Parse ROM list from HTML directory listing"""
        soup = BeautifulSoup(html_content, 'html.parser')
        roms = []
        
        # Find all links to ROM files
        for link in soup.find_all('a', href=True):
            href = link['href']
            
            # Skip parent directory links
            if href in ['../', '../']:
                continue
                
            # Skip directories (usually end with /)
            if href.endswith('/'):
                continue
                
            # Extract file info
            filename = unquote(href)
            if not filename:
                continue
                
            # Get file extension
            name, extension = os.path.splitext(filename)
            if not extension:
                continue
                
            rom_data = {
                'name': name,
                'extension': extension,
                'url': urljoin(base_url, href),
                'sources': []  # Will be populated by calling function
            }
            
            roms.append(rom_data)
            
        return roms


class ROMDownloadThread(QThread):
    """Thread for downloading ROM files"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, rom_data, source):
        super().__init__()
        self.rom_data = rom_data
        self.source = source
        
    def run(self):
        """Download ROM file"""
        try:
            success = self.download_rom(self.rom_data, self.source)
            if success:
                self.finished.emit(True, self.rom_data['name'])
            else:
                self.finished.emit(False, "Download failed")
        except Exception as e:
            self.finished.emit(False, str(e))
            
    def download_rom(self, rom_data, source):
        """Download the ROM file with progress tracking"""
        try:
            url = source['full_url']
            filename = f"{rom_data['name']}{rom_data['extension']}"
            
            # Create downloads directory if it doesn't exist
            downloads_dir = "downloads"
            if not os.path.exists(downloads_dir):
                os.makedirs(downloads_dir)
                
            filepath = os.path.join(downloads_dir, filename)
            
            # Download with progress tracking
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            self.progress.emit(progress)
                            
            return True
            
        except Exception as e:
            raise Exception(f"Download failed: {str(e)}")