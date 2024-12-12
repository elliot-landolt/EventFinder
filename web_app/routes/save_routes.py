from flask import Blueprint, session, render_template, current_app, request, flash
from app.database.models.itinerary import Itinerary
from app.database.queries import query_itineraries, get_events

save_routes = Blueprint("save_routes", __name__)

@save_routes.route("/saved", methods=['POST', 'GET'])
def saved():
    if request.method == 'POST':
        request_data = dict(request.form)
        Itinerary.create({
            "title":request_data.get('title', '').strip(),
            "user_id":session['current_user']['email'],
            "description":request_data.get('description', '').strip()
        })
        flash('Itinerary Added!', 'success')
    
    itineraries = query_itineraries(session['current_user']['email'])

    return render_template("saved.html", itineraries=itineraries)


@save_routes.route("/saved/new")
def new():
    return render_template("new_itinerary.html")

@save_routes.route("/saved/view_itinerary", methods=['POST'])
def view():
    if request.method == 'POST':
        id = dict(request.form)['itinerary_id']
        events = get_events(id)
        itinerary = Itinerary.where(id=int(id))
        print(events)
        return render_template('view_itinerary.html', events=events, itinerary=itinerary[0])