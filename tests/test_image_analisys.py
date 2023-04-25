import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.cv import *

if __name__ == '__main__':
    # Test Image Tagging model
    print("\nTest Image Tagging model")
    model = ImageTaggingModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/house_yard.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Image Caption model
    print("\nTest Image Caption model")
    model = ImageCaptionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/media/quickstarts/presentation.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Object Detection model
    print("\nTest Object Detection model")
    model = ObjectDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/windows-kitchen.jpg"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Image Text Model
    print("\nTest Image Text Model")
    model = ImageTextModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/handwritten-note.jpg"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Smart Crop Model
    print("\nTest Smart Crop Model")
    model = SmartCropModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/cropped-original.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test People Detection Model
    print("\nTest People Detection Model")
    model = PeopleDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/family_photo.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Image Category Model
    print("\nTest Image Category Model")
    model = ImageCategorizeModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/satya.jpeg"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Brand Detection Model
    print("\nTest Brand Detection Model")
    model = BrandDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/gray-shirt-logo.jpg"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Face Detection Model
    print("\nTest Face Detection Model")
    model = FaceDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/family_photo.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Adult Content Detection Model
    print("\nTest Adult Content Detection Model")
    model = AdultContentDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/family_photo_face.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Color Scheme Detection Model
    print("\nTest Color Scheme Detection Model")
    model = ColorSchemeDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/mountain_vista.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))

    # Test Image Type Detection Model
    print("\nTest Image Type Detection Model")
    model = ImageTypeDetectionModel()
    data = {
        ArgsType.IMAGE.value: "https://learn.microsoft.com/en-us/azure/cognitive-services/computer-vision/images/lion_drawing.png"
    }
    print(model.run(**data))
    data = {
        ArgsType.IMAGE.value: "./tests/examples/wedding.png"
    }
    print(model.run(**data))
