from flask import Blueprint, request, render_template, flash, redirect, session
from app.geohash import address_sanity_check
from app.database.models.searches import Search
from app.ticketmaster_search import search_events, create_params
from app.database.queries import query_itineraries, add_saved_event

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        request_data = dict(request.form)
        Search.create({
            "query":session['query'],
            "user": session.get('current_user', {}).get('email', 'Guest'),
            "correct":next(iter(request_data))
        })
        if 'no' in request_data:
            flash('Please try again, the more specific the better!', 'warning')
        return render_template("search_form.html", request_data=request_data, query=session['query'].capitalize())
    else:
        return render_template("search_form.html")

@search_routes.route("/result")
def result():
    print("RESULT...")
    return render_template("result.html")

@search_routes.route("/search/sanity", methods=["GET", "POST"])
def sanity():
    if request.method == "POST":
        request_data = dict(request.form)
    else:
        request_data = dict(request.args)

    dest = request_data.get("destination")
    try:
        sanity_check, geohash, bbox, query = address_sanity_check(dest)
        session['query'] = query
        session['geohash'] = geohash
        if bbox == '0,0,0,0':
            flash('Map Unavailable', 'danger')
        return render_template("search_sanity.html",
                               sanity_check=sanity_check,
                               bbox=bbox)
    except Exception as e:
        flash("An Error Occurred. Please try agian.", 'danger')
        print(e)
        return redirect("/search")
    
@search_routes.route("/search/events", methods=['POST'])
def results():
    result_data = dict(request.form)
    if 'itinerary[]' in result_data:
        # this is a modal submission
        itinerary_selection = request.form.getlist('itinerary[]')
        result_data = dict(request.form)
        result = add_saved_event(result_data.get('event_id'), itinerary_selection)
        if result == True:
            flash('Success! Your event was added.', 'success')
        else:
            flash('Oops! Looks like this is already in your itinerary!', 'warning')


    if 'page' not in result_data:
        result_data['page']=0
        params = create_params(result_data, session['geohash'])
    else:
        params=session['params']
        params['page']=result_data['page']
    
    if session.get('current_user'):
        itinerary_list = query_itineraries(session['current_user']['email'])
    else:
        # Handle the case where there is no current user
        itinerary_list = []
    session['params']=params
    
    result = search_events(params)
    if result is not None:
        return render_template('results.html', 
                            event_objects=result[0],
                            page_data=result[1],
                            itineraries=itinerary_list,
                            params=params)
    else:
        return render_template('results.html',
                            params=params)