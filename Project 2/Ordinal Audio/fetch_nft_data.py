import sys
import requests
import secrets
from pycoin.encoding import is_address_valid

def fetch_nft_data(txid):
    if not txid:
        raise ValueError("No transaction ID provided")
    if not isinstance(txid, str):
        raise ValueError("Transaction ID must be a string")

    API_ENDPOINT = f"https://api.blockcypher.com/v1/btc/main/txs/{txid}"
    response = requests.get(API_ENDPOINT)

    if response.status_code != 200:
        raise ValueError("Error fetching transaction data")

    response_data = response.json()
    for output in response_data["outputs"]:
        if "data_hex" in output:
            metadata_hex = output["data_hex"]
            metadata = bytes.fromhex(metadata_hex).decode("utf-8")
            return metadata

    raise ValueError("No NFT metadata found in transaction outputs")

if __name__ == "__main__":
    try:
        txid = sys.argv[1]
        metadata = fetch_nft_data(txid)
        print(metadata)
    except IndexError:
        print("Please provide a transaction ID as an argument")
    except ValueError as e:
        print(str(e))
    except Exception:
        print("An unexpected error occurred")
