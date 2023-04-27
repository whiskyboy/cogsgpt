from __future__ import annotations

import os
import tempfile
import time

import azure.cognitiveservices.speech as speechsdk

from cogsgpt.schema import ArgsType, LanguageType
from cogsgpt.cogsmodel import BaseModel


class Text2SpeechModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()

        COGS_KEY = os.environ['COGS_KEY']
        COGS_REGION = os.environ['COGS_REGION']
        self.speech_config = speechsdk.SpeechConfig(subscription=COGS_KEY, region=COGS_REGION)

        self.supported_language = {
            LanguageType.English.value: "en-US",
            LanguageType.Chinese.value: "zh-CN",
        }

    def _text2speech(self, text: str, language: str = "en-US") -> str:
        self.speech_config.speech_synthesis_language = language
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
        speech_synthesis_stream = speechsdk.AudioDataStream(speech_synthesis_result)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix=".wav", delete=False) as temp_audio_file:
            speech_synthesis_stream.save_to_wav_file(temp_audio_file.name)
            return temp_audio_file.name

    def run(self, *args, **kwargs) -> str:
        text = kwargs[ArgsType.TEXT.value]
        language = kwargs.get(ArgsType.SRC_LANGUAGE.value, LanguageType.English.value)
        language = self.supported_language[language]
        return self._text2speech(text, language)
    

class Speech2TextModel(BaseModel):
    def __init__(self) -> None:
        super().__init__()
        
        COGS_KEY = os.environ['COGS_KEY']
        COGS_REGION = os.environ['COGS_REGION']
        self.speech_config = speechsdk.SpeechConfig(subscription=COGS_KEY, region=COGS_REGION)

        self.supported_language = {
            LanguageType.English.value: "en-US",
            LanguageType.Chinese.value: "zh-CN",
        }

    def _recognize_continuous(self, speech_recognizer: speechsdk.SpeechRecognizer) -> str:
        done = False
        text = ""

        def stop_cb(evt: speechsdk.SessionEventArgs) -> None:
            """callback that signals to stop continuous recognition upon receiving an event `evt`"""
            speech_recognizer.stop_continuous_recognition_async()
            nonlocal done
            done = True

        def retrieve_cb(evt: speechsdk.SpeechRecognitionEventArgs) -> None:
            """callback that retrieves the intermediate recognition results"""
            nonlocal text
            text += evt.result.text

        # retrieve text on recognized events
        speech_recognizer.recognized.connect(retrieve_cb)
        # stop continuous recognition on either session stopped or canceled events
        speech_recognizer.session_stopped.connect(stop_cb)
        speech_recognizer.canceled.connect(stop_cb)

        # Start continuous speech recognition
        speech_recognizer.start_continuous_recognition_async()
        while not done:
            time.sleep(.5)
        return text

    def _speech2text(self, audio_file: str, language: str = "en-US") -> str:
        self.speech_config.speech_recognition_language = language
        audio_config = speechsdk.AudioConfig(filename=audio_file)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=audio_config)
        # speech_recognition_result = speech_recognizer.recognize_once_async().get()
        speech_recognition_result = self._recognize_continuous(speech_recognizer)
        return speech_recognition_result

    def run(self, *args, **kwargs) -> str:
        audio_file = kwargs[ArgsType.AUDIO.value]
        language = kwargs.get(ArgsType.SRC_LANGUAGE.value, LanguageType.English.value)
        language = self.supported_language[language]
        return self._speech2text(audio_file, language)