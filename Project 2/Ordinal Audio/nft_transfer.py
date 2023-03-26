import os
import json
import requests
from pycoin.networks.registry import network_for_netcode
from pycoin.encoding import wif_to_secret_exponent, is_address_valid
from pycoin.services.providers import spendables_for_address
from pycoin.tx import Tx, TxOut, TxIn

# Set up network and WIF
NETWORK = "BTC"
WIF = os.environ["WIF"]  # Your WIF (private key) here

# Set up Bitcoin addresses
sender_address = "1SenderAddressHere"
receiver_address = "1ReceiverAddressHere"

# Validate addresses
if not is_address_valid(sender_address) or not is_address_valid(receiver_address):
    raise ValueError("Invalid Bitcoin address")

# Prompt user for the existing NFT transaction hash
nft_txid = input("Enter the transaction hash of the NFT you want to transfer: ")

# Fetch the existing NFT transaction
API_ENDPOINT = f"https://api.blockcypher.com/v1/btc/main/txs/{nft_txid}"
response = requests.get(API_ENDPOINT)
if response.status_code != 200:
    raise ValueError(f"Error fetching NFT transaction: {response.content}")

# Extract the metadata from the NFT transaction output script
output_script = response.json()["outputs"][0]["script"]
metadata_hex = output_script.split("OP_RETURN ")[1]
metadata = json.loads(bytes.fromhex(metadata_hex).decode("utf-8"))

# Set up Bitcoin network
network = network_for_netcode(NETWORK)
key = network.ui.wif_to_key(WIF)

# Fetch spendables for the sender address
spendables = spendables_for_address(sender_address, NETWORK)

# Check if there are spendable outputs
if not spendables:
    raise ValueError("No spendable outputs found for the sender address")

# Create a transaction input
tx_input = TxIn(spendables[0].tx_hash_hex, spendables[0].tx_out_index)

# Create a transaction output with the NFT Script
script = "OP_RETURN " + metadata_hex
tx_output = TxOut(int(spendables[0].coin_value * 0.99), script)

# Create and sign the transaction
tx = Tx(version=1, txs_in=[tx_input], txs_out=[tx_output], unspents=spendables)
tx.sign([key.secret_exponent()])

# Get transaction as hex
transaction_hex = tx.as_hex()

print(f"Signed transaction: {transaction_hex}")

# Broadcast the transaction to the Bitcoin network
API_ENDPOINT = "https://api.blockcypher.com/v1/btc/main/txs/push"

response = requests.post(API_ENDPOINT, json={"tx": transaction_hex})
response_data = response.json()

if response.status_code == 200:
    print(f"Transaction broadcasted successfully. TXID: {response_data['tx']['hash']}")
else:
    print("Error broadcasting the transaction:")
    print(json.dumps(response_data, indent=2))
