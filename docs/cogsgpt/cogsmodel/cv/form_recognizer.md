Module cogsgpt.cogsmodel.cv.form_recognizer
===========================================

Classes
-------

`BusinessCardFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`FormKeyValueModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`FormLayoutModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`FormReadModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`FromRecognizerBaseModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

    ### Descendants

    * cogsgpt.cogsmodel.cv.form_recognizer.FormKeyValueModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FormLayoutModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FormReadModel
    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel

    ### Methods

    `run(self, *args, **kwargs) ‑> str`
    :

`IDDocumentFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`InvoiceFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`PrebuiltFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

    ### Descendants

    * cogsgpt.cogsmodel.cv.form_recognizer.BusinessCardFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.IDDocumentFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.InvoiceFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.ReceiptFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.W2TaxFormModel

`ReceiptFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC

`W2TaxFormModel()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * cogsgpt.cogsmodel.cv.form_recognizer.PrebuiltFormModel
    * cogsgpt.cogsmodel.cv.form_recognizer.FromRecognizerBaseModel
    * cogsgpt.cogsmodel.base_model.BaseModel
    * abc.ABC