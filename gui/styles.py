"""
UI Styles for the RetroAchievements ROM Collector
"""

def get_button_style():
    """Get the standard button style"""
    return """
        QPushButton {
            background-color: #2C97FA;
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

def get_stop_button_style():
    """Get the stop button style (danger/red theme)"""
    return """
        QPushButton {
            background-color: #e74c3c;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #c0392b;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
    """

def get_clear_button_style():
    """Get the clear button style (secondary/gray theme)"""
    return """
        QPushButton {
            background-color: #95a5a6;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 5px;
        }
        QPushButton:hover {
            background-color: #7f8c8d;
        }
        QPushButton:disabled {
            background-color: #bdc3c7;
            color: #7f8c8d;
        }
    """

def get_main_window_style():
    """Get the main window style"""
    return """
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
    """

def get_progress_text_style():
    """Get the progress text area style"""
    return """
        background-color: #f8f9fa; 
        font-family: 'Courier New';
        border: 1px solid #bdc3c7;
        padding: 5px;
    """

def get_input_field_style():
    """Get the input field style"""
    return """
        border: 1px solid #bdc3c7;
        padding: 5px;
        background: white;
        border-radius: 3px;
    """

def get_title_style():
    """Get the title label style"""
    return """
        color: #2c3e50; 
        margin: 10px 0;
        font-weight: bold;
    """

def get_help_text_style():
    """Get the help text style"""
    return """
        color: #7f8c8d; 
        font-style: italic;
    """

def get_info_panel_style():
    """Get the info panel style"""
    return """
        background-color: #f8f9fa; 
        padding: 10px; 
        border-radius: 5px;
        border: 1px solid #e9ecef;
    """