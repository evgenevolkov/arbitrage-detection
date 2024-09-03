# Assets market simulation with real-time arbitrage detection 

Creates an endpoit with dynamically updated prices of assets on different markets and a service, that queries current prices and searches for arbitrage possibilities: a buying price of an asset on one market is lower than the selling price for the same asset on another market.

Consists of two services: prices generator and prices analyzer

1. Prices generator.
Having a list of assets (e.g. Copper, Oil, Corn) and markets (e.g. US, Asia, etc.) randomly generates initial prices for each provided asset on each market, so that the inital price for the same asses is just slightly different on each market. 
Then an infinite loop for each asset and market is started, so that on each iteration a price is changed and a pause is set. Each runs independently in own loop.

Besides that an API is exposed, allowing to get current price for a specified asset on specified market.

2. Prices analyzer.
Provided an endpoint URL, a list of assets and a list of markets, infinetely querries for current price for each asset on each market. If possibility for arbitrage is detected  a message is outputed.


# Stack:
Python
FastAPI
Asyncio, Threading
Pydantic


# To install:

1. clone repo: 
2. If you are on MacOS or Linux: execute 'make install'. Otherwise, create virtual environment and install dependencies from `requirements.txt`
3. execute `make menu` and select `start generator`. You should be able to see uvicorn app starting logs and then logs of assets prices updates. 
4. open another one terminal instance and execute `make menu` and select `start analyzer`. You should see logs of retrieved assets prices and updates. Once there is an oportunity of arbitrage, a dedicate message would be displayed. 