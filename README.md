# opbnb-minter
Quickly mint a [commemorative NFT](https://zkbridge.com/gallery/theOrigin) celebrating launch of opBNB mainnet to any number of wallets



## Quickstart
1. Create and activate virtual environment
```
python -m venv .venv
.\venv\Scripts\activate
```

2. Install dependencies
```
pip install web3 tqdm loguru pyfiglet
```

3. Insert private keys into keys.txt

4. Set delay time between wallets https://github.com/mikke555/opbnb-minter/blob/92bb83f8967b8d1567e09cbdc83c9875775f425e/main.py#L10-L11

5. Run the script
```
python main.py
```
