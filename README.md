# Assets market simulation with real-time arbitrage detection 

Simulation of assets markets and service to detect arbitrage possibilities between markets.


## Consists of two services: prices generator and prices analyzer


__1. Prices generator.__

Constantly updates prices for each asset on each market.

Provides read access to the current price of an asset on a specific market via API.


_In details:_ Having a list of assets (e.g. Copper, Oil, Corn) and markets (e.g. US, Asia, etc.) provided, randomly generates initial prices for each asset on each market, so that the inital price for the same asset is just slightly different across each market.
Then an infinite price update loop for each asset and market is started. On each iteration price is changed by a value, randomly generated within predefined range. Each loop runs independently.


__2. Prices analyzer.__

Infinitely queries for a current price for each asset on each market. If possibility for arbitrage is detected a message is output.

Accepts API endpoint URL, a list of assets and a list of markets as parameters.

# Stack:

Business logic: __Python__

API interface: __FastAPI__

Concurrency: __Asyncio, multithreading__

Data typing: __Pydantic__


# To install:

1. clone repo: 

`git clone git@github.com:evgenevolkov/arbitrage-detection.git`

2. If you are on MacOS or Linux: execute:

`make install`

Otherwise, manually create a virtual environment and install dependencies from `requirements.txt`

3. execute `make` and select `start generator`. You should be able to see uvicorn app starting logs and then logs of assets prices updates.

4. open another one terminal instance and execute `make` and select `start analyzer`. You should see logs of retrieved assets prices and updates. Once there is an opportunity of arbitrage, a dedicated message would be displayed.