import sys
import requests

def list_nfts(address):
    if not address:
        raise ValueError("Address cannot be empty")

    API_ENDPOINT = f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/full"
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        response_data = response.json()
    except requests.exceptions.RequestException as e:
        raise ValueError(f"Error fetching address data: {e}")

    nfts = []
    if "txs" in response_data:
        for tx in response_data["txs"]:
            for output in tx["outputs"]:
                if "data_hex" in output:
                    try:
                        metadata_hex = output["data_hex"]
                        metadata = bytes.fromhex(metadata_hex).decode("utf-8")
                        nfts.append({"txid": tx["hash"], "metadata": metadata})
                    except ValueError as e:
                        print(f"Error decoding metadata: {e}")
    else:
        raise ValueError("No transactions found for the given address")

    return nfts

if __name__ == "__main__":
    try:
        address = sys.argv[1]
        nfts = list_nfts(address)
        print(nfts)
    except (IndexError, ValueError) as e:
        print(f"Error: {e}")
