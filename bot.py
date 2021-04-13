from telethon.sync import TelegramClient
from datetime import datetime
import requests
import asyncio
import redis
from config import *


sudoID = int(SUDO_ID)
redis = redis.Redis(host = 'localhost', port = 6379, db = 0, decode_responses = True, encoding = 'utf-8')
client = TelegramClient(str(BOT_ID), int(API_ID), API_HASH)
loop = asyncio.get_event_loop()


def return_emoji_change(price_old, price):
	if price_old > price:
		emoji_change = "🔻"
	elif price_old < price:
		emoji_change = "🔹"
	elif price == 0:
		emoji_change = ""
	elif price_old == price:
		emoji_change = "🔸"
	return emoji_change


def return_percent(price_old, price):
	percent = ((price - price_old) / price_old) * 100
	return percent


def return_alarm(percent):
	if abs(percent) >= 50:
		alarm = '**♨️!!!**'
	elif abs(percent) >= 10:
		alarm = '**♨️!!**'
	elif abs(percent) >= 5:
		alarm = '**♨️!**'
	else:
		alarm = ''
	return alarm


async def send_to_destination(chatID, text, parse_mode):
	try:
		chatID = int(chatID)
	except:
		chatID = chatID
	return await client.send_message(chatID, text, parse_mode = parse_mode, link_preview = False)


async def main():
	ti_me = datetime.now()
	now_time = int("{:02d}{:02d}".format(ti_me.hour, ti_me.minute))
	try: # section_1
		if now_time % 10 == 0:
			text = ''
			headers = {'Cache-Control': 'no-cache'}
			for i in coins_list:
				coin = requests.get('https://api.coinstats.app/public/v1/coins/{}?currency=USD'.format(i), headers = headers).json()['coin']
				symbol = coin['symbol']
				price = float("{:.6f}".format(coin['price']))
				price_old = redis.get('coinstats.changes.{}'.format(symbol))
				if price_old:
					price_old = float(price_old)
					emoji_change = return_emoji_change(price_old, price)
					percent = return_percent(price_old, price)
					alarm = return_alarm(percent)
					if percent > 0:
						percent = "`+{:.2f}%`".format(percent)
					else:
						percent = "`{:.2f}%`".format(percent)
				else:
					emoji_change = ''
					percent = ''
					alarm = '🆕💫'
				if symbol == "BRG":
					link = '[{0}](https://www.bw.com/newTrade/spotTradding/brg_usdt)'.format(symbol)
				elif symbol == "KIN":
					link = '[{0}](https://hitbtc.com/kin-to-btc)'.format(symbol)
				else:
					link = '[{0}](https://binance.com/en/trade/{0}_USDT)'.format(symbol)
				text = "{}\n{} • **{:,}**$ {} {}   {}".\
				format(text, link, price, emoji_change, percent, alarm)
				redis.set('coinstats.changes.{}'.format(symbol), price)
				tim_e = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}".format(ti_me.year, ti_me.month, ti_me.day, ti_me.hour, ti_me.minute)
