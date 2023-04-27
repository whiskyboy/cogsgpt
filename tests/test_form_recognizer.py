import sys
sys.path.insert(0, "./")

from cogsgpt.schema import ArgsType
from cogsgpt.cogsmodel.cv import *

if __name__ == '__main__':
    # Test FormReadModel
    print("\nTest FormReadModel")
    form_recog_model = FormReadModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/read.png"
    }
    print(form_recog_model.run(**data))

    # Test FormLayoutModel
    print("\nTest FormLayoutModel")
    form_layout_model = FormLayoutModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/layout.png"
    }
    print(form_layout_model.run(**data))

    # Test FormKeyValueModel
    print("\nTest FormKeyValueModel")
    form_kv_model = FormKeyValueModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-layout.pdf"
    }
    print(form_kv_model.run(**data))

    # Test W2TaxFormModel
    print("\nTest W2TaxFormModel")
    w2tax_form_model = W2TaxFormModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/w2.png"
    }
    print(w2tax_form_model.run(**data))

    # Test InvoiceFormModel
    print("\nTest InvoiceFormModel")
    invoice_form_model = InvoiceFormModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/sample-invoice.pdf"
    }
    print(invoice_form_model.run(**data))

    # Test ReceiptFormModel
    print("\nTest ReceiptFormModel")
    receipt_form_model = ReceiptFormModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/receipt.png"
    }
    print(receipt_form_model.run(**data))

    # Test IDDocumentFormModel
    print("\nTest IDDocumentFormModel")
    id_doc_form_model = IDDocumentFormModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/master/curl/form-recognizer/rest-api/identity_documents.png"
    }
    print(id_doc_form_model.run(**data))

    # Test BusinessCardFormModel
    print("\nTest BusinessCardFormModel")
    biz_card_form_model = BusinessCardFormModel()
    data = {
        ArgsType.FILE.value: "https://raw.githubusercontent.com/Azure-Samples/cognitive-services-REST-api-samples/de5e0d8982ab754823c54de47a47e8e499351523/curl/form-recognizer/rest-api/business_card.jpg"
    }
    print(biz_card_form_model.run(**data))