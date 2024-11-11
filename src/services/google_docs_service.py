from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils.logger import Logger


class GoogleDocsService:
    def __init__(self, credentials_path):
        self.logger = Logger(__name__)
        try:
            self.credentials = service_account.Credentials.from_service_account_file(
                credentials_path,
                scopes=["https://www.googleapis.com/auth/documents.readonly"],
            )
            self.service = build("docs", "v1", credentials=self.credentials)
        except Exception as e:
            self.logger.error(f"Failed to initialize Google Docs service: {str(e)}")
            raise

    def get_document(self, doc_id):
        try:
            document = self.service.documents().get(documentId=doc_id).execute()
            return self._extract_text(document)
        except HttpError as e:
            self.logger.error(f"Failed to fetch document {doc_id}: {str(e)}")
            raise

    def _extract_text(self, document):
        text_content = []
        for element in document.get("body").get("content"):
            if "paragraph" in element:
                paragraph = element.get("paragraph")
                for elem in paragraph.get("elements"):
                    if "textRun" in elem:
                        text_content.append(elem.get("textRun").get("content"))
        return "".join(text_content)
