from http import HTTPStatus
import json
import urllib.parse
import urllib3


class YandexAPI:
    LANGUAGES = {
        'en': 'en-US',
        'ru': 'ru-RU'
    }

    TEXT_TO_SPEECH_URL = 'https://tts.voicetech.yandex.net/generate?key={key}&text={text}&format=mp3&lang={lang}&speaker=alyss&emotion=good'

    def __init__(self):
        with open('apis/credentials.json') as f:
            config = json.load(f)

        self._api_key = config['key']

    def text_to_speech(self, text, lang, path='output.mp3'):
        if lang not in self.LANGUAGES:
            assert RuntimeError('{} is not supported'.format(lang))

        http = urllib3.PoolManager()
        url = self.TEXT_TO_SPEECH_URL.format(
            key=self._api_key,
            text=urllib.parse.quote_plus(text),
            lang=self.LANGUAGES[lang]
        )
        print(url)
        response = http.request('GET', url)

        if response.status == HTTPStatus.OK:
            with open(path, 'wb') as f:
                f.write(response.data)
