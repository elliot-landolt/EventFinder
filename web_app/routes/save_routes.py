from flask import Blueprint, session, render_template, current_app

save_routes = Blueprint("save_routes", __name__)

@save_routes.route("/saved")
def saved():
    return render_template("saved.html")


@save_routes.route("/saved/new")
def new():
    return render_template("new_itinerary.html")