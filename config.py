BOT_TOKEN = 'ENTER BOT_TOKEN' # example: 1564184930:AAFmxeXzCfVLtcQ_rhWOX9FfkkXdxNAXAsA
API_HASH = 'ENTER API_HASH' # example: a91xx7390xxc6f5xxxb9dfxx87exxxxx
API_ID = 'ENTER API_ID' # example: 582164
CMP_API_KEY = 'ENTER CoinMarketCap API' # example: feca8xx5-3xx2-4xxc-axxc-55c4e8exxxxx
CHAT_ID = 'ENTER DESTINATION_ID' # example: 139946685 or coinsstats (write username channels without "@")
SUDO_ID = 'ENTER SUDO_ID' # example: 139946685
BOT_ID = int(BOT_TOKEN.split(':')[0]) # don't change it
coins_list = (
'bitcoin', 'ethereum', 'bitcoin-cash',
'litecoin', 'dash', 'binance-coin',
'cardano', 'vechain', 'ontology', 'holo',
'elrond-erd-2', 'chainlink', 'the-sandbox',
'cosmos', '1inch', 'polkadot',
'ripple', 'dogecoin', 'bridge-oracle'
) # just write symbol coin/token
