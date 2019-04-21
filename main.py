from api_provider import APIProvider
from buttons import Button, Switch
from recorder import Recorder
from screen import Screen
from threading import Thread
import logging
import time
import subprocess
import RPi.GPIO as GPIO


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


class Translator:
    LANGUAGES = ['ru', 'fr', 'de', 'es']
    BASE_LANGUAGE = 'en'

    TRY_AGAIN_PHRASES = {'en': 'I\'m sorry, I did not understand you. Please, try again.',
                         'fr': 'Je suis désolé, je ne vous ai pas compris. Veuillez réessayer.',
                         'ru': 'Извините, я вас не поняла. Пожалуйста, попробуйте еще раз.',
                         'de': 'Es tut mir leid, ich habe dich nicht verstanden. Bitte versuche es erneut.',
                         'es': 'Lo siento, no te entendí. Inténtalo de nuevo.'}

    def __init__(self, screen, api_provider):
        self._language = 0
        self._is_customer = True
        self._screen = screen
        self._api_provider = api_provider

        self._screen.display_text(self.LANGUAGES[self._language])
        self._is_recording = False
        self._logger = logging.getLogger(self.__class__.__name__)
        self._thread = None

        self._recorder = Recorder()

    def _start_recording(self):
        self._logger.debug('start_recording')

        self._is_recording = True
        lang_to_speak = 'en' if self._is_customer else self.LANGUAGES[self._language]
        lang_to_rec = self.LANGUAGES[self._language] if self._is_customer else 'en'

        self._recorder.start()

        while self._is_recording:
            time.sleep(0.5)

        self._recorder.stop()
        self._logger.debug('Audio is recordered!')
        recognized_text = self._api_provider.speech_to_text('output.wav', lang_to_rec)
        self._logger.debug('Recognized text: {}'.format(recognized_text))

        lang_of_speech = lang_to_speak
        if not recognized_text:
            translated_text = self.TRY_AGAIN_PHRASES[lang_to_rec]
            self._logger.debug('Try-again text: {}'.format(translated_text))
            lang_of_speech = lang_to_rec if self._is_customer else lang_to_speak
        else:
            self._is_customer ^= True
            self._screen.display_text(lang_to_speak)
            translated_text = self._api_provider.translate(recognized_text, lang_to_speak)
            self._logger.debug('Translated text: {}'.format(translated_text))

        APIProvider.text_to_speech(translated_text, lang_of_speech)
        self._logger.debug('Playing sound...')
        self._play_sound('output.mp3')

    def start_recording(self):
        if self._thread:
            self._thread.join()
        self._thread = Thread(target=self._start_recording)
        self._thread.start()

    def stop_recording(self):
        self._logger.debug('stop_recording')
        self._is_recording = False

    def switch_language(self):
        if self._is_recording:
            return

        self._logger.debug('switch_language')
        self._is_customer = True
        self._language = (self._language + 1) % len(self.LANGUAGES)
        self._screen.display_text(self.LANGUAGES[self._language])

    @staticmethod
    def _play_sound(path):
        subprocess.Popen(['mpg123', '-q', path]).wait()


if __name__ == '__main__':
    # setup buttons
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    screen = Screen()
    api_provider = APIProvider()
    translator = Translator(screen, api_provider)
    button = Button(translaor.switch_language)
    switch = Switch(translator.start_recording, translator.stop_recording)

    # add events
    GPIO.add_event_detect(15, GPIO.RISING, callback=lambda _: button.click())
    GPIO.add_event_detect(18, GPIO.RISING, callback=lambda _: switch.click())

    while True:
        pass

    GPIO.cleanup()
