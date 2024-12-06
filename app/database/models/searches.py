from app.database.db import BaseModel

class Search(BaseModel):
    SHEET_NAME = 'searches'
    COLUMNS = ['query', 'user', 'correct']