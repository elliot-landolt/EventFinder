from app.database.db import BaseModel

class Itinerary(BaseModel):
    SHEET_NAME='itinerary'
    COLUMNS=['title','user_id','description']