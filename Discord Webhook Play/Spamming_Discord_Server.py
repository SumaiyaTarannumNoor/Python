import requests

# Your Discord webhook URL
webhook_url = "https://discord.com/api/webhooks/1340617822145089546/elBRdyyzwfeZqgDVkTuKzKmY0QigoKMhO2gz_HAA5OBHexEhE04LeEyCE5ey34Q6Njpy"

# JSON payload (message content)
data = {
    "content": "Because I am a bit curious... XOXO",
    "username": "Mayisha ❤️"
}

# Send the POST request to the webhook URL
response = requests.post(webhook_url, json=data)

# Check the response status
if response.status_code == 204:
    print("✅ Message sent successfully! GPT is good.")
else:
    print(f"❌ Failed to send message. You Failure! Status Code: {response.status_code}, Response: {response.text}")
