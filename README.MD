
# Disclaimer
This script is provided for educational and informational purposes only. The use of this script is at your own risk. The author of this script assumes no responsibility or liability for any damages or consequences, including but not limited to account bans, data loss, or legal actions, resulting from the use or misuse of this script.

By using this script, you acknowledge that you understand and agree to this disclaimer. You are solely responsible for ensuring that your use of this script complies with all applicable laws, terms of service, and guidelines provided by the relevant platforms and services.

USE THIS SCRIPT AT YOUR OWN RISK.

# Prick Bot Auto Claim

Created by marylnrose with some code obtained from https://github.com/akasakaid. DO WITH YOUR OWN RESEARCH (DWYOR) because this app has banned fields from json response. 

You can start Prick bot by using my refferal code (if you want): https://t.me/Prickgame_bot?start=ref-fjQUywCdDT3yZ9BSpe7Fn8

# How to use
- pip install -r requirements.txt
- Open Prick bot and then webview inspect
- Open network tab and then click on ws request
- Click messages tab and then click uppermost request
- Expand the requests until you find telegramId
- Paste the telegram id to config.json
- python botv1.py

# Config.json

| Parameter | Type     | Description                |Default Value|
| :-------- | :------- | :------------------------- |-----------------|
| `telegram_id` | `int` | **Required**. Your Telegram Id |12345|
| `clicks` | `int` | **Required**. Amount of clicks generated |5|
| `delay_click_in_ms` | `int` | **Required**. Delay click after generating click event |1000ms|
| `delay_empty_energy_in_second` | `int` | **Required**. Waiting time when energy is empty|1800s|