from telethon.sync import TelegramClient
from datetime import datetime
from config import *
import requests
import asyncio
import redis


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
			url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest'
			headers2 = {
			  'Accepts': 'application/json',
			  'X-CMC_PRO_API_KEY': CMP_API_KEY,
			}
			for i in coins_list:
				coin = requests.get('https://api.coinstats.app/public/v1/coins/{}?currency=USD'.format(i), headers = headers).json()['coin']
				symbol = coin['symbol']
				price = float("{:.6f}".format(coin['price']))
				price_old = redis.get('{}.changes.{}'.format(BOT_ID, symbol))
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
				redis.set('{}.changes.{}'.format(BOT_ID, symbol), price)
			tim_e = "{:04d}/{:02d}/{:02d} {:02d}:{:02d}".format(ti_me.year, ti_me.month, ti_me.day, ti_me.hour, ti_me.minute)
			try: # section_2
				coinmarketcap = requests.get(url, headers = headers2).json()
				coinmarketcap = coinmarketcap['data']
				text = '{}\n- • - • - • - • -\nBTC.D • {:,.2f}%\nETH.D • {:,.2f}%'.\
				format(text, coinmarketcap['btc_dominance'], coinmarketcap['eth_dominance'])
			except Exception as e:
				await client.send_message(sudoID, "#BUG in section_2\n{}".format(e))
				text = '{}\n- • - • - • - • -\nBTC.D • {}%\nETH.D • {}%'.\
				format(text, "-", "-")
			text = '{}\n{}\n@{}'.format(text, tim_e, 'statSsnioC'[::-1])
			await send_to_destination(CHAT_ID, text, 'md')
	except Exception as e:
		await client.send_message(sudoID, "#BUG in section_1\n{}".format(e))

		
client.start(bot_token = BOT_TOKEN)
with client:
	client.loop.run_until_complete(main())
