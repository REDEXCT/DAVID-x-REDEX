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

# Set up NFT metadata
metadata = {
    "name": "My Bitcoin NFT",
    "description": "This is my first Bitcoin NFT",
    "image": "https://example.com/nft.png",
    "attributes": [
        {"trait_type": "Color", "value": "Red"},
        {"trait_type": "Size", "value": "Large"}
    ]
}

# Convert metadata to hex
metadata_hex = metadata.dumps().hex()

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
