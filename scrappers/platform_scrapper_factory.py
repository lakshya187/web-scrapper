from scrappers.virgio_scrapper  import VirgioScrapper
from scrappers.westside_scrapper import WestsideScraper 
from scrappers.nyka_fashion_scrapper import NykaaScraper
from scrappers.tata_cliq_scrapper import TataCliqScraper    

class ScraperFactory:
    """Factory to get the correct scraper for a given platform."""
    PLATFORM_MAP = {
        "virgio": VirgioScrapper,
        "westside": WestsideScraper,
        "nykaafashion":  NykaaScraper,
        'tatacliq': TataCliqScraper,
    }

    @staticmethod
    def get_scraper(platform, url):
        if platform in ScraperFactory.PLATFORM_MAP:
            return ScraperFactory.PLATFORM_MAP[platform](url)
        else:
            raise ValueError(f"No scraper available for platform: {platform}")
