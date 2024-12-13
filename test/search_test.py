from app.ticketmaster_search import create_params, search_events
from datetime import datetime

def test_params():
    form_response = {
        'date':'01-01-2024 to 01-01-2025',
        'range':20,
        'page':0
    }
    geohash = 'dr5rtwccpb'

    expected_result = {
        'startDateTime': '2024-01-01T00:00:00Z',
        'endDateTime': '2025-01-01T00:00:00Z',
        'radius': 20,
        'geoPoint': 'dr5rtwccp',
        'page': 0
    }

    params = create_params(form_response, geohash)
    assert params == expected_result

def test_search_connection():
    today = datetime.now().strftime('%m-%d-%Y')
    params = create_params({
        'date':'01-01-2025',
        'range':'24',
        'page':'0'
    }, 'dr5rtwccpb')
    events, data = search_events(params)
    assert len(events) > 1