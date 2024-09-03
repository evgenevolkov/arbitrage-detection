import asyncio
# import httpx

from .utils.fetch_requests import PriceFetcher 
from .utils.logger import get_logger
from .core.detector import ArbitrageDetector


logger = get_logger(__name__)
semaphore = asyncio.Semaphore(200)


async def fetch_and_process_price(
        price_fetcher: PriceFetcher, 
        detector: ArbitrageDetector, asset: str, market: str):
    """High-level function that runs infinite loop to track price of an asset
    on specific market"""
    while True:
        asset_data = await price_fetcher.fetch_price(asset=asset, market=market)
        if asset_data:
            await detector.check_for_arbitrage(asset_data)
            async with semaphore:
                asyncio.create_task(detector.price_update(asset_data))


async def main():
    detector = ArbitrageDetector()
    price_fetcher = PriceFetcher()

    # initialize task for each asset / market pair
    tasks = []
    for asset in detector.assets_list:
        for market in detector.markets_list:
            tasks.append(fetch_and_process_price(price_fetcher, detector, asset, market))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())








