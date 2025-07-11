#!/usr/bin/env python3
"""
RetroAchievements ROM Collector
Main entry point for the application
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import ROMCollectorGUI
from gui.styles import get_main_window_style

def get_icon_path():
    """Get the path to the application icon (PyInstaller compatible)"""
    def resource_path(relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    # Try different possible locations for the icon
    possible_paths = [
        'resources/ra-logo.ico',
        'resources/ra-logo.png',
        'ra-logo.ico',
        'ra-logo.png'
    ]
    
    for path in possible_paths:
        full_path = resource_path(path)
        if os.path.exists(full_path):
            return full_path
    
    # Return None if no icon found
    return None

def main():
    """Main entry point for the application"""
    # Load environment variables
    load_dotenv()
    
    # Create the QApplication
    app = QApplication(sys.argv)
    
    # Fix Windows taskbar icon grouping
    if sys.platform.startswith('win'):
        import ctypes
        myappid = 'retroachievements.romcollector.1.0.7'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    app.setApplicationName("RetroAchievements ROM Collector")
    app.setApplicationVersion("1.00.7")
    app.setOrganizationName("RetroAchievements")
    app.setOrganizationDomain("retroachievements.org")
    
    # Set application icon (this affects taskbar, alt-tab, etc.)
    icon_path = get_icon_path()
    if icon_path:
        app_icon = QIcon(icon_path)
        app.setWindowIcon(app_icon)  # Set for the entire application
        
        # On Windows, also set as the default window icon
        if sys.platform.startswith('win'):
            app.setWindowIcon(app_icon)
    
    # Set application style
    app.setStyleSheet(get_main_window_style())
    
    # Create and show the main window
    window = ROMCollectorGUI()
    
    # Set window icon (this affects the window title bar)
    if icon_path:
        window.setWindowIcon(QIcon(icon_path))
    
    window.show()
    
    # Run the application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()