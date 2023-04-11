import sys
sys.path.insert(0, "./")

from cogsgpt.args import ArgsType
from cogsgpt.cogsmodel.cv import OCRModel, FormRecognizerModel

if __name__ == '__main__':
    # Test OCR model
    # ocr_model = OCRModel()
    # data = {
    #     ArgsType.IMAGE.value: "./samples/ocr.png"
    # }
    # print(ocr_model.run(**data))

    # Test form recognizer model
    form_recog_model = FormRecognizerModel()
    data = {
        ArgsType.IMAGE.value: "./samples/read.png"
    }
    print(form_recog_model.run(**data))