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


@app.route("/clubs")
def clubs():
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    return render_template("clubs.html", clubs=clubs, access=access)


@app.route("/edit_club/<club_id>", methods=["GET", "POST"])
def edit_club(club_id):
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    club = mongo.db.clubs.find_one({"_id": ObjectId(club_id)})

    if request.method == "POST":
        submit = {
            "club_name": request.form.get("club_name"),
            "club_number": request.form.get("club_number"),
            "club_website": request.form.get("club_website"),
            "club_status": request.form.get("club_status")
        }
        mongo.db.clubs.update({"_id": ObjectId(club_id)}, submit)
        flash("Club information successfully updated")
        return redirect(url_for("clubs"))

    return render_template("edit_club.html", club=club, access=access)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        if request.form.get("is_official") == "is_official" or request.form.get("is_administrator") == "is_administrator":
            access = "full"
        else:
            access = "standard"

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "club": request.form.get("club"),
            "is_athlete": request.form.get("is_athlete"),
            "is_coach": request.form.get("is_coach"),
            "is_manager": request.form.get("is_manager"),
            "is_official": request.form.get("is_official"),
            "is_administrator": request.form.get("is_administrator"),
            "access": access
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Great, you are now registered!")
        return redirect(url_for("profile", username=session["user"]))

    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    return render_template("register.html", clubs=clubs)


@app.route("/login", methods=["GET", "POST"])
def login():
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

    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    return render_template("login.html", clubs=clubs)


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    clubs = mongo.db.clubs.find({"club_status": "active"}).sort("club_name")
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    club = mongo.db.users.find_one(
        {"username": session["user"]})["club"]
    is_athlete = mongo.db.users.find_one(
        {"username": session["user"]})["is_athlete"]
    is_coach = mongo.db.users.find_one(
        {"username": session["user"]})["is_coach"]
    is_manager = mongo.db.users.find_one(
        {"username": session["user"]})["is_manager"]
    is_official = mongo.db.users.find_one(
        {"username": session["user"]})["is_official"]
    is_administrator = mongo.db.users.find_one(
        {"username": session["user"]})["is_administrator"]
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]

    if session["user"]:
        return render_template(
            "profile.html",
            clubs=clubs,
            username=username,
            is_athlete=is_athlete,
            is_coach=is_coach,
            is_manager=is_manager,
            is_official=is_official,
            is_administrator=is_administrator,
            club=club,
            access=access
        )

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/matches_display")
def matches_display():
    matches = mongo.db.matches.find().sort("match_date", -1)
    return render_template("matches_display.html", matches=matches)


