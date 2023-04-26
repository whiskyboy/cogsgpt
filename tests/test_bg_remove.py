import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.cv import *

if __name__ == '__main__':
    # Test Background Remover model
    print("\nTest Background Remover model")
    model = BackgroundRemover()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/media/background-removal/person-5.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))