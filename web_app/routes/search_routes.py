from flask import Blueprint, request, render_template, flash, redirect, session
from app.geohash import address_sanity_check
from app.database.models.searches import Search

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        request_data = dict(request.form)
        print(request_data)
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