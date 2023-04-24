import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.speech import Speech2TextModel, Text2SpeechModel

if __name__ == '__main__':
    # Test text2speech model
    text2speech_model = Text2SpeechModel()
    data = {
        ArgsType.TEXT.value: "I'm your AI assistant. You can call me Tina. How can I help you?"
    }
    audio_file = text2speech_model.run(**data)
    print(audio_file)

    # Test speech2text model
    speech2text_model = Speech2TextModel()
    data = {
        ArgsType.AUDIO.value: audio_file
    }
    print(speech2text_model.run(**data))