from scrappers.platform_scrapers.virgio import VirgioScrapper
from scrappers.platform_scrapers.westside import WestsideScraper
from scrappers.platform_scrapers.nyka_fashion import NykaaScraper
from scrappers.platform_scrapers.tata_cliq import TataCliqScraper


class ScraperFactory:
    """Factory to get the correct scraper for a given platform."""

    PLATFORM_MAP = {
        "virgio": VirgioScrapper,
        "westside": WestsideScraper,
        "nykaafashion": NykaaScraper,
        "tatacliq": TataCliqScraper,
    }

    @staticmethod
    def get_scraper(platform, url):
        if platform in ScraperFactory.PLATFORM_MAP:
            return ScraperFactory.PLATFORM_MAP[platform](url)
        else:
            raise ValueError(f"No scraper available for platform: {platform}")
