from flask import Flask, request, jsonify
from fetch_nft_data import fetch_nft_data
from nft_listing import list_nfts
from ordinal import create_nft, broadcast_transaction
from nftMarketplace import get_offers, post_offer, put_offer, delete_offer_endpoint, post_trade

app = Flask(__name__)

@app.route('/nft-data/<txid>', methods=['GET'])
def get_nft_data(txid):
    try:
        nft_data = fetch_nft_data(txid)
        return jsonify({"success": True, "nft_data": nft_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/nfts/<address>', methods=['GET'])
def get_nfts(address):
    try:
        nfts = list_nfts(address)
        return jsonify({"success": True, "nfts": nfts})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/create-nft', methods=['POST'])
def create_nft_transaction():
    try:
        data = request.get_json()
        sender_address = data.get("sender_address")
        receiver_address = data.get("receiver_address")
        metadata = data.get("metadata")

        transaction_hex = create_nft(sender_address, receiver_address, metadata)
        txid = broadcast_transaction(transaction_hex)

        return jsonify({"success": True, "txid": txid})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Marketplace API endpoints
@app.route('/offers', methods=['GET'])
def get_all_offers():
    return get_offers()

@app.route('/offers', methods=['POST'])
def create_offer():
    return post_offer()

@app.route('/offers/<offer_id>', methods=['PUT'])
def update_offer(offer_id):
    return put_offer(offer_id)

@app.route('/offers/<offer_id>', methods=['DELETE'])
def remove_offer(offer_id):
    return delete_offer_endpoint(offer_id)

@app.route('/trades', methods=['POST'])
def create_trade():
    return post_trade()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
