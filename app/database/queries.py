from app.database.models.itinerary import Itinerary
from app.database.models.saved_events import Saved_Event
from app.ticketmaster_key import TICKETMASTER_KEY
import requests
from datetime import datetime

def query_itineraries(user_id):
    itineraries = Itinerary.where(user_id=user_id)
    return itineraries

def add_saved_event(event_id, itinerary_ids):
    # get event data
    url = f'https://app.ticketmaster.com/discovery/v2/events/{event_id}.json'
    params = {
        'apikey':TICKETMASTER_KEY
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            event = response.json()
    
    except Exception as e:
        print(e)
    
    
    # add to DB

    for itinerary_id in itinerary_ids:
        print(itinerary_id)
        exists =  Saved_Event.where(event_id=event_id, itinerary=int(itinerary_id))
        if len(exists) == 0:
            local_date = datetime.strptime(event['dates']['start']['localDate'], "%Y-%m-%d")
            event['dates']['start']['formattedDate'] = local_date.strftime("%b %d, %Y")  # Example: December 7, 2024

            if event['dates']['start']['noSpecificTime'] == True:
                local_time = None
                event['dates']['start']['formattedTime'] = 'None'
            else:
                local_time = datetime.strptime(event['dates']['start']['localTime'], "%H:%M:%S")
                event['dates']['start']['formattedTime'] = local_time.strftime("%I:%M %p")  # Example: 06:30 PM
            
            Saved_Event.create({
                'itinerary':itinerary_id,
                'event_id':event_id,
                'title':event['name'],
                'location':event['_embedded']['venues'][0]['name'],
                'date':event['dates']['start']['formattedTime'],
                'time':event['dates']['start']['formattedDate']
            })
            return True
        else:
            return False

if __name__ == "__main__":
    add_saved_event('rZ7HnEZ1AKrbCK',[1,2])
    events = Saved_Event.where(event_id='rZ7HnEZ1AKrbCK', itinerary=3)
    print(events)
