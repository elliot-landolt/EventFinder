from app.ticketmaster_search import create_params, search_events
from datetime import datetime

def test_search_connection():
    today = datetime.now().strftime('%m-%d-%Y')
    params = create_params({
        'date':'01-01-2025',
        'range':'100',
        'page':'0'
    }, 'dr5rtwccpb')
    events, data = search_events(params)
    print(len(events))

if __name__=='__main__':
    test_search_connection()