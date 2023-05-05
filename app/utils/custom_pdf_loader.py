import io
from typing import Any, Dict, List
import pdfplumber
from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class BufferLoader(BaseLoader):
    def __init__(self, file_path_or_blob):
        super().__init__()
        self.file_path_or_blob = file_path_or_blob

    def parse(self, raw, metadata):
        raise NotImplementedError()

    def load(self) -> List[Document]:
        if isinstance(self.file_path_or_blob, str):
            with open(self.file_path_or_blob, "rb") as f:
                raw = f.read()
            metadata = {"source": self.file_path_or_blob}
        else:
            raise NotImplementedError("Blob handling not implemented")

        return self.parse(raw, metadata)


class CustomPDFLoader(BufferLoader):
    def parse(self, raw: bytes, metadata: Dict[str, Any]) -> List[Document]:
        with io.BytesIO(raw) as bytes_io:
            with pdfplumber.open(bytes_io) as pdf:
                pages = []
                for i, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    pages.append(
                        Document(
                            id=f"{metadata['id']}_page_{i}",
                            page_number=i,
                            page_content=text,
                            metadata=metadata,
                        )
                    )
                return pages

    def load(self) -> List[Document]:
        if isinstance(self.file_path_or_blob, str):
            with open(self.file_path_or_blob, "rb") as f:
                raw = f.read()
            # Add 'id' key to the metadata dictionary
            metadata = {"source": self.file_path_or_blob, "id": self.file_path_or_blob}
        else:
            raise NotImplementedError("Blob handling not implemented")

        return self.parse(raw, metadata)
