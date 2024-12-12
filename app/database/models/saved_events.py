from app.database.db import BaseModel

class Saved_Event(BaseModel):
    SHEET_NAME = 'saved_events'
    COLUMNS = ['itinerary','event_id','title','location','date', 'time', 'url', 'image']