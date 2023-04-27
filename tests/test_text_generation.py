import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.nlp import *

if __name__ == '__main__':
    # Test TextGenerationModel
    model = TextGenerationModel()
    data = {
        ArgsType.TEXT.value: "A young girl is playing with a ball in the park. She is wearing a red shirt and blue shorts.",
        "human_input": "Write a Chinene poem base on this image: ./samples/girl.png"
    }
    print(model.run(**data))