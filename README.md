# gpu-bot

## How it works

When a GPU is in stock, the bot will simply send a windows notification alert. The bot will not purchase the GPU for you. A proxy or VPN is recommended when using this bot.

This gpu bot will scan all links provided in the **links.txt** file. The bot will scan the following websites:

- **newegg.ca**
- **canadacomputers.com**
- **memoryexpress.com**
- **bestbuy.ca**

## Installation & Setup

You must install a custom version of [win10toast](https://github.com/jithurjacob/Windows-10-Toast-Notifications/pull/38) for this script to work. More info [here](https://github.com/jithurjacob/Windows-10-Toast-Notifications/pull/38#issuecomment-770334636)

`pip install -r requirements.txt`

`python ./main.py`

## Other notes

- `main.py` currently runs on **10** threads. you can increase or decrease this amount if need be
- `bot.scanLoop()` currently runs every 120 seconds. you can increase or decrease this amount of need be
