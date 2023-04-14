import sys
sys.path.insert(0, "./")

from cogsgpt.utils import ArgsType, LanguageType
from cogsgpt.cogsmodel.nlp import *

if __name__ == '__main__':
    # Test TextTranslationModel
    model = TextTranslationModel()
    data = {
        ArgsType.TEXT.value: "The extractive summarization feature uses natural language processing techniques to locate key sentences in an unstructured text document. "
        "These sentences collectively convey the main idea of the document. This feature is provided as an API for developers. " 
        "They can use it to build intelligent solutions based on the relevant information extracted to support various use cases. "
        "In the public preview, extractive summarization supports several languages. It is based on pretrained multilingual transformer models, part of our quest for holistic representations. "
        "It draws its strength from transfer learning across monolingual and harness the shared nature of languages to produce models of improved quality and efficiency. ",
        "from_language": LanguageType.English.value,
        "to_language": LanguageType.Chinese.value,
    }
    print(model.run(**data))