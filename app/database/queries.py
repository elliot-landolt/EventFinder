from app.database.models.itinerary import Itinerary
from app.database.models.saved_events import Saved_Event
from app.ticketmaster_key import TICKETMASTER_KEY
import requests
from datetime import datetime

def query_itineraries(user_id):
    itineraries = Itinerary.where(user_id=user_id)
    return itineraries

def get_events(id):
    events = Saved_Event.where(itinerary=int(id))
    return events

def add_saved_event(event_id, itinerary_ids):
    # Get event data
    url = f'https://app.ticketmaster.com/discovery/v2/events/{event_id}.json'
    params = {
        'apikey': TICKETMASTER_KEY
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            event = response.json()
        else:
            print(f"Failed to fetch event: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error fetching event data: {e}")
        return False

    # Add to DB
    added_to_any = False  # Track if any event was successfully added

    for itinerary_id in itinerary_ids:
        exists = Saved_Event.where(event_id=event_id, itinerary=int(itinerary_id))
        if len(exists) == 0:
            # Format date and time
            local_date = datetime.strptime(event['dates']['start']['localDate'], "%Y-%m-%d")
            event['dates']['start']['formattedDate'] = local_date.strftime("%b %d, %Y")  # Example: Dec 7, 2024

            if event['dates']['start']['noSpecificTime']:
                event['dates']['start']['formattedTime'] = 'None'
            else:
                local_time = datetime.strptime(event['dates']['start']['localTime'], "%H:%M:%S")
                event['dates']['start']['formattedTime'] = local_time.strftime("%I:%M %p")  # Example: 06:30 PM

            # Add to database
            Saved_Event.create({
                'itinerary': itinerary_id,
                'event_id': event_id,
                'title': event['name'],
                'location': event['_embedded']['venues'][0]['name'],
                'date': event['dates']['start']['formattedDate'],
                'time': event['dates']['start']['formattedTime'],
                'url': event['url'],
                'image': event['images'][2]['url']
            })
            added_to_any = True
        else:
            print(f"Event already exists in itinerary {itinerary_id}")

    return added_to_any  # Return True if added to any itinerary, otherwise False


if __name__ == "__main__":
    # events = get_events(5)


    add_saved_event('rZ7HnEZ1AKrbCK',[1,2,3])
    events = Saved_Event.where(event_id='rZ7HnEZ1AKrbCK', itinerary=1)
    print(events)
