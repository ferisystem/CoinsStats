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

