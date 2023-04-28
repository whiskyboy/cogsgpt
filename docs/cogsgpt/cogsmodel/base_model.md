Module cogsgpt.cogsmodel.base_model
===================================

Classes
-------

`BaseModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * cogsgpt.cogsmodel.cv.background_remover.BackgroundRemover
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.cv.image_analysis_v3.ImageAnalysisV3Model
    * cogsgpt.cogsmodel.cv.image_analysis_v4.ImageAnalysisV4Model
    * cogsgpt.cogsmodel.nlp.text_analysis.BaseAnalysisModel
    * cogsgpt.cogsmodel.nlp.text_generation.TextGenerationModel
    * cogsgpt.cogsmodel.nlp.text_summarize.BaseSummarizeModel
    * cogsgpt.cogsmodel.nlp.text_translation.TextTranslationModel
    * cogsgpt.cogsmodel.speech.speech.Speech2TextModel
    * cogsgpt.cogsmodel.speech.speech.Text2SpeechModel

    ### Methods

    `run(self, *args, **kwargs) ‑> str`
    :