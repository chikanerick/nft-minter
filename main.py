from web3 import Web3
import json
import time
from settings import RPC_URL, DELAY
import random
rpc_url = RPC_URL
web3 = Web3(Web3.HTTPProvider(rpc_url))

if not web3.is_connected():
    raise Exception("[-] connect to Arbitrum network")

contract_address = '0x78072889Ee4D7Fe1A100C25296AABBEA32e92Bea'
method_id = '0xfb9d09c8'  
quantity = 5

with open('private_keys.txt', 'r') as file:
    wallets = [line.strip() for line in file]


successful_wallets_file = 'successful_wallets.txt'

def send_mint_transaction(wallet_private_key):
    try:
        account = web3.eth.account.from_key(wallet_private_key)
        wallet_address = account.address

        
        calldata = method_id + web3.to_hex(web3.to_bytes(quantity)).lstrip("0x").zfill(64)

        
        nonce = web3.eth.get_transaction_count(wallet_address)

        
        transaction = {
            'from': wallet_address,
            'to': contract_address,
            'value': web3.to_wei(0, 'ether'),  
            'gas': 2000000,  
            'gasPrice': web3.to_wei(0.01, 'gwei'),  
            'nonce': nonce,
            'data': calldata,
            'chainId': 42161,  
        }

       
        gas_limit = web3.eth.estimate_gas(transaction)
        transaction['gas'] = gas_limit

       
        signed_txn = web3.eth.account.sign_transaction(transaction, wallet_private_key)

      
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"[+] Transaction confirmed. Txn: {web3.to_hex(tx_hash)}")

       
        with open(successful_wallets_file, 'a') as f:
            f.write(f"{wallet_address}\n")

        return True  

    except Exception as e:
       
        print(f"[-] {wallet_address}: {e}")
        return False 


for private_key in wallets:
    success = send_mint_transaction(private_key)
    
    if success:
        delay = random.choice(DELAY) 
        print(f"[*] Sleep {delay} sec")   
       
        time.sleep(delay)  
        