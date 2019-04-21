from apis.google_api import GoogleAPI
from apis.yandex_api import YandexAPI


class APIProvider:
    def __init__(self):
        self._google = GoogleAPI()
        self._yandex = YandexAPI()

    def speech_to_text(self, path, lang):
        return self._google.speech_to_text(path, lang)

    def text_to_speech(self, text, lang, path='output.mp3'):
        api_provider = self._yandex if lang == 'ru' else self._google
        return api_provider.text_to_speech(text, lang, path)

    def translate(self, text, lang_to):
        return self._google.translate(text, lang_to)
