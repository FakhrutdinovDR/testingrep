import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = ''
TEXT: str = 'Увы, кина не будет'
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int


while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            getgif = requests.get(url='https://api.giphy.com/v1/gifs/random?api_key=PASTEYOURAPIKEY')
            if getgif.status_code == 200:
                requests.get(f"{API_URL}{BOT_TOKEN}/sendVideo?chat_id={chat_id}&video={getgif.json()['data']['images']['original_mp4']['mp4']}")
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={TEXT}')
    time.sleep(1)
    counter += 1