import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.cv import *

if __name__ == '__main__':
    # Test Image Tagging model
    model = ImageTaggingModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/house_yard.png"
    }
    print(model.run(**data))

    # Test Image Caption model
    model = ImageCaptionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/media/quickstarts/presentation.png"
    }
    print(model.run(**data))

    # Test Object Detection model
    model = ObjectDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/windows-kitchen.jpg"
    }
    print(model.run(**data))

    # Test Image Text Model
    model = ImageTextModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/handwritten-note.jpg"
    }
    print(model.run(**data))

    # Test Smart Crop Model
    model = SmartCropModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/cropped-original.png"
    }
    print(model.run(**data))

    # Test People Detection Model
    model = PeopleDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/family_photo.png"
    }
    print(model.run(**data))
