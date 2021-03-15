import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)


app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/welcome")
def welcome():
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    return render_template("welcome.html", clubs=clubs)


@app.route("/register", methods=["GET", "POST"])
def register():
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "club": request.form.get("club"),
            "is_athlete": request.form.get("is_athlete"),
            "is_coach": request.form.get("is_coach"),
            "is_manager": request.form.get("is_manager"),
            "is_official": request.form.get("is_official"),
            "is_administrator": request.form.get("is_administrator")
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Great, you are now registered!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html", clubs=clubs)


@app.route("/login", methods=["GET", "POST"])
def login():
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                    session["user"] = request.form.get("username").lower()
                    flash("Welcome, {}".format(
                        request.form.get("username")))
                    return redirect(url_for(
                        "profile", username=session["user"]))
            else:
                flash("One or both of those aren't quite right")
                return redirect(url_for("login"))

        else:
            flash("One or both of those aren't quite right")
            return redirect(url_for("login"))

    return render_template("login.html", clubs=clubs)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template(
            "profile.html", clubs=clubs, username=username)
    
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/matches")
def matches():
    matches = mongo.db.matches.find().sort("match_date", -1)
    return render_template("matches.html", matches=matches)


@app.route("/add_match", methods=["GET", "POST"])
def add_match():
    if request.method == "POST":
        # Additional information for venues
        if request.form.get("match_venue") == "Tilsley Park":
            venue_address = "Dunmore Road, Abingdon, Oxfordshire"
            venue_postcode = "OX14 1PU"
            venue_latitude = 51.68851413424184
            venue_longitude = -1.2844304304305583
        elif request.form.get("match_venue") == "Horspath Athletics and Sports Ground":
            venue_address = "Horspath Road, Oxford, Oxfordshire"
            venue_postcode = "OX4 2RR"
            venue_latitude = 51.7375972575029
            venue_longitude = -1.1871759304287552
        elif request.form.get("match_venue") == "Palmer Park Stadium":
            venue_address = "Wokingham Road, Earley, Reading, Berkshire"
            venue_postcode = "RG6 1LF"
            venue_latitude = 51.451455101790785
            venue_longitude = -0.9376482397139002
        elif request.form.get("match_venue") == "Swindon Athletics Track":
            venue_address = "75 Shrivenham Road, Swindon, Wiltshire"
            venue_postcode = "SN1 2QA"
            venue_latitude = 51.56697977134897
            venue_longitude = -1.76940873043505
        elif request.form.get("match_venue") == "Crookham Common Athletics Track":
            venue_address = "Thatcham, Berkshire"
            venue_postcode = "RG19 8ET"
            venue_latitude = 51.380717539827984
            venue_longitude = -1.2511990592783035
        elif request.form.get("match_venue") == "John Nike Stadium":
            venue_address = "2 South Hill Road, Bracknell, Berkshire"
            venue_postcode = "RG12 7NN"
            venue_latitude = 51.400788248114885
            venue_longitude = -0.7499129592775471
        # Date compiler
        match_date = request.form.get("match_season") + request.form.get("match_month") + request.form.get("match_monthday")
        # Day of month for display compiler
        if request.form.get("match_monthday") == "-01":
            display_monthday = "1st"
        elif request.form.get("match_monthday") == "-02":
            display_monthday = "2nd"
        elif request.form.get("match_monthday") == "-03":
            display_monthday = "3rd"
        elif request.form.get("match_monthday") == "-04":
            display_monthday = "4th"
        elif request.form.get("match_monthday") == "-05":
            display_monthday = "5th"
        elif request.form.get("match_monthday") == "-06":
            display_monthday = "6th"
        elif request.form.get("match_monthday") == "-07":
            display_monthday = "7th"
        elif request.form.get("match_monthday") == "-08":
            display_monthday = "8th"
        elif request.form.get("match_monthday") == "-09":
            display_monthday = "9th"
        elif request.form.get("match_monthday") == "-10":
            display_monthday = "10th"
        elif request.form.get("match_monthday") == "-11":
            display_monthday = "11th"
        elif request.form.get("match_monthday") == "-12":
            display_monthday = "12th"
        elif request.form.get("match_monthday") == "-13":
            display_monthday = "13th"
        elif request.form.get("match_monthday") == "-14":
            display_monthday = "14th"
        elif request.form.get("match_monthday") == "-15":
            display_monthday = "15th"
        elif request.form.get("match_monthday") == "-16":
            display_monthday = "16th"
        elif request.form.get("match_monthday") == "-17":
            display_monthday = "17th"
        elif request.form.get("match_monthday") == "-18":
            display_monthday = "18th"
        elif request.form.get("match_monthday") == "-19":
            display_monthday = "19th"
        elif request.form.get("match_monthday") == "-20":
            display_monthday = "20th"
        elif request.form.get("match_monthday") == "-21":
            display_monthday = "21st"
        elif request.form.get("match_monthday") == "-22":
            display_monthday = "22nd"
        elif request.form.get("match_monthday") == "-23":
            display_monthday = "23rd"
        elif request.form.get("match_monthday") == "-24":
            display_monthday = "24th"
        elif request.form.get("match_monthday") == "-25":
            display_monthday = "25th"
        elif request.form.get("match_monthday") == "-26":
            display_monthday = "26th"
        elif request.form.get("match_monthday") == "-27":
            display_monthday = "27th"
        elif request.form.get("match_monthday") == "-28":
            display_monthday = "28th"
        elif request.form.get("match_monthday") == "-29":
            display_monthday = "29th"
        elif request.form.get("match_monthday") == "-30":
            display_monthday = "30th"
        elif request.form.get("match_monthday") == "-31":
            display_monthday = "31st"
        # Month for display compiler
        if request.form.get("match_month") == "-01":
            display_month = "January"
        elif request.form.get("match_month") == "-02":
            display_month = "February"
        elif request.form.get("match_month") == "-03":
            display_month = "March"
        elif request.form.get("match_month") == "-04":
            display_month = "April"
        elif request.form.get("match_month") == "-05":
            display_month = "May"
        elif request.form.get("match_month") == "-06":
            display_month = "June"
        elif request.form.get("match_month") == "-07":
            display_month = "July"
        elif request.form.get("match_month") == "-08":
            display_month = "August"
        elif request.form.get("match_month") == "-09":
            display_month = "September"
        elif request.form.get("match_month") == "-10":
            display_month = "October"
        elif request.form.get("match_month") == "-11":
            display_month = "November"
        elif request.form.get("match_month") == "-12":
            display_month = "December"
        match = {
            "match_season": request.form.get("match_season"),
            "match_number": request.form.get("match_number"),
            "match_weekday": request.form.get("match_weekday"),
            "match_monthday": request.form.get("match_monthday"),
            "display_monthday": display_monthday,
            "match_month": request.form.get("match_month"),
            "display_month": display_month,
            "match_date": match_date,
            "match_venue": request.form.get("match_venue"),
            "venue_address": venue_address,
            "venue_postcode": venue_postcode,
            "venue_latitude": venue_latitude,
            "venue_longitude": venue_longitude
        }
        mongo.db.matches.insert_one(match)
        flash("Match successfully added")
        return redirect(url_for("matches"))

    venues = mongo.db.venues.find().sort("venue_name", 1)
    return render_template("add_match.html", venues=venues)


@app.route("/edit_match/<match_id>", methods=["GET", "POST"])
def edit_match(match_id):
    match = mongo.db.matches.find_one({"_id": ObjectId(match_id)})
    venues = mongo.db.venues.find().sort("venue_name", 1)
    return render_template("edit_match.html", match=match, venues=venues)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
