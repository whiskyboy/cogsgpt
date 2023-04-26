import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.nlp import *

if __name__ == '__main__':
    # Test KeyPhraseModel
    model = KeyPhraseModel()
    data = {
        ArgsType.TEXT.value: "Dr. Smith has a very modern medical office, and she has great staff."
    }
    print(model.run(**data))

    # Test EntityLinkingModel
    model = EntityLinkingModel()
    data = {
        ArgsType.TEXT.value: """Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, 
        to develop and sell BASIC interpreters for the Altair 8800. 
        During his career at Microsoft, Gates held the positions of chairman,
        chief executive officer, president and chief software architect, 
        while also being the largest individual shareholder until May 2014."""
    }
    print(model.run(**data))

    # Test EntityRecognitionModel
    model = EntityRecognitionModel()
    data = {
        ArgsType.TEXT.value: "I had a wonderful trip to Seattle last week."
    }
    print(model.run(**data))

    # Test PIIModel
    model = PIIModel()
    data = {
        ArgsType.TEXT.value: "The employee's phone number is 555-555-5555."
    }
    print(model.run(**data))

    # Test SentimentClassiferModel
    model = SentimentAnalysisModel()
    data = {
        ArgsType.TEXT.value: "The food and service were unacceptable. The concierge was nice, however."
    }
    print(model.run(**data))

    # Test LanguageDetectionModel
    model = LanguageDetectionModel()
    data = {
        ArgsType.TEXT.value: "Ce document est rédigé en Français."
    }
    print(model.run(**data))