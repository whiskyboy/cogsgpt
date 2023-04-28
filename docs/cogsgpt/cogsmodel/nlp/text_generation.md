Module cogsgpt.cogsmodel.nlp.text_generation
============================================

Classes
-------

`GenerativeTextSummarizationModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.nlp.text_generation.TextGenerationModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`GenerativeTextTranslationModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.nlp.text_generation.TextGenerationModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`TextGenerationModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

    ### Descendants

    * cogsgpt.cogsmodel.nlp.text_generation.GenerativeTextSummarizationModel
    * cogsgpt.cogsmodel.nlp.text_generation.GenerativeTextTranslationModel

    ### Methods

    `run(self, *args, **kwargs) ‑> str`
    :