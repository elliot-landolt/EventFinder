from flask import Blueprint, request, render_template, flash, redirect
from app.geohash import address_sanity_check

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search")
def search():
    print("SEARCH...")
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
        sanity_check, geohash = address_sanity_check(dest)
        print(sanity_check)
        return render_template("search_sanity.html",
                               sanity_check=sanity_check)
    except Exception as e:
        flash("An Error Occurred. Please try agian.")
        print(e)
        return redirect("/search")