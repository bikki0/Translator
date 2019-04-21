import io

import html.parser as htmlparser

from google.cloud import speech_v1p1beta1 as speech
from google.cloud import texttospeech
from google.cloud import translate


class GoogleAPI:
    SAMPLE_RATE = 44100
    LANGUAGES = {
        'en': 'en-US',
        'ru': 'ru-RU',
        'fr': 'fr-FR',
        'de': 'de-DE',
        'es': 'es-ES'
    }

    def __init__(self):
        self._sound_to_text = speech.SpeechClient()
        self._text_to_sound = texttospeech.TextToSpeechClient()
        self._audio_config = texttospeech.types.AudioConfig(audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        self._translator = translate.Client()

    def speech_to_text(self, path, lang):
        with io.open(path, 'rb') as audio_file:
            content = audio_file.read()

        audio = self._sound_to_text.types.RecognitionAudio(content=content)

        sound_config = speech.types.RecognitionConfig(
            encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.SAMPLE_RATE,
            language_code=self.LANGUAGES[lang],
            enable_automatic_punctuation=True)

        response = self._sound_to_text.recognize(sound_config, audio)

        print(response)

        text = ''
        for result in response.results:
            text += result.alternatives[0].transcript

        return text

    def text_to_speech(self, text, lang, path='output.mp3'):
        voice = texttospeech.types.VoiceSelectionParams(
            language_code=self.LANGUAGES[lang],
            ssml_gender=texttospeech.enums.SsmlVoiceGender.FEMALE)
        response = self._text_to_sound.synthesize_speech(texttospeech.types.SynthesisInput(text=text),
                                                         voice,
                                                         self._audio_config)

        with open(path, 'wb') as out:
            out.write(response.audio_content)

    def translate(self, text, lang_to):
        translation = self._translator.translate(text, target_language=lang_to)['translatedText']
        # We need this parser to deal with ' and other non-alphabetic characters.
        parser = htmlparser.HTMLParser()
        return parser.unescape(translation)
