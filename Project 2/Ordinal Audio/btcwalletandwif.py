import secrets
import hashlib
import base58

# Generate a 32-byte random private key
private_key = secrets.token_bytes(32)

# Add a 0x80 byte to the beginning of the private key
private_key_with_prefix = b"\x80" + private_key

# Calculate the double-SHA256 hash of the private key
hash1 = hashlib.sha256(private_key_with_prefix).digest()
hash2 = hashlib.sha256(hash1).digest()

# Take the first 4 bytes of the hash and append them to the private key
private_key_with_checksum = private_key_with_prefix + hash2[:4]

# Convert the resulting 37-byte string to base58 to get the WIF key
wif_key = base58.b58encode(private_key_with_checksum)

print(f"WIF key: {wif_key.decode('utf-8')}")
