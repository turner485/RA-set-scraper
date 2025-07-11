from PyQt5.QtCore import QThread, pyqtSignal
import os
import requests


class ROMDownloadThread(QThread):
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)

    def __init__(self, rom_data, source):
        super().__init__()
        self.rom_data = rom_data
        self.source = source

    def run(self):
        try:
            success = self.download_rom()
            if success:
                self.finished.emit(True, self.rom_data['name'])
            else:
                self.finished.emit(False, "Download failed")
        except Exception as e:
            self.finished.emit(False, str(e))

    def download_rom(self):
        url = self.source['full_url']
        filename = f"{self.rom_data['name']}{self.rom_data['extension']}"

        console = self.rom_data.get("console") or "UnknownConsole"
        base_path = self.rom_data.get("download_path", "downloads")
        downloads_dir = os.path.join(base_path, "Games", console)
        os.makedirs(downloads_dir, exist_ok=True)

        filepath = os.path.join(downloads_dir, filename)
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

