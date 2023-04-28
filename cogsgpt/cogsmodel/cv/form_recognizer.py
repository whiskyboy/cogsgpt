from __future__ import annotations

from abc import ABC, abstractmethod
import os
from typing import Any, Dict, List

from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.ai.formrecognizer import AnalyzeResult, AnalyzedDocument, DocumentField, DocumentParagraph, DocumentTable, DocumentKeyValuePair
from azure.core.credentials import AzureKeyCredential

from cogsgpt.cogsmodel import BaseModel
from cogsgpt.schema import ArgsType, FileSource
from cogsgpt.utils import detect_file_source


class FromRecognizerBaseModel(BaseModel, ABC):
    def __init__(self) -> None:
        super().__init__()

        COGS_KEY = os.environ['COGS_KEY']
        COGS_ENDPOINT = os.environ['COGS_ENDPOINT']
        self.document_analysis_client = DocumentAnalysisClient(
            endpoint=COGS_ENDPOINT,
            credential=AzureKeyCredential(COGS_KEY)
        )
        self.model_id = None

    def _parse_paragraphs(self, paragraphs: List[DocumentParagraph]) -> List[Dict]:
        result = []
        for para in paragraphs:
            role = para.role if para.role else "body"
            result.append((role, para.content))
        return result

    def _parse_tables(self, tables: List[DocumentTable]) -> List[Dict]:
        result = []
        for table in tables:
            rc, cc = table.row_count, table.column_count
            _table = [['' for _ in range(cc)] for _ in range(rc)]
            for cell in table.cells:
                _table[cell.row_index][cell.column_index] = cell.content
            result.append(_table)
        return result
    
    def _parse_kv_pairs(self, kv_pairs: List[DocumentKeyValuePair]) -> List[Dict]:
        result = []
        for kv_pair in kv_pairs:
            key = kv_pair.key.content if kv_pair.key else ""
            value = kv_pair.value.content if kv_pair.value else ""
            result.append((key, value))
        return result

    def _parse_document(self, document: AnalyzedDocument) -> Dict:

        def _parse_document_field(field: DocumentField) -> Any:
            if field.value_type == "list":
                return [_parse_document_field(f) for f in field.value]
            elif field.value_type == "dictionary":
                return {k: _parse_document_field(v) for k, v in field.value.items()}
            else:
                return field.value

        return {k: _parse_document_field(v) for k, v in document.fields.items()}

    @abstractmethod
    def _parse_result(self, analyze_result: AnalyzeResult) -> Dict:
        pass

    def _analyze_document(self, document_file: str) -> Dict:
        if self.model_id is None:
            raise ValueError("Model ID is not set")

        document_src = detect_file_source(document_file)
        if document_src == FileSource.LOCAL:
            with open(document_file, "rb") as f:
                poller = self.document_analysis_client.begin_analyze_document(
                    model_id=self.model_id, document=f
                )
        elif document_src == FileSource.REMOTE:
            poller = self.document_analysis_client.begin_analyze_document_from_url(
                model_id=self.model_id, document_url=document_file
            )
        else:
            raise ValueError(f"Invalid document source: {document_file}")

        result = poller.result()
        return self._parse_result(result)

    def run(self, *args, **kwargs) -> str:
        document_file = kwargs[ArgsType.FILE.value]
        return str(self._analyze_document(document_file))


class FormReadModel(FromRecognizerBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-read"

    def _parse_result(self, analyze_result: AnalyzeResult) -> Dict:
        return {
            "content": analyze_result.content
        }


class FormLayoutModel(FromRecognizerBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-layout"

    def _parse_result(self, analyze_result: AnalyzeResult) -> Dict:
        return {
            # "paragraphs": self._parse_paragraphs(analyze_result.paragraphs),
            "tables": self._parse_tables(analyze_result.tables)
        }


class FormKeyValueModel(FromRecognizerBaseModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-document"

    def _parse_result(self, analyze_result: AnalyzeResult) -> Dict:
        return {
            "key_value_pairs": self._parse_kv_pairs(analyze_result.key_value_pairs),
            # "tables": self._parse_tables(analyze_result.tables)
        }


class PrebuiltFormModel(FromRecognizerBaseModel):
    def _parse_result(self, analyze_result: AnalyzeResult) -> Dict:
        return {
            "documents": [
                self._parse_document(doc) for doc in analyze_result.documents 
            ]
        }

class W2TaxFormModel(PrebuiltFormModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-tax.us.w2"


class InvoiceFormModel(PrebuiltFormModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-invoice"


class ReceiptFormModel(PrebuiltFormModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-receipt"


class IDDocumentFormModel(PrebuiltFormModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-idDocument"


class BusinessCardFormModel(PrebuiltFormModel):
    def __init__(self) -> None:
        super().__init__()
        self.model_id = "prebuilt-businessCard"