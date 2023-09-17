from web3 import Web3
from tqdm import tqdm
from loguru import logger
import pyfiglet
import time
import random
import json

BSC_RPC = 'https://binance.llamarpc.com'
MIN_SLEEP = 30
MAX_SLEEP = 60

web3 = Web3(Web3.HTTPProvider(endpoint_uri=BSC_RPC))

contract_addr = '0x427A258d7184Ceb1cB7FFA7Ec91983040bD386E5'
with open('abi.json', 'r') as f:
    abi = json.load(f)

contract = web3.eth.contract(address=contract_addr, abi=abi)
name = contract.functions.name().call()
endTime = contract.functions.mintEndTime().call()

logger.add(
    "debug.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="ERROR",
)

def mint(private_key):
    try:
        wallet_address = web3.eth.account.from_key(private_key).address
        nonce = web3.eth.get_transaction_count(wallet_address)
        gas_price = Web3.to_wei(1, 'gwei')

        tx = contract.functions.mint().build_transaction({'from': wallet_address, 'nonce': nonce, 'gasPrice': gas_price})
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
    
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction) 
        logger.info(f'wallet {wallet_address} | tx_hash {tx_hash.hex()}')

        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=500)

        if tx_receipt.status == 1:
            logger.success(f'Tx confirmed | https://bscscan.com/tx/{tx_hash.hex()}\n')
        else:
            raise ValueError("Tx failed")

    except Exception as error:
         logger.error(f"wallet {wallet_address} | {error}\n")

def load_keys():
    with open("keys.txt", "r") as f:
        keys = [row.strip() for row in f]
        return keys
    
def sleep():
    x = random.randint(MIN_SLEEP, MAX_SLEEP)
    for i in tqdm(range(x), desc='sleeping for', bar_format='{desc}: {n_fmt}/{total_fmt} seconds'):
        time.sleep(1)
    print()


if __name__ == '__main__':
    if endTime < time.time():
        raise ValueError("The mint has ended.")
    
    print('\n\n', pyfiglet.figlet_format(name, font="larry3d", width=330), end='\n\n')
    
    keys_list = load_keys()
    random.shuffle(keys_list)
    logger.info('keys loaded\n')

    while keys_list:
        key = keys_list.pop(0)
        mint(key)
        if keys_list:
            sleep()
    
    logger.success("Minting complete.\n")
