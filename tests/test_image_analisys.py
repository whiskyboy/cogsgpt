import sys
sys.path.insert(0, "./")

from cogsgpt.utils import ArgsType
from cogsgpt.cogsmodel.cv import ImageAnalysisModel

if __name__ == '__main__':
    # Test Image Analysis model
    image_analysis_model = ImageAnalysisModel()
    data = {
        ArgsType.IMAGE.value: "./tests/examples/presentation.png"
    }
    print(image_analysis_model.run(**data))