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
    timetable_events = mongo.db.timetable_events.find().sort("event_time")
    return render_template(
        "matches_display.html",
        matches=matches,
        timetable_events=timetable_events
    )


@app.route("/matches")
def matches():
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    matches = mongo.db.matches.find().sort("match_date", -1)
    timetable_events = mongo.db.timetable_events.find().sort("event_time")
    return render_template(
        "matches.html",
        matches=matches,
        timetable_events=timetable_events,
        access=access
    )


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


@app.route("/add_timetable/<match_id>", methods=["GET", "POST"])
def add_timetable(match_id):
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
        # Time compiler
        event_time01 = request.form.get("event_hour01") + ":" + request.form.get("event_minute01")
        event_time02 = request.form.get("event_hour02") + ":" + request.form.get("event_minute02")
        event_time03 = request.form.get("event_hour03") + ":" + request.form.get("event_minute03")
        event_time04 = request.form.get("event_hour04") + ":" + request.form.get("event_minute04")
        event_time05 = request.form.get("event_hour05") + ":" + request.form.get("event_minute05")
        event_time06 = request.form.get("event_hour06") + ":" + request.form.get("event_minute06")
        event_time07 = request.form.get("event_hour07") + ":" + request.form.get("event_minute07")
        event_time08 = request.form.get("event_hour08") + ":" + request.form.get("event_minute08")
        event_time09 = request.form.get("event_hour09") + ":" + request.form.get("event_minute09")
        event_time10 = request.form.get("event_hour10") + ":" + request.form.get("event_minute10")
        event_time11 = request.form.get("event_hour11") + ":" + request.form.get("event_minute11")
        event_time12 = request.form.get("event_hour12") + ":" + request.form.get("event_minute12")
        event_time13 = request.form.get("event_hour13") + ":" + request.form.get("event_minute13")
        event_time14 = request.form.get("event_hour14") + ":" + request.form.get("event_minute14")
        event_time15 = request.form.get("event_hour15") + ":" + request.form.get("event_minute15")
        event_time16 = request.form.get("event_hour16") + ":" + request.form.get("event_minute16")
        event_time17 = request.form.get("event_hour17") + ":" + request.form.get("event_minute17")
        event_time18 = request.form.get("event_hour18") + ":" + request.form.get("event_minute18")
        # Categories array compiler
        event_categories01 = [
            request.form.get("M3501"),
            request.form.get("M35A01"),
            request.form.get("M35B01"),
            request.form.get("M5001"),
            request.form.get("M6001"),
            request.form.get("MNS01"),
            request.form.get("W3501"),
            request.form.get("W35A01"),
            request.form.get("W35B01"),
            request.form.get("W5001"),
            request.form.get("W6001"),
            request.form.get("WNS01")
        ]
        event_categories02 = [
            request.form.get("M3502"),
            request.form.get("M35A02"),
            request.form.get("M35B02"),
            request.form.get("M5002"),
            request.form.get("M6002"),
            request.form.get("MNS02"),
            request.form.get("W3502"),
            request.form.get("W35A02"),
            request.form.get("W35B02"),
            request.form.get("W5002"),
            request.form.get("W6002"),
            request.form.get("WNS02")
        ]
        event_categories03 = [
            request.form.get("M3503"),
            request.form.get("M35A03"),
            request.form.get("M35B03"),
            request.form.get("M5003"),
            request.form.get("M6003"),
            request.form.get("MNS03"),
            request.form.get("W3503"),
            request.form.get("W35A03"),
            request.form.get("W35B03"),
            request.form.get("W5003"),
            request.form.get("W6003"),
            request.form.get("WNS03")
        ]
        event_categories04 = [
            request.form.get("M3504"),
            request.form.get("M35A04"),
            request.form.get("M35B04"),
            request.form.get("M5004"),
            request.form.get("M6004"),
            request.form.get("MNS04"),
            request.form.get("W3504"),
            request.form.get("W35A04"),
            request.form.get("W35B04"),
            request.form.get("W5004"),
            request.form.get("W6004"),
            request.form.get("WNS04")
        ]
        event_categories05 = [
            request.form.get("M3505"),
            request.form.get("M35A05"),
            request.form.get("M35B05"),
            request.form.get("M5005"),
            request.form.get("M6005"),
            request.form.get("MNS05"),
            request.form.get("W3505"),
            request.form.get("W35A05"),
            request.form.get("W35B05"),
            request.form.get("W5005"),
            request.form.get("W6005"),
            request.form.get("WNS05")
        ]
        event_categories06 = [
            request.form.get("M3506"),
            request.form.get("M35A06"),
            request.form.get("M35B06"),
            request.form.get("M5006"),
            request.form.get("M6006"),
            request.form.get("MNS06"),
            request.form.get("W3506"),
            request.form.get("W35A06"),
            request.form.get("W35B06"),
            request.form.get("W5006"),
            request.form.get("W6006"),
            request.form.get("WNS06")
        ]
        event_categories07 = [
            request.form.get("M3507"),
            request.form.get("M35A07"),
            request.form.get("M35B07"),
            request.form.get("M5007"),
            request.form.get("M6007"),
            request.form.get("MNS07"),
            request.form.get("W3507"),
            request.form.get("W35A07"),
            request.form.get("W35B07"),
            request.form.get("W5007"),
            request.form.get("W6007"),
            request.form.get("WNS07")
        ]
        event_categories08 = [
            request.form.get("M3508"),
            request.form.get("M35A08"),
            request.form.get("M35B08"),
            request.form.get("M5008"),
            request.form.get("M6008"),
            request.form.get("MNS08"),
            request.form.get("W3508"),
            request.form.get("W35A08"),
            request.form.get("W35B08"),
            request.form.get("W5008"),
            request.form.get("W6008"),
            request.form.get("WNS08")
        ]
        event_categories09 = [
            request.form.get("M3509"),
            request.form.get("M35A09"),
            request.form.get("M35B09"),
            request.form.get("M5009"),
            request.form.get("M6009"),
            request.form.get("MNS09"),
            request.form.get("W3509"),
            request.form.get("W35A09"),
            request.form.get("W35B09"),
            request.form.get("W5009"),
            request.form.get("W6009"),
            request.form.get("WNS09")
        ]
        event_categories10 = [
            request.form.get("M3510"),
            request.form.get("M35A10"),
            request.form.get("M35B10"),
            request.form.get("M5010"),
            request.form.get("M6010"),
            request.form.get("MNS10"),
            request.form.get("W3510"),
            request.form.get("W35A10"),
            request.form.get("W35B10"),
            request.form.get("W5010"),
            request.form.get("W6010"),
            request.form.get("WNS10")
        ]
        event_categories11 = [
            request.form.get("M3511"),
            request.form.get("M35A11"),
            request.form.get("M35B11"),
            request.form.get("M5011"),
            request.form.get("M6011"),
            request.form.get("MNS11"),
            request.form.get("W3511"),
            request.form.get("W35A11"),
            request.form.get("W35B11"),
            request.form.get("W5011"),
            request.form.get("W6011"),
            request.form.get("WNS11")
        ]
        event_categories12 = [
            request.form.get("M3512"),
            request.form.get("M35A12"),
            request.form.get("M35B12"),
            request.form.get("M5012"),
            request.form.get("M6012"),
            request.form.get("MNS12"),
            request.form.get("W3512"),
            request.form.get("W35A12"),
            request.form.get("W35B12"),
            request.form.get("W5012"),
            request.form.get("W6012"),
            request.form.get("WNS12")
        ]
        event_categories13 = [
            request.form.get("M3513"),
            request.form.get("M35A13"),
            request.form.get("M35B13"),
            request.form.get("M5013"),
            request.form.get("M6013"),
            request.form.get("MNS13"),
            request.form.get("W3513"),
            request.form.get("W35A13"),
            request.form.get("W35B13"),
            request.form.get("W5013"),
            request.form.get("W6013"),
            request.form.get("WNS13")
        ]
        event_categories14 = [
            request.form.get("M3514"),
            request.form.get("M35A14"),
            request.form.get("M35B14"),
            request.form.get("M5014"),
            request.form.get("M6014"),
            request.form.get("MNS14"),
            request.form.get("W3514"),
            request.form.get("W35A14"),
            request.form.get("W35B14"),
            request.form.get("W5014"),
            request.form.get("W6014"),
            request.form.get("WNS14")
        ]
        event_categories15 = [
            request.form.get("M3515"),
            request.form.get("M35A15"),
            request.form.get("M35B15"),
            request.form.get("M5015"),
            request.form.get("M6015"),
            request.form.get("MNS15"),
            request.form.get("W3515"),
            request.form.get("W35A15"),
            request.form.get("W35B15"),
            request.form.get("W5015"),
            request.form.get("W6015"),
            request.form.get("WNS15")
        ]
        event_categories16 = [
            request.form.get("M3516"),
            request.form.get("M35A16"),
            request.form.get("M35B16"),
            request.form.get("M5016"),
            request.form.get("M6016"),
            request.form.get("MNS16"),
            request.form.get("W3516"),
            request.form.get("W35A16"),
            request.form.get("W35B16"),
            request.form.get("W5016"),
            request.form.get("W6016"),
            request.form.get("WNS16")
        ]
        event_categories17 = [
            request.form.get("M3517"),
            request.form.get("M35A17"),
            request.form.get("M35B17"),
            request.form.get("M5017"),
            request.form.get("M6017"),
            request.form.get("MNS17"),
            request.form.get("W3517"),
            request.form.get("W35A17"),
            request.form.get("W35B17"),
            request.form.get("W5017"),
            request.form.get("W6017"),
            request.form.get("WNS17")
        ]
        event_categories18 = [
            request.form.get("M3518"),
            request.form.get("M35A18"),
            request.form.get("M35B18"),
            request.form.get("M5018"),
            request.form.get("M6018"),
            request.form.get("MNS18"),
            request.form.get("W3518"),
            request.form.get("W35A18"),
            request.form.get("W35B18"),
            request.form.get("W5018"),
            request.form.get("W6018"),
            request.form.get("WNS18")
        ]
        # Remove null values
        event_categories01 = list(filter(None, event_categories01))
        event_categories02 = list(filter(None, event_categories02))
        event_categories03 = list(filter(None, event_categories03))
        event_categories04 = list(filter(None, event_categories04))
        event_categories05 = list(filter(None, event_categories05))
        event_categories06 = list(filter(None, event_categories06))
        event_categories07 = list(filter(None, event_categories07))
        event_categories08 = list(filter(None, event_categories08))
        event_categories09 = list(filter(None, event_categories09))
        event_categories10 = list(filter(None, event_categories10))
        event_categories11 = list(filter(None, event_categories11))
        event_categories12 = list(filter(None, event_categories12))
        event_categories13 = list(filter(None, event_categories13))
        event_categories14 = list(filter(None, event_categories14))
        event_categories15 = list(filter(None, event_categories15))
        event_categories16 = list(filter(None, event_categories16))
        event_categories17 = list(filter(None, event_categories17))
        event_categories18 = list(filter(None, event_categories18))
        # Match event dictionary compiler
        match_event01 = {
            "event_time": event_time01,
            "event_name": request.form.get("event_name01"),
            "event_categories": event_categories01
        }
        match_event02 = {
            "event_time": event_time02,
            "event_name": request.form.get("event_name02"),
            "event_categories": event_categories02
        }
        match_event03 = {
            "event_time": event_time03,
            "event_name": request.form.get("event_name03"),
            "event_categories": event_categories03
        }
        match_event04 = {
            "event_time": event_time04,
            "event_name": request.form.get("event_name04"),
            "event_categories": event_categories04
        }
        match_event05 = {
            "event_time": event_time05,
            "event_name": request.form.get("event_name05"),
            "event_categories": event_categories05
        }
        match_event06 = {
            "event_time": event_time06,
            "event_name": request.form.get("event_name06"),
            "event_categories": event_categories06
        }
        match_event07 = {
            "event_time": event_time07,
            "event_name": request.form.get("event_name07"),
            "event_categories": event_categories07
        }
        match_event08 = {
            "event_time": event_time08,
            "event_name": request.form.get("event_name08"),
            "event_categories": event_categories08
        }
        match_event09 = {
            "event_time": event_time09,
            "event_name": request.form.get("event_name09"),
            "event_categories": event_categories09
        }
        match_event10 = {
            "event_time": event_time10,
            "event_name": request.form.get("event_name10"),
            "event_categories": event_categories10
        }
        match_event11 = {
            "event_time": event_time11,
            "event_name": request.form.get("event_name11"),
            "event_categories": event_categories11
        }
        match_event12 = {
            "event_time": event_time12,
            "event_name": request.form.get("event_name12"),
            "event_categories": event_categories12
        }
        match_event13 = {
            "event_time": event_time13,
            "event_name": request.form.get("event_name13"),
            "event_categories": event_categories13
        }
        match_event14 = {
            "event_time": event_time14,
            "event_name": request.form.get("event_name14"),
            "event_categories": event_categories04
        }
        match_event15 = {
            "event_time": event_time15,
            "event_name": request.form.get("event_name15"),
            "event_categories": event_categories15
        }
        match_event16 = {
            "event_time": event_time16,
            "event_name": request.form.get("event_name16"),
            "event_categories": event_categories16
        }
        match_event17 = {
            "event_time": event_time17,
            "event_name": request.form.get("event_name17"),
            "event_categories": event_categories17
        }
        match_event18 = {
            "event_time": event_time18,
            "event_name": request.form.get("event_name18"),
            "event_categories": event_categories18
        }
        # Match timetable array compiler
        match_timetable = [
            match_event01,
            match_event02,
            match_event03,
            match_event04,
            match_event05,
            match_event06,
            match_event07,
            match_event08,
            match_event09,
            match_event10,
            match_event11,
            match_event12,
            match_event13,
            match_event14,
            match_event15,
            match_event16,
            match_event17,
            match_event18
        ]
        # Remove null values
        match_timetable = list(filter(None, match_timetable))
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
            "venue_longitude": venue_longitude,
            "match_timetable": match_timetable
        }
        mongo.db.matches.update({"_id": ObjectId(match_id)}, submit)
        flash("Timetable successfully added")
        return redirect(url_for("matches"))

    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    match = mongo.db.matches.find_one({"_id": ObjectId(match_id)})
    seasons = mongo.db.seasons.find().sort("season_year")
    weekdays = mongo.db.weekdays.find()
    monthdays = mongo.db.monthdays.find()
    months = mongo.db.months.find()
    venues = mongo.db.venues.find().sort("venue_name", 1)
    timetable_hours = mongo.db.timetable_hours.find().sort("hour")
    timetable_minutes = mongo.db.timetable_minutes.find().sort("minute")
    events = mongo.db.events.find().sort("event_name")
    return render_template(
        "add_timetable.html",
        match=match,
        seasons=seasons,
        weekdays=weekdays,
        monthdays=monthdays,
        months=months,
        venues=venues,
        timetable_hours=timetable_hours,
        timetable_minutes=timetable_minutes,
        events=events,
        access=access
    )


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
