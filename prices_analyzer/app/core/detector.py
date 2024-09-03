import asyncio
from typing import Dict, List

from ..utils import schemas
from ..utils.logger import get_logger


logger = get_logger(__name__)


class ArbitrageDetector:
    """
    Implements arbitrage detector. 
    
    Functionality:
    - Tracks lowest buying and highest selling prices detected, including 
      market where price was detected.
    - Provided a new price for an asset, detect arbitrage opportunity 
    """

    def __init__(self):
        self.prices_dict: Dict[str, schemas.AssetData] = {}
        self.assets_list: List[str] = None
        self.markets_list: List[str] = None
        self.lock = asyncio.Lock()
        self._set_assets_list()
        self._set_markets_list()
        self._initialize_prices()


    def _set_assets_list(self) -> None:
        """Mocks getting and storing a list of assets to track"""
        self.assets_list = ["Copper", "Oil"]

        # 100+ for high load testing 
        # self.assets_list = ["Copper", "Oil", "Gold", "Silver", "Corn", "Coffe", "Sugar", "Wheat", "Rice", "Cotton", "Natural Gas", "Platinum", "Palladium", "Aluminum", "Zinc", "Nickel", "Lead", "Tin", "Iron Ore", "Cobalt", "Lithium", "Uranium", "Ethanol", "Diesel", "Jet Fuel", "Heating Oil"] #, "Gasoline", "Bitumen", "Asphalt", "Steel", "Rubber", "Lumber", "Paper", "Wool", "Silk", "Leather", "Copper Scrap", "Aluminum Scrap", "Gold Scrap", "Platinum Scrap", "Solar Panels", "Wind Turbines", "Batteries", "Electric Vehicles", "Biofuels", "Hydrogen", "LNG (Liquefied Natural Gas)", "LPG (Liquefied Petroleum Gas)", "Coal", "Peat", "Firewood", "Charcoal", "Animal Feed", "Fertilizers", "Pesticides", "Herbicides", "Potash", "Phosphate", "Ammonia", "Urea", "Nitrogen", "Phosphorus", "Sulfur", "Magnesium", "Calcium", "Sodium", "Potassium", "Bauxite", "Boron", "Silicon", "Titanium", "Chromium", "Manganese", "Molybdenum", "Tungsten", "Vanadium", "Bismuth", "Germanium", "Gallium", "Indium", "Tellurium", "Selenium", "Tantalum", "Hafnium", "Zirconium", "Niobium", "Antimony", "Arsenic", "Cadmium", "Cesium", "Thallium", "Yttrium", "Samarium", "Gadolinium", "Terbium", "Dysprosium", "Holmium", "Erbium", "Thulium", "Ytterbium", "Lutetium", "Scandium", "Lanthanum", "Cerium", "Praseodymium", "Neodymium", "Promethium", "Europium", "Osmium", "Rhenium", "Ruthenium", "Rhodium", "Iridium", "Fluorspar", "Gypsum", "Salt", "Limestone", "Granite", "Marble", "Sand", "Gravel", "Clay", "Feldspar", "Phosphate Rock", "Potash Rock", "Bentonite", "Kaolin", "Talc", "Quartz", "Asbestos", "Barite", "Bentonite Clay", "Feldspar", "Graphite", "Talc", "Zeolites", "Borates", "Chromium Ore", "Nickel Ore", "Cobalt Ore", "Zinc Ore", "Lead Ore", "Tin Ore", "Bauxite Ore", "Manganese Ore", "Titanium Ore", "Uranium Ore", "Phosphate Ore", "Iron Ore Pellets", "Copper Ore", "Gold Ore", "Silver Ore", "Platinum Ore", "Palladium Ore", "Saltwater", "Freshwater", "Seawater", "Groundwater", "Deionized Water", "Distilled Water", "River Water", "Lake Water", "Glacier Water", "Bottled Water", "Tap Water", "Drinking Water", "Industrial Water", "Wastewater", "Reclaimed Water", "Rainwater", "Stormwater", "Snow", "Ice", "Brine", "Brackish Water", "Soft Water", "Hard Water", "Ultra-pure Water", "Process Water", "Cooling Water", "Boiling Water", "Hot Water", "Steam", "Wet Steam", "Dry Steam", "Superheated Steam", "Saturated Steam", "Low-Pressure Steam", "High-Pressure Steam", "Hydrogen Gas", "Oxygen Gas", "Nitrogen Gas", "Carbon Dioxide", "Argon Gas", "Helium Gas", "Methane Gas", "Propane Gas", "Butane Gas", "Ethane Gas", "Ammonia Gas", "Chlorine Gas", "Sulfur Dioxide Gas", "Hydrogen Sulfide Gas", "Acetylene Gas", "Carbon Monoxide Gas", "Nitrous Oxide Gas", "Ozone"]
        return


    def _set_markets_list(self) -> None:
        """Mocks getting and storing a list of markets to track"""
        self.markets_list = ["US", "UK"]

        # 8 markets for high load testing
        # self.market_list = ["US", "UK" , "Europe", "Asia", "Africa", "North America", "Eastern Europe", "Australia"] 
        return 


    def _initialize_prices(self) -> None:
        """Mocks getting initial prices for each asset"""
        for asset in self.assets_list:
            self.prices_dict[asset] = schemas.AssetData(
                price_buy = float('inf'),
                price_sell = 0.0,
                location_buy = "US",
                location_sell = "US"
            )
        return


    async def check_for_arbitrage(self, 
                                  asset_price: schemas.AssetPriceFromApi) -> dict:
        """Compares provided asset price with current stored price and 
        provides a response indicating if an arbitrage opportunity is detected 
        """

        response = {
            "arbitrage_found": False  # Initial value
            , "details": []           # Placeholder
        }

        async with self.lock:
            asset_data = self.prices_dict.get(asset_price.name, None)
            if not asset_data:
                return response

            curr_price_buy = asset_data.price_buy
            curr_price_sell = asset_data.price_sell

            new_price_buy = asset_price.price * (1 + asset_price.spread / 100)
            new_price_sell = asset_price.price * (1 - asset_price.spread / 100)

            if new_price_buy < curr_price_sell:
                message = ("Arbitrage possibility detected:"
                            + f" Buy from new location, sell at : {asset_data.location_sell}")
                response["details"].append({"message": message})
                logger.debug(message)
                response["arbitrage_found"] = True

            if new_price_sell > curr_price_buy:
                message = ("Arbitrage possibility detected."
                            + f" Buy from {asset_data.location_buy}, sell at new location")
                logger.debug(message)
                response["details"].append(message)
                response["arbitrage_found"] = True

        return response


    async def price_update(self, asset_data: schemas.AssetPriceFromApi) -> None:
        """Asyncroneous wrapper over function implementation. Adds timeout functionality 
        to drop execution if takes much longer than expected"""
        try:
            # timeout to avoid hanging
            await asyncio.wait_for(self._price_update_internal(asset_data), timeout=2.0)
        except asyncio.TimeoutError:
            logger.error(f"Timeout during price update for {asset_data.name} in {asset_data.market}")

        return


    async def _price_update_internal(self, asset_data: schemas.AssetPriceFromApi) -> None:
        """Implementation of price update.
        A price is updated in any of these cases:
        1) the new price comes from the same market as currently stored value
        2) the new buying price is lower than the stored one
        3) the new selling price is lower than the stored one
        """
        async with self.lock:
            curr_entry = self.prices_dict.get(asset_data.name, None)

            if not curr_entry:
                logger.error(f"Asset {asset_data.name} not found in prices_dict.")
                return

            new_price_buy = round(asset_data.price * (1 + asset_data.spread / 100), 4)
            new_price_sell = round(asset_data.price * (1 - asset_data.spread / 100), 4)
            new_location = asset_data.market

            logger.debug((f"Asset: {asset_data.name}, market: {asset_data.market}"
                            + f" curr_price_buy: {curr_entry.price_buy}"
                            + f" new_price_buy: {new_price_buy}")
                            + f" curr_price_sell: {curr_entry.price_sell}"
                            + f" new_price_sell: {new_price_sell}")

            if (new_price_buy < curr_entry.price_buy 
                or new_location == curr_entry.location_buy):
                logger.info(f"Updating buying price")
                curr_entry.price_buy = new_price_buy
                curr_entry.location_buy = new_location

            if (new_price_sell > curr_entry.price_sell
                or new_location == curr_entry.location_sell):
                logger.debug(f"Updating selling price")
                curr_entry.price_sell = new_price_sell
                curr_entry.location_sell = new_location

            self.prices_dict[asset_data.name] = curr_entry

        return