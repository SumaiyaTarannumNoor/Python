import base64
import requests

# Function to encode a string to Base64
def encode_base64(string):
    encoded = base64.b64encode(string.encode('utf-8')).decode('utf-8')
    return encoded

# Function to decode Base64 to original string
def decode_base64(encoded_str):
    missing_padding = len(encoded_str) % 4
    if missing_padding:
        encoded_str += "=" * (4 - missing_padding)
    return base64.b64decode(encoded_str).decode("utf-8")

# Take the raw webhook URL as input from the user
raw_webhook_url = input("Enter the full webhook URL (e.g., https://discord.com/api/webhooks/...): ")

# Split the URL into base URL, ID, and token (assuming the format 'https://discord.com/api/webhooks/{webhook_id}/{token}')
base_url, webhook_id_token = raw_webhook_url.split("/api/webhooks/")
webhook_id, token = webhook_id_token.split("/")

# Encode the base URL, ID, and token to Base64
encoded_base = encode_base64(base_url + "/api/webhooks")
encoded_id = encode_base64(webhook_id)
encoded_token = encode_base64(token)

# Show the encoded Base64 parts
print("\nEncoded Webhook URL Parts:")
print(f"Base URL (encoded): {encoded_base}")
print(f"Webhook ID (encoded): {encoded_id}")
print(f"Token (encoded): {encoded_token}")

# Wait for the user to press any key to decode the values
input("\nPress any key to decode the Base64-encoded parts back into the original webhook URL...")

# Decode the parts back into the original format
decoded_base = decode_base64(encoded_base)
decoded_id = decode_base64(encoded_id)
decoded_token = decode_base64(encoded_token)

# Construct the final decoded webhook URL
final_decoded_url = f"{decoded_base}/{decoded_id}/{decoded_token}"

# Show the final decoded output
print("\nDecoded Webhook URL:")
print(f"Final Webhook URL: {final_decoded_url}")
