import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.nlp import *

if __name__ == '__main__':
    # Test TextGenerationModel
    model = TextGenerationModel()
    data = {
        ArgsType.TEXT.value: "Write a Chinene poem base on: A young girl is playing with a ball in the park. She is wearing a red shirt and blue shorts.",
    }
    print(model.run(**data))

    # Test GenerativeTextSummarizationModel
    model = GenerativeTextSummarizationModel()
    data = {
        ArgsType.TEXT.value: """TLDR: CogsGPT is a multi-modal LLM integrated ChatGPT with Azure Cognitive Service, inspired by HuggingGPT. 
        As the name CogsGPT suggests, it utilizes the ChatGPT model as the language center and integrates with Azure Cognitive Services to achieve multimodal capabilities to some extent."""
    }
    print(model.run(**data))

    # Test GenerativeTextTranslationModel
    model = GenerativeTextTranslationModel()
    data = {
        ArgsType.TEXT.value: "A multi-modal LLM integrated ChatGPT with Azure Cognitive Service, inspired by HuggingGPT.",
        ArgsType.SRC_LANGUAGE.value: "English",
        ArgsType.TGT_LANGUAGE.value: "Janpanese",
    }
    print(model.run(**data))