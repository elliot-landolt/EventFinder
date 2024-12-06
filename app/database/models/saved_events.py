from app.database.db import BaseModel

class Login(BaseModel):
    SHEET_NAME = 'saved_events'
    COLUMNS = ['itinerary','event_id','title','location','date']