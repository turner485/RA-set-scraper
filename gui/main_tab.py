from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QSpinBox, QProgressBar, QGroupBox, QCheckBox, QTextEdit,
    QScrollArea, QGridLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCursor

from core.rom_sources import ROM_SOURCES
from gui.styles import get_button_style, get_stop_button_style, get_clear_button_style


class MainTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.console_checkboxes = {}
        self.current_download_progress = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Set up the main tab interface"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("RetroAchievements Most Recent Sets")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 10px 0;")
        layout.addWidget(title)
        
        # Input section
        self.setup_input_section(layout)
        
        # Console filter section
        self.setup_console_filter_section(layout)
        
        # Progress section
        self.setup_progress_section(layout)
        
        # Control buttons
        self.setup_control_buttons(layout)
    
    def setup_input_section(self, layout):
        """Set up the input controls section"""
        input_group = QGroupBox("Search Settings")
        input_layout = QGridLayout(input_group)
        
        # Number of ROMs
        input_layout.addWidget(QLabel("Number of recent Games:"), 0, 0)
        self.rom_count_spin = QSpinBox()
        self.rom_count_spin.setRange(1, 100)
        self.rom_count_spin.setValue(10)
        input_layout.addWidget(self.rom_count_spin, 0, 1)
        
        # Download path
        input_layout.addWidget(QLabel("Download Path:"), 1, 0)
        path_layout = QHBoxLayout()
        self.path_display = QLabel()
        self.path_display.setStyleSheet("border: 1px solid #bdc3c7; padding: 5px; background: white;")
        path_layout.addWidget(self.path_display)
        
        browse_btn = QPushButton("Browse...")
        browse_btn.clicked.connect(self.browse_download_path)
        path_layout.addWidget(browse_btn)
        
        input_layout.addLayout(path_layout, 1, 1)
        
        layout.addWidget(input_group)
    
    def setup_console_filter_section(self, layout):
        """Set up the console filter section"""
        console_group = QGroupBox("Console Filter (Optional)")
        console_layout = QVBoxLayout(console_group)
        
        # Scrollable area for console checkboxes
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)
        
        # Create checkboxes for each console
        consoles = list(ROM_SOURCES.keys())
        for i, console in enumerate(consoles):
            checkbox = QCheckBox(console)
            self.console_checkboxes[console] = checkbox
            row = i // 6
            col = i % 6
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
    
    def setup_progress_section(self, layout):
        """Set up the progress tracking section"""
        progress_group = QGroupBox("Progress Console")
        progress_layout = QVBoxLayout(progress_group)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        # Status text area
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(200)
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("background-color: #f8f9fa; font-family: 'Courier New';")
        progress_layout.addWidget(self.status_text)
        
        layout.addWidget(progress_group)
    
    def setup_control_buttons(self, layout):
        """Set up the control buttons"""
        button_layout = QHBoxLayout()
        
        # Start button
        self.start_btn = QPushButton("Start Search 🚀")
        self.start_btn.setStyleSheet(get_button_style())
        self.start_btn.clicked.connect(self.start_collection)
        
        # Stop button
        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_collection)
        self.stop_btn.setStyleSheet(get_stop_button_style())
        # Clear log button
        clear_btn = QPushButton("🗑️ Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        clear_btn.setStyleSheet(get_clear_button_style())
        button_layout.addWidget(self.start_btn)
        button_layout.addWidget(self.stop_btn)
        button_layout.addWidget(clear_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """Load settings from parent configuration"""
        self.path_display.setText(self.parent.get_download_path())
    
    def save_settings(self):
        """Save current settings to parent configuration"""
        # Settings are handled by the parent window
        pass
    
    def browse_download_path(self):
        """Browse for download directory"""
        current_path = self.parent.get_download_path()
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory", current_path)
        if path:
            self.parent.set_download_path(path)
            self.path_display.setText(path)
    
    def select_all_consoles(self):
        """Select all console checkboxes"""
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(True)
    
    def select_no_consoles(self):
        """Deselect all console checkboxes"""
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(False)
    
    def get_selected_consoles(self):
        """Get list of selected console names"""
        return [console for console, checkbox in self.console_checkboxes.items() 
                if checkbox.isChecked()]
    
    def start_collection(self):
        """Start the ROM collection process"""
        num_roms = self.rom_count_spin.value()
        selected_consoles = self.get_selected_consoles()
        
        if self.parent.start_collection(num_roms, selected_consoles):
            self.on_collection_started()
    
    def stop_collection(self):
        """Stop the ROM collection process"""
        self.parent.stop_collection()
    
    def on_collection_started(self):
        """Handle collection start UI updates"""
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        self.current_download_progress.clear()
    
    def on_collection_finished(self):
        """Handle collection completion UI updates"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def on_collection_stopped(self):
        """Handle collection stop UI updates"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def on_collection_error(self):
        """Handle collection error UI updates"""
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
    
    def update_progress_bar(self, value):
        """Update the progress bar"""
        self.progress_bar.setValue(value)
    
    def update_status(self, message):
        """Update the status text area"""
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
                if filename[:30] in line and '|' in line:
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
    
    def clear_log(self):
        """Clear the status log"""
        self.status_text.clear()
        self.current_download_progress.clear()