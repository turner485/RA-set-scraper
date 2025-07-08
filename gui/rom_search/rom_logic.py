import re
from PyQt5.QtCore import QTimer, Qt, QThread
from PyQt5.QtWidgets import QListWidgetItem, QMessageBox

from .rom_loader_thread import AsyncROMLoaderThread
from .download_thread import ROMDownloadThread
from core.rom_sources import get_supported_consoles


def setup_connections(self):
    self.console_combo.currentTextChanged.connect(self.on_console_changed)
    self.search_input.textChanged.connect(self.on_search_changed)
    self.case_sensitive_cb.toggled.connect(self.on_search_changed)
    self.whole_word_cb.toggled.connect(self.on_search_changed)
    self.rom_list.itemSelectionChanged.connect(self.on_rom_selected)
    self.download_btn.clicked.connect(self.download_selected_rom)
    self.refresh_consoles_btn.clicked.connect(lambda: populate_consoles(self))

    self.search_timer = QTimer()
    self.search_timer.setSingleShot(True)
    self.search_timer.timeout.connect(lambda: perform_search(self))


def populate_consoles(self):
    self.console_combo.clear()
    self.console_combo.addItem("Select Console...", None)

    consoles = get_supported_consoles()
    for console in sorted(consoles):
        self.console_combo.addItem(console, console)

    self.status_label.setText(f"Loaded {len(consoles)} consoles")


def on_console_changed(self):
    console = self.console_combo.currentData()
    if console is None:
        clear_rom_list(self)
        return

    self.load_progress.setVisible(True)
    self.load_progress.setRange(0, 0)
    self.status_label.setText(f"Loading ROMs for {console}...")

    if self.rom_loader_thread and self.rom_loader_thread.isRunning():
        self.rom_loader_thread.terminate()
        self.rom_loader_thread.wait()

    self.rom_loader_thread = AsyncROMLoaderThread(console)
    self.rom_loader_thread.roms_loaded.connect(self.on_roms_loaded)
    self.rom_loader_thread.progress_update.connect(self.on_loading_progress)
    self.rom_loader_thread.error_occurred.connect(self.on_loading_error)
    self.rom_loader_thread.start()


def on_roms_loaded(self, console_name, roms):
    self.rom_data[console_name] = roms
    self.filtered_roms = roms.copy()
    update_rom_list(self)
    self.load_progress.setVisible(False)
    self.status_label.setText(f"Loaded {len(roms)} ROMs for {console_name}")


def on_loading_progress(self, msg):
    self.status_label.setText(msg)


def on_loading_error(self, console, error_msg):
    self.load_progress.setVisible(False)
    self.status_label.setText(f"Error loading {console}: {error_msg}")
    QMessageBox.warning(self, "Loading Error", f"Failed to load ROMs for {console}:\n{error_msg}")


def on_search_changed(self):
    self.search_timer.stop()
    self.search_timer.start(300)


def perform_search(self):
    search_text = self.search_input.text().strip()
    console_name = self.console_combo.currentData()

    if console_name is None or console_name not in self.rom_data:
        return

    all_roms = self.rom_data[console_name]

    if not search_text:
        self.filtered_roms = all_roms.copy()
    else:
        try:
            pattern = search_text
            if self.whole_word_cb.isChecked():
                pattern = r'\b' + pattern + r'\b'
            flags = 0 if self.case_sensitive_cb.isChecked() else re.IGNORECASE
            regex = re.compile(pattern, flags)

            self.filtered_roms = [
                rom for rom in all_roms
                if regex.search(rom['name']) or regex.search(rom.get('extension', ''))
            ]
        except re.error:
            self.filtered_roms = all_roms.copy()

    update_rom_list(self)


def update_rom_list(self):
    self.rom_list.clear()
    for rom in self.filtered_roms:
        label = f"{rom['name']} ({rom['extension']})"
        item = QListWidgetItem(label)
        item.setData(Qt.UserRole, rom)
        self.rom_list.addItem(item)

    total = len(self.rom_data.get(self.console_combo.currentData(), []))
    shown = len(self.filtered_roms)
    self.rom_count_label.setText(f"Showing {shown} of {total} ROMs")


def clear_rom_list(self):
    self.rom_list.clear()
    self.filtered_roms = []
    self.rom_count_label.setText("No ROMs loaded")
    clear_rom_details(self)


def on_rom_selected(self):
    item = self.rom_list.currentItem()
    if not item:
        clear_rom_details(self)
        return

    show_rom_details(self, item.data(Qt.UserRole))


def show_rom_details(self, rom_data):
    self.selected_rom_label.setText(f"Selected: {rom_data['name']}")
    self.download_btn.setEnabled(True)
    details = f"""
Name: {rom_data['name']}
Extension: {rom_data['extension']}
Console: {self.console_combo.currentData()}
""".strip()
    self.rom_details.setText(details)

    self.sources_list.clear()
    for source in rom_data.get('sources', []):
        item = QListWidgetItem(f"Source: {source['base_url']}")
        item.setData(Qt.UserRole, source)
        self.sources_list.addItem(item)


def clear_rom_details(self):
    self.selected_rom_label.setText("No ROM selected")
    self.rom_details.clear()
    self.sources_list.clear()
    self.download_btn.setEnabled(False)


def download_selected_rom(self):
    item = self.rom_list.currentItem()
    if not item:
        return

    rom_data = item.data(Qt.UserRole)

    rom_data['console'] = self.console_combo.currentData()
    rom_data['download_path'] = self.parent.get_download_path()

    self.download_btn.setEnabled(False)
    self.download_progress.setVisible(True)
    self.download_progress.setRange(0, 100)

    if rom_data.get('sources'):
        source = rom_data['sources'][0]
        self.download_thread = ROMDownloadThread(rom_data, source)
        self.download_thread.progress.connect(self.download_progress.setValue)
        self.download_thread.finished.connect(self.on_download_finished)
        self.download_thread.start()
    else:
        self.on_download_finished(False, "No download sources available")


def on_download_finished(self, success, message):
    self.download_btn.setEnabled(True)
    self.download_progress.setVisible(False)
    if success:
        self.selected_rom_label.setText(f"Downloaded: {message}")
        QMessageBox.information(self, "Download Complete", f"Successfully downloaded: {message}")
    else:
        self.selected_rom_label.setText(f"Error: {message}")
        QMessageBox.warning(self, "Download Error", f"Download failed: {message}")
