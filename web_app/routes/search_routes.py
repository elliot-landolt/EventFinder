from flask import Blueprint, request, render_template

search_routes = Blueprint("search_routes", __name__)

@search_routes.route("/search")
def search():
    print("SEARCH...")
    return render_template("search.html")

@search_routes.route("/result")
def result():
    print("RESULT...")
    return render_template("result.html")

