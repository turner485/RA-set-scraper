from PyQt5.QtCore import QThread, pyqtSignal
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote
import os

from core.rom_sources import get_console_sources


class AsyncROMLoaderThread(QThread):
    roms_loaded = pyqtSignal(str, list)
    progress_update = pyqtSignal(str)
    error_occurred = pyqtSignal(str, str)

    def __init__(self, console_name):
        super().__init__()
        self.console_name = console_name

    def run(self):
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            roms = loop.run_until_complete(self.fetch_roms_async())
            self.roms_loaded.emit(self.console_name, roms)
        except Exception as e:
            self.error_occurred.emit(self.console_name, str(e))
        finally:
            loop.close()

    async def fetch_roms_async(self):
        sources = get_console_sources(self.console_name)
        if not sources:
            return []

        all_roms = []
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [self.fetch_from_source(session, src) for src in sources]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    self.progress_update.emit(f"Source {i+1} failed: {result}")
                    continue
                for rom in result:
                    rom['sources'] = rom.get('sources', []) + [{
                        'base_url': sources[i],
                        'full_url': rom['url']
                    }]
                all_roms.extend(result)
                self.progress_update.emit(f"Loaded {len(result)} from source {i+1}")

        # Deduplicate
        unique = {}
        for rom in all_roms:
            name = rom['name']
            if name not in unique:
                unique[name] = rom
            else:
                unique[name]['sources'].extend(rom['sources'])
        return list(unique.values())

    async def fetch_from_source(self, session, url):
        try:
            async with session.get(url) as resp:
                if resp.status != 200:
                    raise Exception(f"HTTP {resp.status}")
                html = await resp.text()
                return self.parse_html(html, url)
        except Exception as e:
            raise Exception(f"Fetch failed from {url}: {e}")

    def parse_html(self, html, base_url):
        soup = BeautifulSoup(html, 'html.parser')
        roms = []

        # ✅ Detect archive.org and extract collection folder correctly
        is_archive = "archive.org" in base_url
        archive_collection = ""
        if is_archive:
            # Ensure we preserve everything after "/download/"
            # E.g., https://archive.org/download/nointro.atari-2600 => nointro.atari-2600
            archive_collection = base_url.split("/download/")[-1].strip("/")

        for link in soup.find_all('a', href=True):
            href = link['href']
            if href in ['../', '/'] or href.endswith('/'):
                continue

            filename = unquote(href)
            name, ext = os.path.splitext(filename)
            if not ext:
                continue

            # ✅ Ensure archive.org link includes collection path
            if is_archive:
                full_url = f"https://archive.org/download/{archive_collection}/{filename}"
            else:
                full_url = urljoin(base_url, href)

            roms.append({
                'name': name,
                'extension': ext,
                'url': full_url
            })

        return roms
