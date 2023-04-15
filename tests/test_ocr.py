import sys
sys.path.insert(0, "./")

from cogsgpt.utils import ArgsType
from cogsgpt.cogsmodel.cv import FormRecognizerModel

if __name__ == '__main__':
    # Test form recognizer model
    form_recog_model = FormRecognizerModel()
    data = {
        ArgsType.IMAGE.value: "./tests/examples/read.png"
    }
    print(form_recog_model.run(**data))