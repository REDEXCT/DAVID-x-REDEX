import os
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from ordinal import create_nft, broadcast_transaction
from nft_listing import list_nfts
from fetch_nft_data import fetch_nft_data
from nft_transfer import transfer_nft

# Set up Flask app
app = Flask(__name__)

# Set up MongoDB
MONGO_URI = os.environ["MONGO_URI"]
client = MongoClient(MONGO_URI)
db = client.nft_marketplace
offers = db.offers

# Function to list NFT offers
def list_offers():
    return list(offers.find())

# Function to create an NFT offer
def create_offer(offer_data):
    return offers.insert_one(offer_data).inserted_id

# Function to update an NFT offer
def update_offer(offer_id, updated_data):
    offers.update_one({"_id": ObjectId(offer_id)}, {"$set": updated_data})

# Function to delete an NFT offer
def delete_offer(offer_id):
    offers.delete_one({"_id": ObjectId(offer_id)})

# Function to find a matching trade
def find_trade(offer_id):
    offer = offers.find_one({"_id": ObjectId(offer_id)})
    if not offer:
        return None

    matched_offer = offers.find_one({"nft_id": offer["wants_nft_id"]})
    return matched_offer

# Flask API endpoints for the marketplace

@app.route('/offers', methods=['GET'])
def get_offers():
    all_offers = list_offers()
    return jsonify(all_offers)

@app.route('/offers', methods=['POST'])
def post_offer():
    data = request.get_json()
    offer_id = create_offer(data)
    return jsonify({"success": True, "offer_id": str(offer_id)})

@app.route('/offers/<offer_id>', methods=['PUT'])
def put_offer(offer_id):
    data = request.get_json()
    update_offer(offer_id, data)
    return jsonify({"success": True})

@app.route('/offers/<offer_id>', methods=['DELETE'])
def delete_offer_endpoint(offer_id):
    delete_offer(offer_id)
    return jsonify({"success": True})

@app.route('/trades', methods=['POST'])
def post_trade():
    data = request.get_json()
    offer_id = data.get("offer_id")

    matched_offer = find_trade(offer_id)
    if not matched_offer:
        return jsonify({"success": False, "message": "No matching trade found"})

    # Perform the NFT transfer
    transfer_result = transfer_nft(
        offer_owner_wif=offer["owner_wif"],
        offer_owner_address=offer["owner_address"],
        wanted_nft_owner_wif=matched_offer["owner_wif"],
        wanted_nft_owner_address=matched_offer["owner_address"],
        offer_nft_txid=offer["nft_id"],
        wanted_nft_txid=matched_offer["nft_id"]
    )

    if transfer_result["success"]:
        delete_offer(offer_id)
        delete_offer(str(matched_offer["_id"]))
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "NFT transfer failed"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
