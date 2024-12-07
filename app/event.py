class Event:
    def __init__(self, event_id, name, description, location, dates, url, image):
        self.event_id = event_id
        self.name = name
        self.description = description
        self.location = location
        self.dates = dates
        self.url = url
        self.image = image

    def __repr__(self):
        return (f"Event(id={self.event_id}, \n name={self.name}, \n description={self.description}, "
                f"location={self.location}, \n dates={self.dates}, \n url={self.url}, "
                f" \n date_time={self.image})")