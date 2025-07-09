from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit,
    QPushButton, QGroupBox, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt


class SettingsTab(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # API and download path settings
        self.setup_api_and_path_settings(layout)

        # Save button
        save_btn = QPushButton("💾 Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        self.add_version_info(layout)
        layout.addStretch()
        

    def setup_api_and_path_settings(self, layout):
        group = QGroupBox("RetroAchievements Settings")
        grid = QGridLayout(group)

        # API Key
        grid.addWidget(QLabel("API Key:"), 0, 0)
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.Password)
        grid.addWidget(self.api_key_edit, 0, 1)

        toggle_btn = QPushButton("👁️ Show/Hide")
        toggle_btn.clicked.connect(self.toggle_api_key_visibility)
        grid.addWidget(toggle_btn, 0, 2)

        api_help = QLabel("Get your API key from: https://retroachievements.org/controlpanel.php")
        api_help.setStyleSheet("color: #7f8c8d; font-style: italic;")
        grid.addWidget(api_help, 1, 0, 1, 3)

        # Download path
        grid.addWidget(QLabel("Download Path:"), 2, 0)
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        grid.addWidget(self.path_edit, 2, 1)

        browse_btn = QPushButton("📁 Browse")
        browse_btn.clicked.connect(self.browse_path)
        grid.addWidget(browse_btn, 2, 2)

        layout.addWidget(group)

    def toggle_api_key_visibility(self):
        if self.api_key_edit.echoMode() == QLineEdit.Password:
            self.api_key_edit.setEchoMode(QLineEdit.Normal)
        else:
            self.api_key_edit.setEchoMode(QLineEdit.Password)

    def browse_path(self):
        current = self.parent.get_download_path()
        path = QFileDialog.getExistingDirectory(self, "Select Download Directory", current)
        if path:
            self.path_edit.setText(path)

    def load_settings(self):
        self.api_key_edit.setText(self.parent.get_api_key())
        self.path_edit.setText(self.parent.get_download_path())

    def save_settings(self):
        api_key = self.api_key_edit.text().strip()
        download_path = self.path_edit.text().strip()

        if not api_key:
            QMessageBox.warning(self, "Missing API Key", "Please enter your API key.")
            return
        if not download_path:
            QMessageBox.warning(self, "Missing Download Path", "Please select a download directory.")
            return

        self.parent.set_api_key(api_key)
        self.parent.set_download_path(download_path)
        self.parent.config.save_config(api_key=api_key, download_path=download_path)
        

        QMessageBox.information(self, "Settings Saved", "Settings saved successfully.")

    def add_version_info(self, layout):
        version_label = QLabel("Version: 1.00.7 - developed and maintained by devbenji 😎")
        version_label.setStyleSheet("color: #7f8c8d; font-size: 8pt; font-style: italic;")
        layout.addWidget(version_label)