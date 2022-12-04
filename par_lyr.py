import time
import requests
from bs4 import BeautifulSoup

# We push and pull like a magnet do


class SongTitleScraperException(Exception):
    """Handles all song title extractor exceptions."""


class _ScraperFactory:
    """All scrapers are defined here."""

    PARAGRAPH_BREAK = '\n\n'
    source_code = None
    title = None

    def __call__(self, source_code, title):
        self.source_code = source_code
        self.title = title
        # print(f'1: {title}')

    def _update_title(self, title):
        self.title = title
        # print(f'2: {title}')

    def _genius_scraper_method_1(self):
        extract = self.source_code.select(".title")
        if not extract:
            # print(f'extract scraper 1 returns None')
            return None

        song_title = (extract[0].get_text()).strip()
        print(f'Met 1 Title: {song_title}')
        return song_title

    def _genius_scraper_method_2(self):
        all_extracts = self.source_code.select('h1[class*="SongHeaderdesktop__Title-sc-"]')
        if not all_extracts:
            # print(f'extract scraper 2 returns None')
            return None

        song_title = ''
        for extract in all_extracts:
            # print(f'extract: {extract}')
            for br in extract.find_all("br"):
                br.replace_with("\n")
            song_title += extract.get_text()

        # print(f'extract: {extract}')
        # song_title = (extract.get_text()).strip()
        # print(f'Met 2 Title: {song_title}')
        return song_title

    def genius_scraper(self):
        song_title = self._genius_scraper_method_1() or self._genius_scraper_method_2()
        self._update_title(self.title[:-16])
        # print(f'scraper: {song_title}')

        return song_title


class SongTitle:
    """
        Takes in Google Custom Search API & Google Engine ID in constructor args.
        Call get_lyrics function with song_name as args to get started.
        Handle raised SongTitleScraperException by importing it alongside.
    """

    scraper_factory = _ScraperFactory()
    SCRAPERS = {
        "genius": scraper_factory.genius_scraper,
    }

    def __init__(self, gcs_api_key: str, gcs_engine_id: str):
        if type(gcs_api_key) != str or type(gcs_engine_id) != str:
            raise TypeError("API key and engine ID must be a string.")

        self.GCS_API_KEY = gcs_api_key
        self.GCS_ENGINE_ID = gcs_engine_id

    def __handle_search_request(self, song_lyrics):
        url = "https://www.googleapis.com/customsearch/v1/siterestrict"
        params = {
            'key': self.GCS_API_KEY,
            'cx': self.GCS_ENGINE_ID,
            'q': '{} lyrics'.format(song_lyrics),
        }

        response = requests.get(url, params=params)
        data = response.json()
        # print(f'Data: {data}')
        if response.status_code != 200:
            raise SongTitleScraperException(data)
        return data

    def __extract_song_name(self, result_url, title):
        # Get the page source code
        page = requests.get(result_url)
        source_code = BeautifulSoup(page.content, 'lxml')
        # print(f'Title: {title}')
        self.scraper_factory(source_code, title)

        for domain, scraper in self.SCRAPERS.items():
            if domain in result_url:
                song_name = scraper()
                # print(f'Song Title: {song_name}')

        return song_name

    def get_song_name(self, song_lyrics: str) -> dict:
        """
            Fetches and autocorrects (if incorrect) song lyrics.
            Gets URL and title of the top Results.
            Extracts name by using one of the available scrapers.
            Raises SongTitleScraperException on handling errors.
            Returns dict with title and lyrics.
        """

        data = self.__handle_search_request(f'lyrics"{song_lyrics}"')

        spell = data.get('spelling', {}).get('correctedQuery')
        data = (spell and self.__handle_search_request(spell)) or data
        query_results = data.get('items', [])

        # Try scraping lyrics from top results
        for i in range(len(query_results)):
            result_url = query_results[i]["link"]
            title = query_results[i]["title"]
            try:
                song_name = self.__extract_song_name(result_url, title)
                # print(f'song Name is {song_name}')
            except Exception as err:
                raise SongTitleScraperException(err)

            if song_name:
                return {
                    "title": self.scraper_factory.title,
                    "song_name": song_name
                }

        raise SongTitleScraperException({"error": "No results found"})
