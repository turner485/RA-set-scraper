def get_primary_button_style():
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


def get_secondary_button_style():
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
