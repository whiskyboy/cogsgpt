import sys
sys.path.insert(0, "./")

from cogsgpt.utils import ArgsType, LanguageType
from cogsgpt.cogsmodel.nlp import *

if __name__ == '__main__':
    # Test TextGenerationModel
    model = TextGenerationModel()
    data = {
        ArgsType.TEXT.value: "A young girl is playing with a ball in the park. She is wearing a red shirt and blue shorts.",
        "from_language": LanguageType.English.value,
        "to_language": LanguageType.Chinese.value,
        "human_input": "Write a Chinene poem base on this image: ./samples/girl.png"
    }
    print(model.run(**data))