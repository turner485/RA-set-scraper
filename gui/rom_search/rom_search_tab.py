from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer

from .ui_sections import (
    create_search_section,
    create_rom_list_section,
    create_rom_text_section,
    create_download_section
)
from .rom_logic import (
    setup_connections,
    populate_consoles,
    on_console_changed,
    on_roms_loaded,
    on_loading_progress,
    on_loading_error,
    on_search_changed,
    perform_search,
    update_rom_list,
    clear_rom_list,
    on_rom_selected,
    show_rom_details,
    clear_rom_details,
    download_selected_rom,
    on_download_finished
)


class ROMSearchTab(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.rom_data = {}
        self.filtered_roms = []
        self.search_thread = None
        self.download_thread = None
        self.rom_loader_thread = None

        self.setup_ui()
        setup_connections(self)
        populate_consoles(self)

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(create_search_section(self))
        layout.addWidget(create_rom_list_section(self))
        layout.addWidget(create_rom_text_section(self))
        layout.addWidget(create_download_section(self))
        self.setLayout(layout)

    # Hook external logic methods back in
    def on_console_changed(self): on_console_changed(self)
    def on_roms_loaded(self, name, roms): on_roms_loaded(self, name, roms)
    def on_loading_progress(self, msg): on_loading_progress(self, msg)
    def on_loading_error(self, name, err): on_loading_error(self, name, err)
    def on_search_changed(self): on_search_changed(self)
    def perform_search(self): perform_search(self)
    def update_rom_list(self): update_rom_list(self)
    def clear_rom_list(self): clear_rom_list(self)
    def on_rom_selected(self): on_rom_selected(self)
    def show_rom_details(self, rom): show_rom_details(self, rom)
    def clear_rom_details(self): clear_rom_details(self)
    def download_selected_rom(self): download_selected_rom(self)
    def on_download_finished(self, success, msg): on_download_finished(self, success, msg)
