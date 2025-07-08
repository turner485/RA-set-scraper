from PyQt5.QtWidgets import (
    QGroupBox, QGridLayout, QLabel, QComboBox, QPushButton, QLineEdit,
    QHBoxLayout, QCheckBox, QProgressBar, QListWidget, QTextEdit,
    QVBoxLayout, QSplitter, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from .styles import get_primary_button_style, get_secondary_button_style


def create_search_section(self):
    group = QGroupBox("Search ROMs")
    layout = QGridLayout()

    layout.addWidget(QLabel("Console:"), 0, 0)
    self.console_combo = QComboBox()
    self.console_combo.addItem("Select Console...", None)
    layout.addWidget(self.console_combo, 0, 1)

    self.refresh_consoles_btn = QPushButton("🔄 Refresh")
    self.refresh_consoles_btn.setStyleSheet(get_secondary_button_style())
    layout.addWidget(self.refresh_consoles_btn, 0, 2)

    layout.addWidget(QLabel("Search (Regex):"), 1, 0)
    self.search_input = QLineEdit()
    self.search_input.setPlaceholderText("Enter game name or regex pattern...")
    layout.addWidget(self.search_input, 1, 1, 1, 2)

    search_options = QHBoxLayout()
    self.case_sensitive_cb = QCheckBox("Case Sensitive")
    self.whole_word_cb = QCheckBox("Whole Word")
    search_options.addWidget(self.case_sensitive_cb)
    search_options.addWidget(self.whole_word_cb)
    layout.addLayout(search_options, 2, 1, 1, 2)

    self.load_progress = QProgressBar()
    self.load_progress.setVisible(False)
    layout.addWidget(self.load_progress, 3, 0, 1, 3)

    self.status_label = QLabel("Ready")
    layout.addWidget(self.status_label, 4, 0, 1, 3)

    group.setLayout(layout)
    return group


def create_rom_list_section(self):
    splitter = QSplitter(Qt.Horizontal)

    # Left list
    left = QWidget()
    lbox = QVBoxLayout()
    self.rom_count_label = QLabel("No ROMs loaded")
    self.rom_count_label.setFont(QFont("Arial", 10))
    lbox.addWidget(self.rom_count_label)
    self.rom_list = QListWidget()
    lbox.addWidget(self.rom_list)
    left.setLayout(lbox)

    # Right side
    right = QWidget()
    rbox = QVBoxLayout()
    rbox.addWidget(QLabel("ROM Details:"))
    self.rom_details = QTextEdit()
    self.rom_details.setReadOnly(True)
    rbox.addWidget(self.rom_details)
    rbox.addWidget(QLabel("Available Sources:"))
    self.sources_list = QListWidget()
    rbox.addWidget(self.sources_list)
    right.setLayout(rbox)

    splitter.addWidget(left)
    splitter.addWidget(right)
    splitter.setSizes([400, 300])
    return splitter


def create_rom_text_section(self):
    group = QGroupBox("ROM Summary")
    layout = QVBoxLayout()
    self.selected_rom_label = QLabel("No ROM selected")
    layout.addWidget(self.selected_rom_label)
    group.setLayout(layout)
    return group


def create_download_section(self):
    group = QGroupBox("Download")
    layout = QHBoxLayout()
    self.download_btn = QPushButton("⬇️ Download Selected ROM")
    self.download_btn.setEnabled(False)
    self.download_btn.setStyleSheet(get_primary_button_style())
    layout.addWidget(self.download_btn)
    self.download_progress = QProgressBar()
    self.download_progress.setVisible(False)
    layout.addWidget(self.download_progress)
    group.setLayout(layout)
    return group
