import asyncio
from ticle_scrapper import TicleScrapper

ticle_scrapper = TicleScrapper()
loop = asyncio.get_event_loop()
loop.run_until_complete(ticle_scrapper.find_elements_to_interact())
loop.run_until_complete(ticle_scrapper.execute_scrapping())