@app.route("/matches")
def matches():
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    matches = mongo.db.matches.find().sort("match_date", -1)
    return render_template("matches.html", matches=matches, access=access)


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
        # Day of month conversion
        if request.form.get("match_monthday") == "1st":
            numeric_monthday = "-01"
        elif request.form.get("match_monthday") == "2nd":
            numeric_monthday = "-02"
        elif request.form.get("match_monthday") == "3rd":
            numeric_monthday = "-03"
        elif request.form.get("match_monthday") == "4th":
            numeric_monthday = "-04"
        elif request.form.get("match_monthday") == "5th":
            numeric_monthday = "-05"
        elif request.form.get("match_monthday") == "6th":
            numeric_monthday = "-06"
        elif request.form.get("match_monthday") == "7th":
            numeric_monthday = "-07"
        elif request.form.get("match_monthday") == "8th":
            numeric_monthday = "-08"
        elif request.form.get("match_monthday") == "9th":
            numeric_monthday = "-09"
        elif request.form.get("match_monthday") == "10th":
            numeric_monthday = "-10"
        elif request.form.get("match_monthday") == "11th":
            numeric_monthday = "-11"
        elif request.form.get("match_monthday") == "12th":
            numeric_monthday = "-12"
        elif request.form.get("match_monthday") == "13th":
            numeric_monthday = "-13"
        elif request.form.get("match_monthday") == "14th":
            numeric_monthday = "-14"
        elif request.form.get("match_monthday") == "15th":
            numeric_monthday = "-15"
        elif request.form.get("match_monthday") == "16th":
            numeric_monthday = "-16"
        elif request.form.get("match_monthday") == "17th":
            numeric_monthday = "-17"
        elif request.form.get("match_monthday") == "18th":
            numeric_monthday = "-18"
        elif request.form.get("match_monthday") == "19th":
            numeric_monthday = "-19"
        elif request.form.get("match_monthday") == "20th":
            numeric_monthday = "-20"
        elif request.form.get("match_monthday") == "21st":
            numeric_monthday = "-21"
        elif request.form.get("match_monthday") == "22nd":
            numeric_monthday = "-22"
        elif request.form.get("match_monthday") == "23rd":
            numeric_monthday = "-23"
        elif request.form.get("match_monthday") == "24th":
            numeric_monthday = "-24"
        elif request.form.get("match_monthday") == "25th":
            numeric_monthday = "-25"
        elif request.form.get("match_monthday") == "26th":
            numeric_monthday = "-26"
        elif request.form.get("match_monthday") == "27th":
            numeric_monthday = "-27"
        elif request.form.get("match_monthday") == "28th":
            numeric_monthday = "-28"
        elif request.form.get("match_monthday") == "29th":
            numeric_monthday = "-29"
        elif request.form.get("match_monthday") == "30th":
            numeric_monthday = "-30"
        elif request.form.get("match_monthday") == "31st":
            numeric_monthday = "-31"
        # Month conversion
        if request.form.get("match_month") == "January":
            numeric_month = "-01"
        elif request.form.get("match_month") == "February":
            numeric_month = "-02"
        elif request.form.get("match_month") == "March":
            numeric_month = "-03"
        elif request.form.get("match_month") == "April":
            numeric_month = "-04"
        elif request.form.get("match_month") == "May":
            numeric_month = "-05"
        elif request.form.get("match_month") == "June":
            numeric_month = "-06"
        elif request.form.get("match_month") == "July":
            numeric_month = "-07"
        elif request.form.get("match_month") == "August":
            numeric_month = "-08"
        elif request.form.get("match_month") == "September":
            numeric_month = "-09"
        elif request.form.get("match_month") == "October":
            numeric_month = "-10"
        elif request.form.get("match_month") == "November":
            numeric_month = "-11"
        elif request.form.get("match_month") == "December":
            numeric_month = "-12"
        # Date compiler
        match_date = request.form.get("match_season") + numeric_month + numeric_monthday
        match = {
            "match_season": request.form.get("match_season"),
            "match_number": request.form.get("match_number"),
            "match_weekday": request.form.get("match_weekday"),
            "match_monthday": request.form.get("match_monthday"),
            "match_month": request.form.get("match_month"),
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

    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    seasons = mongo.db.seasons.find().sort("season_year")
    weekdays = mongo.db.weekdays.find()
    monthdays = mongo.db.monthdays.find()
    months = mongo.db.months.find()
    venues = mongo.db.venues.find().sort("venue_name", 1)
    return render_template(
        "add_match.html",
        seasons=seasons,
        weekdays=weekdays,
        monthdays=monthdays,
        months=months,
        venues=venues,
        access=access
    )


@app.route("/edit_match/<match_id>", methods=["GET", "POST"])
def edit_match(match_id):
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
        # Day of month conversion
        if request.form.get("match_monthday") == "1st":
            numeric_monthday = "-01"
        elif request.form.get("match_monthday") == "2nd":
            numeric_monthday = "-02"
        elif request.form.get("match_monthday") == "3rd":
            numeric_monthday = "-03"
        elif request.form.get("match_monthday") == "4th":
            numeric_monthday = "-04"
        elif request.form.get("match_monthday") == "5th":
            numeric_monthday = "-05"
        elif request.form.get("match_monthday") == "6th":
            numeric_monthday = "-06"
        elif request.form.get("match_monthday") == "7th":
            numeric_monthday = "-07"
        elif request.form.get("match_monthday") == "8th":
            numeric_monthday = "-08"
        elif request.form.get("match_monthday") == "9th":
            numeric_monthday = "-09"
        elif request.form.get("match_monthday") == "10th":
            numeric_monthday = "-10"
        elif request.form.get("match_monthday") == "11th":
            numeric_monthday = "-11"
        elif request.form.get("match_monthday") == "12th":
            numeric_monthday = "-12"
        elif request.form.get("match_monthday") == "13th":
            numeric_monthday = "-13"
        elif request.form.get("match_monthday") == "14th":
            numeric_monthday = "-14"
        elif request.form.get("match_monthday") == "15th":
            numeric_monthday = "-15"
        elif request.form.get("match_monthday") == "16th":
            numeric_monthday = "-16"
        elif request.form.get("match_monthday") == "17th":
            numeric_monthday = "-17"
        elif request.form.get("match_monthday") == "18th":
            numeric_monthday = "-18"
        elif request.form.get("match_monthday") == "19th":
            numeric_monthday = "-19"
        elif request.form.get("match_monthday") == "20th":
            numeric_monthday = "-20"
        elif request.form.get("match_monthday") == "21st":
            numeric_monthday = "-21"
        elif request.form.get("match_monthday") == "22nd":
            numeric_monthday = "-22"
        elif request.form.get("match_monthday") == "23rd":
            numeric_monthday = "-23"
        elif request.form.get("match_monthday") == "24th":
            numeric_monthday = "-24"
        elif request.form.get("match_monthday") == "25th":
            numeric_monthday = "-25"
        elif request.form.get("match_monthday") == "26th":
            numeric_monthday = "-26"
        elif request.form.get("match_monthday") == "27th":
            numeric_monthday = "-27"
        elif request.form.get("match_monthday") == "28th":
            numeric_monthday = "-28"
        elif request.form.get("match_monthday") == "29th":
            numeric_monthday = "-29"
        elif request.form.get("match_monthday") == "30th":
            numeric_monthday = "-30"
        elif request.form.get("match_monthday") == "31st":
            numeric_monthday = "-31"
        # Month conversion
        if request.form.get("match_month") == "January":
            numeric_month = "-01"
        elif request.form.get("match_month") == "February":
            numeric_month = "-02"
        elif request.form.get("match_month") == "March":
            numeric_month = "-03"
        elif request.form.get("match_month") == "April":
            numeric_month = "-04"
        elif request.form.get("match_month") == "May":
            numeric_month = "-05"
        elif request.form.get("match_month") == "June":
            numeric_month = "-06"
        elif request.form.get("match_month") == "July":
            numeric_month = "-07"
        elif request.form.get("match_month") == "August":
            numeric_month = "-08"
        elif request.form.get("match_month") == "September":
            numeric_month = "-09"
        elif request.form.get("match_month") == "October":
            numeric_month = "-10"
        elif request.form.get("match_month") == "November":
            numeric_month = "-11"
        elif request.form.get("match_month") == "December":
            numeric_month = "-12"
        # Date compiler
        match_date = request.form.get("match_season") + numeric_month + numeric_monthday
        submit = {
            "match_season": request.form.get("match_season"),
            "match_number": request.form.get("match_number"),
            "match_weekday": request.form.get("match_weekday"),
            "match_monthday": request.form.get("match_monthday"),
            "match_month": request.form.get("match_month"),
            "match_date": match_date,
            "match_venue": request.form.get("match_venue"),
            "venue_address": venue_address,
            "venue_postcode": venue_postcode,
            "venue_latitude": venue_latitude,
            "venue_longitude": venue_longitude
        }
        mongo.db.matches.update({"_id": ObjectId(match_id)}, submit)
        flash("Match successfully updated")
        return redirect(url_for("matches"))

    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    match = mongo.db.matches.find_one({"_id": ObjectId(match_id)})
    seasons = mongo.db.seasons.find().sort("season_year")
    weekdays = mongo.db.weekdays.find()
    monthdays = mongo.db.monthdays.find()
    months = mongo.db.months.find()
    venues = mongo.db.venues.find().sort("venue_name", 1)
    return render_template(
        "edit_match.html",
        match=match,
        seasons=seasons,
        weekdays=weekdays,
        monthdays=monthdays,
        months=months,
        venues=venues,
        access=access
    )


@app.route("/delete_match/<match_id>")
def delete_match(match_id):
    mongo.db.matches.remove({"_id": ObjectId(match_id)})
    flash("Match successfully deleted")
    return redirect(url_for("matches"))


@app.route("/add_timetable", methods=["GET", "POST"])
def add_timetable():
    if request.method == "POST":
        # Time compiler
        event_time = request.form.get("event_hour") + ":" + request.form.get("event_minute")
        # Categories array compiler
        event_categories = [
            request.form.get("M35"),
            request.form.get("M35A"),
            request.form.get("M35B"),
            request.form.get("M50"),
            request.form.get("M60"),
            request.form.get("MNS"),
            request.form.get("W35"),
            request.form.get("W35A"),
            request.form.get("W35B"),
            request.form.get("W50"),
            request.form.get("W60"),
            request.form.get("WNS"),
        ]
        # Remove null values
        event_categories = list(filter(None,event_categories))
        timetable_event = {
            "match_season": request.form.get("match_season"),
            "match_number": request.form.get("match_number"),
            "event_time": event_time,
            "event_name": request.form.get("event_name"),
            "event_categories": event_categories
        }
        mongo.db.timetable_events.insert_one(timetable_event)
        flash("Event successfully added")
        return redirect(url_for("add_timetable"))

    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    seasons = mongo.db.seasons.find().sort("season_year")
    timetable_hours = mongo.db.timetable_hours.find().sort("hour")
    timetable_minutes = mongo.db.timetable_minutes.find().sort("minute")
    events = mongo.db.events.find().sort("event_name")
    return render_template(
        "add_timetable.html",
        seasons=seasons,
        timetable_hours=timetable_hours,
        timetable_minutes=timetable_minutes,
        events=events,
        access=access
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
