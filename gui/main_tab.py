from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QSpinBox, QProgressBar, QGroupBox, QCheckBox, QTextEdit,
    QScrollArea, QGridLayout
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
        label = QLabel("Number of recent Games:")
        input_layout.addWidget(label, 0, 0)
        
        self.rom_count_spin = QSpinBox()
        self.rom_count_spin.setRange(1, 100)
        self.rom_count_spin.setValue(10)
        self.rom_count_spin.setFixedWidth(60)
        input_layout.addWidget(self.rom_count_spin, 0, 1)

        layout.addWidget(input_group)

    def setup_console_filter_section(self, layout):
        """Set up the console filter section"""
        console_group = QGroupBox("Console Filter (Optional)")
        console_layout = QVBoxLayout(console_group)

        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QGridLayout(scroll_widget)

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

        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)

        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(200)
        self.status_text.setReadOnly(True)
        self.status_text.setStyleSheet("background-color: #f8f9fa; font-family: 'Courier New';")
        progress_layout.addWidget(self.status_text)

        layout.addWidget(progress_group)

    def setup_control_buttons(self, layout):
        """Set up the control buttons"""
        button_layout = QHBoxLayout()

        self.start_btn = QPushButton("Start Search 🚀")
        self.start_btn.setStyleSheet(get_button_style())
        self.start_btn.clicked.connect(self.start_collection)

        self.stop_btn = QPushButton("⏹️ Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_collection)
        self.stop_btn.setStyleSheet(get_stop_button_style())

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
        # No longer editable here — handled in SettingsTab
        pass

    def save_settings(self):
        """Save current settings to parent configuration"""
        # No longer editable here — handled in SettingsTab
        pass

    def select_all_consoles(self):
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(True)

    def select_no_consoles(self):
        for checkbox in self.console_checkboxes.values():
            checkbox.setChecked(False)

    def get_selected_consoles(self):
        return [console for console, checkbox in self.console_checkboxes.items() if checkbox.isChecked()]

    def start_collection(self):
        num_roms = self.rom_count_spin.value()
        selected_consoles = self.get_selected_consoles()

        if self.parent.start_collection(num_roms, selected_consoles):
            self.on_collection_started()

    def stop_collection(self):
        self.parent.stop_collection()

    def on_collection_started(self):
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        self.status_text.clear()
        self.current_download_progress.clear()

    def on_collection_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)

    def on_collection_stopped(self):
        self.on_collection_finished()

    def on_collection_error(self):
        self.on_collection_finished()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, message):
        if message.startswith("✅ Downloaded:") or message.startswith("⚠️ Skipped"):
            filename = message.split(": ", 1)[1] if ": " in message else ""
            if filename in self.current_download_progress:
                del self.current_download_progress[filename]

        self.status_text.append(message)
        cursor = self.status_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.status_text.setTextCursor(cursor)

    def update_download_progress(self, filename, current, total):
        if total > 0:
            percent = (current / total) * 100
            filled = int(percent / 2)
            bar = "█" * filled + "░" * (50 - filled)
            current_mb = current / (1024 * 1024)
            total_mb = total / (1024 * 1024)
            progress_line = f"📥 {filename[:30]:<30} |{bar}| {percent:5.1f}% ({current_mb:.1f}/{total_mb:.1f} MB)"
            self.current_download_progress[filename] = progress_line

            text = self.status_text.toPlainText()
            lines = text.split('\n')
            found_index = -1
            for i, line in enumerate(lines):
                if filename[:30] in line and '|' in line:
                    found_index = i
                    break

            if found_index >= 0:
                lines[found_index] = progress_line
            else:
                lines.append(progress_line)

            self.status_text.clear()
            self.status_text.append('\n'.join(lines))

            cursor = self.status_text.textCursor()
            cursor.movePosition(QTextCursor.End)
            self.status_text.setTextCursor(cursor)

    def clear_log(self):
        self.status_text.clear()
        self.current_download_progress.clear()
