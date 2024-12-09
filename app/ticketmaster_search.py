import requests
from datetime import datetime, timedelta
from app.ticketmaster_key import TICKETMASTER_KEY
from app.event import Event


def format_to_iso(date_string):
    return datetime.strptime(date_string, "%m-%d-%Y").isoformat() + "Z"

def create_params(form_response, geohash):
    # Initialize the params dictionary with common keys
    date = form_response['date']
    range = form_response['range']

    date_parts = date.split('to')

    # Handle the single date or date range
    if len(date_parts) == 1:
        # Only a single date is provided
        startDateTime = format_to_iso(date_parts[0].strip())

        start_date_obj = datetime.strptime(date_parts[0].strip(), "%m-%d-%Y")
        end_date_obj = start_date_obj + timedelta(days=1)
        
        endDateTime = format_to_iso(end_date_obj.strftime("%m-%d-%Y"))
    else:
        # A date range is provided
        startDateTime = format_to_iso(date_parts[0].strip())
        endDateTime = format_to_iso(date_parts[1].strip())

    params = {
        'startDateTime': startDateTime,
        'endDateTime': endDateTime,
        'radius': int(range),
        'geoPoint': geohash[:9],
        'page':form_response['page']
    }
    
    # Dynamically add optional keys if they have values
    if 'source' in form_response and form_response["source"] is not None:
        params['source'] = 'ticketmaster'
    if 'tba' in form_response and form_response['tba'] is not None:
        params['tba'] = 'yes'
    if 'family' in form_response and form_response['family'] is not None:
        params['family'] = 'only'
    return params

def search_events(params):
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    
    params['apikey'] = TICKETMASTER_KEY
    params['size'] = 20
    params['sort'] = 'date,asc'

    try:
        # Send the GET request
        response = requests.get(url, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            json_data = response.json()
            event_objects = []
            if '_embedded' in json_data and 'events' in json_data['_embedded']:
                events = json_data['_embedded']['events']
                page_data = (json_data['page']['totalPages'], int(params['page']))

                for event in events:
                    if event['dates']['status']['code'] == 'onsale':
                        description = event['description'] if 'description' in event else None
                        event_objects.append(Event(
                            event['id'], 
                            event['name'], 
                            description,
                            event['_embedded']['venues'][0]['name'],
                            event['dates'],
                            event['url'],
                            event['images'][2])
                        )
                        local_date = datetime.strptime(event['dates']['start']['localDate'], "%Y-%m-%d")
                        event['dates']['start']['formattedDate'] = local_date.strftime("%b %d, %Y")  # Example: December 7, 2024

                        if event['dates']['start']['noSpecificTime'] == True:
                            local_time = None
                            event['dates']['start']['formattedTime'] = 'None'
                        else:
                            local_time = datetime.strptime(event['dates']['start']['localTime'], "%H:%M:%S")
                            event['dates']['start']['formattedTime'] = local_time.strftime("%I:%M %p")  # Example: 06:30 PM
                return event_objects, page_data
            else:
                print("No events found.")
        else:
            print(response.status_code)
    except requests.exceptions.RequestException as e:
        # Handle any request errors
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    params = create_params({
        'date':'12-08-2024',
        'range':'24',
        'page':'0'
    }, 'dr5rtwccpb')
    event_objects, page_data = search_events(params)
    for event in event_objects:
        print(event.event_id)
