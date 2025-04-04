from scrappers.virgio_scrapper  import VirgioScrapper
from scrappers.westside_scrapper import WestsideScraper 
class ScraperFactory:
    """Factory to get the correct scraper for a given platform."""

    PLATFORM_MAP = {
        "virgio": VirgioScrapper,
        "westside": WestsideScraper,
    }

    @staticmethod
    def get_scraper(platform, url):
        if platform in ScraperFactory.PLATFORM_MAP:
            return ScraperFactory.PLATFORM_MAP[platform](url)
        else:
            raise ValueError(f"No scraper available for platform: {platform}")
