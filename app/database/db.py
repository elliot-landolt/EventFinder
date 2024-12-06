import os
from dotenv import load_dotenv
from gspread_models.service import SpreadsheetService
from gspread_models.base import BaseModel

load_dotenv()

DEFAULT_FILEPATH = os.path.join(os.path.dirname(__file__),'..','google-credentials.json')
GOOGLE_CREDENTIALS_FILEPATH = os.getenv("GOOGLE_GREDENTIALS_FILEPATH", default=DEFAULT_FILEPATH)

GOOGLE_SHEETS_DOCUMENT_ID = os.getenv('GOOGLE_SHEETS_DOCUMENT_ID', default="OOPS, Please get the correct Document ID")

service = SpreadsheetService(
    credentials_filepath=GOOGLE_CREDENTIALS_FILEPATH,
    document_id=GOOGLE_SHEETS_DOCUMENT_ID
)
BaseModel.service = service