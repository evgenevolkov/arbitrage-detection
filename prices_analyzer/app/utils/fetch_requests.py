import asyncio
import httpx

from ..utils import schemas
from ..utils.logger import get_logger


logger = get_logger(__name__)


class PriceFetcher:
    """Class responsible for fetching price of an asset on a market from predefined API"""

    api_url_template: str = None

    def __init__(self): 
        self._get_api_url_template()

    def _get_api_url_template(self):
        self.api_url_template: str = "http://127.0.0.1:8000/price?asset_name={asset}&market={market}"


    def get_api(self, asset, market):
        return self.api_url_template.format(asset=asset, market=market)


    async def fetch_price(self, asset: str, market: str):
        asset_data = None
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
                api_url = self.get_api(asset=asset, market=market)
                response = await client.get(api_url)
                response.raise_for_status()
                asset_data = response.json()
                print(f"Received asset data: {asset_data}")
                asset_data = schemas.AssetPriceFromApi(**asset_data)

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error for {asset} in {market}: {e}")
            await asyncio.sleep(0.1)
        except httpx.RequestError as e:
            logger.error(f"Request error for {asset} in {market}: {e}")
            await asyncio.sleep(0.1)
        return asset_data