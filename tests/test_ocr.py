import sys
sys.path.insert(0, "./")

from cogsgpt.args import ArgsType
from cogsgpt.cogsmodel.cv import OCRModel

if __name__ == '__main__':
    # Test OCR model
    ocr_model = OCRModel()
    data = {
        ArgsType.IMAGE.value: "./samples/ocr.png"
    }
    print(ocr_model.run(**data))