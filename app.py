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

        if request.form.get(
            "is_official") == "is_official" or request.form.get(
                "is_administrator") == "is_administrator":
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
    return render_template(
        "matches_display.html",
        matches=matches
    )


@app.route("/matches")
def matches():
    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    matches = mongo.db.matches.find().sort("match_date", -1)
    return render_template(
        "matches.html",
        matches=matches,
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
        elif request.form.get(
            "match_venue") == "Horspath Athletics and Sports Ground":
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
        elif request.form.get(
            "match_venue") == "Crookham Common Athletics Track":
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
        match_date = request.form.get(
            "match_season") + numeric_month + numeric_monthday
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
        elif request.form.get(
            "match_venue") == "Horspath Athletics and Sports Ground":
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
        elif request.form.get(
            "match_venue") == "Crookham Common Athletics Track":
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
        match_date = request.form.get(
            "match_season") + numeric_month + numeric_monthday
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
        elif request.form.get(
            "match_venue") == "Horspath Athletics and Sports Ground":
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
        elif request.form.get(
            "match_venue") == "Crookham Common Athletics Track":
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
        match_date = request.form.get(
            "match_season") + numeric_month + numeric_monthday
        # Time compiler
        if request.form.get("first_sprint_hour") is None:
            first_sprint_time = None
        elif request.form.get("first_sprint_minute") is None:
            first_sprint_time = None
        else:
            first_sprint_time = request.form.get(
                "first_sprint_hour") + ":" + request.form.get(
                    "first_sprint_minute")
        if request.form.get("second_sprint_hour") is None:
            second_sprint_time = None
        elif request.form.get("second_sprint_minute") is None:
            second_sprint_time = None
        else:
            second_sprint_time = request.form.get(
                "second_sprint_hour") + ":" + request.form.get(
                    "second_sprint_minute")
        if request.form.get("third_sprint_hour") is None:
            third_sprint_time = None
        elif request.form.get("third_sprint_minute") is None:
            third_sprint_time = None
        else:
            third_sprint_time = request.form.get(
                "third_sprint_hour") + ":" + request.form.get(
                    "third_sprint_minute")
        if request.form.get("fourth_sprint_hour") is None:
            fourth_sprint_time = None
        elif request.form.get("fourth_sprint_minute") is None:
            fourth_sprint_time = None
        else:
            fourth_sprint_time = request.form.get(
                "fourth_sprint_hour") + ":" + request.form.get(
                    "fourth_sprint_minute")
        if request.form.get("first_middle_hour") is None:
            first_middle_time = None
        elif request.form.get("first_middle_minute") is None:
            first_middle_time = None
        else:
            first_middle_time = request.form.get(
                "first_middle_hour") + ":" + request.form.get(
                    "first_middle_minute")
        if request.form.get("second_middle_hour") is None:
            second_middle_time = None
        elif request.form.get("second_middle_minute") is None:
            second_middle_time = None
        else:
            second_middle_time = request.form.get(
                "second_middle_hour") + ":" + request.form.get(
                    "second_middle_minute")
        if request.form.get("first_distance_hour") is None:
            first_distance_time = None
        elif request.form.get("first_distance_minute") is None:
            first_distance_time = None
        else:
            first_distance_time = request.form.get(
                "first_distance_hour") + ":" + request.form.get(
                    "first_distance_minute")
        if request.form.get("second_distance_hour") is None:
            second_distance_time = None
        elif request.form.get("second_distance_minute") is None:
            second_distance_time = None
        else:
            second_distance_time = request.form.get(
                "second_distance_hour") + ":" + request.form.get(
                    "second_distance_minute")
        if request.form.get("third_distance_hour") is None:
            third_distance_time = None
        elif request.form.get("third_distance_minute") is None:
            third_distance_time = None
        else:
            third_distance_time = request.form.get(
                "third_distance_hour") + ":" + request.form.get(
                    "third_distance_minute")
        if request.form.get("fourth_distance_hour") is None:
            fourth_distance_time = None
        elif request.form.get("fourth_distance_minute") is None:
            fourth_distance_time = None
        else:
            fourth_distance_time = request.form.get(
                "fourth_distance_hour") + ":" + request.form.get(
                    "fourth_distance_minute")
        if request.form.get("first_relay_hour") is None:
            first_relay_time = None
        elif request.form.get("first_relay_minute") is None:
            first_relay_time = None
        else:
            first_relay_time = request.form.get(
                "first_relay_hour") + ":" + request.form.get(
                    "first_relay_minute")
        if request.form.get("second_relay_hour") is None:
            second_relay_time = None
        elif request.form.get("second_relay_minute") is None:
            second_relay_time = None
        else:
            second_relay_time = request.form.get(
                "second_relay_hour") + ":" + request.form.get(
                    "second_relay_minute")
        if request.form.get("first_jump_hour") is None:
            first_jump_time = None
        elif request.form.get("first_jump_minute") is None:
            first_jump_time = None
        else:
            first_jump_time = request.form.get(
                "first_jump_hour") + ":" + request.form.get(
                    "first_jump_minute")
        if request.form.get("second_jump_hour") is None:
            second_jump_time = None
        elif request.form.get("second_jump_minute") is None:
            second_jump_time = None
        else:
            second_jump_time = request.form.get(
                "second_jump_hour") + ":" + request.form.get(
                    "second_jump_minute")
        if request.form.get("third_jump_hour") is None:
            third_jump_time = None
        elif request.form.get("third_jump_minute") is None:
            third_jump_time = None
        else:
            third_jump_time = request.form.get(
                "third_jump_hour") + ":" + request.form.get(
                    "third_jump_minute")
        if request.form.get("fourth_jump_hour") is None:
            fourth_jump_time = None
        elif request.form.get("fourth_jump_minute") is None:
            fourth_jump_time = None
        else:
            fourth_jump_time = request.form.get(
                "fourth_jump_hour") + ":" + request.form.get(
                    "fourth_jump_minute")
        if request.form.get("first_throw_hour") is None:
            first_throw_time = None
        elif request.form.get("first_throw_minute") is None:
            first_throw_time = None
        else:
            first_throw_time = request.form.get(
                "first_throw_hour") + ":" + request.form.get(
                    "first_throw_minute")
        if request.form.get("second_throw_hour") is None:
            second_throw_time = None
        elif request.form.get("second_throw_minute") is None:
            second_throw_time = None
        else:
            second_throw_time = request.form.get(
                "second_throw_hour") + ":" + request.form.get(
                    "second_throw_minute")
        if request.form.get("third_throw_hour") is None:
            third_throw_time = None
        elif request.form.get("third_throw_minute") is None:
            third_throw_time = None
        else:
            third_throw_time = request.form.get(
                "third_throw_hour") + ":" + request.form.get(
                    "third_throw_minute")
        if request.form.get("fourth_throw_hour") is None:
            fourth_throw_time = None
        elif request.form.get("fourth_throw_minute") is None:
            fourth_throw_time = None
        else:
            fourth_throw_time = request.form.get(
                "fourth_throw_hour") + ":" + request.form.get(
                    "fourth_throw_minute")
        # Categories array compiler
        first_sprint_categories = [
            request.form.get("first_sprint_M35A"),
            request.form.get("first_sprint_M35B"),
            request.form.get("first_sprint_M50"),
            request.form.get("first_sprint_M60"),
            request.form.get("first_sprint_MNS"),
            request.form.get("first_sprint_W35A"),
            request.form.get("first_sprint_W35B"),
            request.form.get("first_sprint_W50"),
            request.form.get("first_sprint_W60"),
            request.form.get("first_sprint_WNS")
        ]
        second_sprint_categories = [
            request.form.get("second_sprint_M35A"),
            request.form.get("second_sprint_M35B"),
            request.form.get("second_sprint_M50"),
            request.form.get("second_sprint_M60"),
            request.form.get("second_sprint_MNS"),
            request.form.get("second_sprint_W35A"),
            request.form.get("second_sprint_W35B"),
            request.form.get("second_sprint_W50"),
            request.form.get("second_sprint_W60"),
            request.form.get("second_sprint_WNS")
        ]
        third_sprint_categories = [
            request.form.get("third_sprint_M35A"),
            request.form.get("third_sprint_M35B"),
            request.form.get("third_sprint_M50"),
            request.form.get("third_sprint_M60"),
            request.form.get("third_sprint_MNS"),
            request.form.get("third_sprint_W35A"),
            request.form.get("third_sprint_W35B"),
            request.form.get("third_sprint_W50"),
            request.form.get("third_sprint_W60"),
            request.form.get("third_sprint_WNS")
        ]
        fourth_sprint_categories = [
            request.form.get("fourth_sprint_M35A"),
            request.form.get("fourth_sprint_M35B"),
            request.form.get("fourth_sprint_M50"),
            request.form.get("fourth_sprint_M60"),
            request.form.get("fourth_sprint_MNS"),
            request.form.get("fourth_sprint_W35A"),
            request.form.get("fourth_sprint_W35B"),
            request.form.get("fourth_sprint_W50"),
            request.form.get("fourth_sprint_W60"),
            request.form.get("fourth_sprint_WNS")
        ]
        first_middle_categories = [
            request.form.get("first_middle_M35A"),
            request.form.get("first_middle_M35B"),
            request.form.get("first_middle_M50"),
            request.form.get("first_middle_M60"),
            request.form.get("first_middle_MNS"),
            request.form.get("first_middle_W35A"),
            request.form.get("first_middle_W35B"),
            request.form.get("first_middle_W50"),
            request.form.get("first_middle_W60"),
            request.form.get("first_middle_WNS")
        ]
        second_middle_categories = [
            request.form.get("second_middle_M35A"),
            request.form.get("second_middle_M35B"),
            request.form.get("second_middle_M50"),
            request.form.get("second_middle_M60"),
            request.form.get("second_middle_MNS"),
            request.form.get("second_middle_W35A"),
            request.form.get("second_middle_W35B"),
            request.form.get("second_middle_W50"),
            request.form.get("second_middle_W60"),
            request.form.get("second_middle_WNS")
        ]
        first_distance_categories = [
            request.form.get("first_distance_M35"),
            request.form.get("first_distance_M35A"),
            request.form.get("first_distance_M35B"),
            request.form.get("first_distance_M50"),
            request.form.get("first_distance_M60"),
            request.form.get("first_distance_MNS"),
            request.form.get("first_distance_W35"),
            request.form.get("first_distance_W35A"),
            request.form.get("first_distance_W35B"),
            request.form.get("first_distance_W50"),
            request.form.get("first_distance_W60"),
            request.form.get("first_distance_WNS")
        ]
        second_distance_categories = [
            request.form.get("second_distance_M35"),
            request.form.get("second_distance_M35A"),
            request.form.get("second_distance_M35B"),
            request.form.get("second_distance_M50"),
            request.form.get("second_distance_M60"),
            request.form.get("second_distance_MNS"),
            request.form.get("second_distance_W35"),
            request.form.get("second_distance_W35A"),
            request.form.get("second_distance_W35B"),
            request.form.get("second_distance_W50"),
            request.form.get("second_distance_W60"),
            request.form.get("second_distance_WNS")
        ]
        third_distance_categories = [
            request.form.get("third_distance_M35"),
            request.form.get("third_distance_M35A"),
            request.form.get("third_distance_M35B"),
            request.form.get("third_distance_M50"),
            request.form.get("third_distance_M60"),
            request.form.get("third_distance_MNS"),
            request.form.get("third_distance_W35"),
            request.form.get("third_distance_W35A"),
            request.form.get("third_distance_W35B"),
            request.form.get("third_distance_W50"),
            request.form.get("third_distance_W60"),
            request.form.get("third_distance_WNS")
        ]
        fourth_distance_categories = [
            request.form.get("fourth_distance_M35"),
            request.form.get("fourth_distance_M35A"),
            request.form.get("fourth_distance_M35B"),
            request.form.get("fourth_distance_M50"),
            request.form.get("fourth_distance_M60"),
            request.form.get("fourth_distance_MNS"),
            request.form.get("fourth_distance_W35"),
            request.form.get("fourth_distance_W35A"),
            request.form.get("fourth_distance_W35B"),
            request.form.get("fourth_distance_W50"),
            request.form.get("fourth_distance_W60"),
            request.form.get("fourth_distance_WNS")
        ]
        first_relay_categories = [
            request.form.get("first_relay_M35"),
            request.form.get("first_relay_W35")
        ]
        second_relay_categories = [
            request.form.get("second_relay_M35"),
            request.form.get("second_relay_W35")
        ]
        first_jump_categories = [
            request.form.get("first_jump_M35"),
            request.form.get("first_jump_M50"),
            request.form.get("first_jump_M60"),
            request.form.get("first_jump_MNS"),
            request.form.get("first_jump_W35"),
            request.form.get("first_jump_W50"),
            request.form.get("first_jump_W60"),
            request.form.get("first_jump_WNS")
        ]
        second_jump_categories = [
            request.form.get("second_jump_M35"),
            request.form.get("second_jump_M50"),
            request.form.get("second_jump_M60"),
            request.form.get("second_jump_MNS"),
            request.form.get("second_jump_W35"),
            request.form.get("second_jump_W50"),
            request.form.get("second_jump_W60"),
            request.form.get("second_jump_WNS")
        ]
        third_jump_categories = [
            request.form.get("third_jump_M35"),
            request.form.get("third_jump_M50"),
            request.form.get("third_jump_M60"),
            request.form.get("third_jump_MNS"),
            request.form.get("third_jump_W35"),
            request.form.get("third_jump_W50"),
            request.form.get("third_jump_W60"),
            request.form.get("third_jump_WNS")
        ]
        fourth_jump_categories = [
            request.form.get("fourth_jump_M35"),
            request.form.get("fourth_jump_M50"),
            request.form.get("fourth_jump_M60"),
            request.form.get("fourth_jump_MNS"),
            request.form.get("fourth_jump_W35"),
            request.form.get("fourth_jump_W50"),
            request.form.get("fourth_jump_W60"),
            request.form.get("fourth_jump_WNS")
        ]
        first_throw_categories = [
            request.form.get("first_throw_M35"),
            request.form.get("first_throw_M50"),
            request.form.get("first_throw_M60"),
            request.form.get("first_throw_MNS"),
            request.form.get("first_throw_W35"),
            request.form.get("first_throw_W50"),
            request.form.get("first_throw_W60"),
            request.form.get("first_throw_WNS")
        ]
        second_throw_categories = [
            request.form.get("second_throw_M35"),
            request.form.get("second_throw_M50"),
            request.form.get("second_throw_M60"),
            request.form.get("second_throw_MNS"),
            request.form.get("second_throw_W35"),
            request.form.get("second_throw_W50"),
            request.form.get("second_throw_W60"),
            request.form.get("second_throw_WNS")
        ]
        third_throw_categories = [
            request.form.get("third_throw_M35"),
            request.form.get("third_throw_M50"),
            request.form.get("third_throw_M60"),
            request.form.get("third_throw_MNS"),
            request.form.get("third_throw_W35"),
            request.form.get("third_throw_W50"),
            request.form.get("third_throw_W60"),
            request.form.get("third_throw_WNS")
        ]
        fourth_throw_categories = [
            request.form.get("fourth_throw_M35"),
            request.form.get("fourth_throw_M50"),
            request.form.get("fourth_throw_M60"),
            request.form.get("fourth_throw_MNS"),
            request.form.get("fourth_throw_W35"),
            request.form.get("fourth_throw_W50"),
            request.form.get("fourth_throw_W60"),
            request.form.get("fourth_throw_WNS")
        ]
        # Remove null values in categories arrays
        first_sprint_categories = list(
            filter(None, first_sprint_categories))
        second_sprint_categories = list(
            filter(None, second_sprint_categories))
        third_sprint_categories = list(
            filter(None, third_sprint_categories))
        fourth_sprint_categories = list(
            filter(None, fourth_sprint_categories))
        first_middle_categories = list(
            filter(None, first_middle_categories))
        second_middle_categories = list(
            filter(None, second_middle_categories))
        first_distance_categories = list(
            filter(None, first_distance_categories))
        second_distance_categories = list(
            filter(None, second_distance_categories))
        third_distance_categories = list(
            filter(None, third_distance_categories))
        fourth_distance_categories = list(
            filter(None, fourth_distance_categories))
        first_relay_categories = list(
            filter(None, first_relay_categories))
        second_relay_categories = list(
            filter(None, second_relay_categories))
        first_jump_categories = list(
            filter(None, first_jump_categories))
        second_jump_categories = list(
            filter(None, second_jump_categories))
        third_jump_categories = list(
            filter(None, third_jump_categories))
        fourth_jump_categories = list(
            filter(None, fourth_jump_categories))
        first_throw_categories = list(
            filter(None, first_throw_categories))
        second_throw_categories = list(
            filter(None, second_throw_categories))
        third_throw_categories = list(
            filter(None, third_throw_categories))
        fourth_throw_categories = list(
            filter(None, fourth_throw_categories))
        # Match event dictionary compiler
        if request.form.get("first_sprint_name") is None:
            first_sprint_event = None
        else:
            first_sprint_event = {
                "event_time": first_sprint_time,
                "event_name": request.form.get("first_sprint_name"),
                "event_categories": first_sprint_categories
            }
        if request.form.get("second_sprint_name") is None:
            second_sprint_event = None
        else:
            second_sprint_event = {
                "event_time": second_sprint_time,
                "event_name": request.form.get("second_sprint_name"),
                "event_categories": second_sprint_categories
            }
        if request.form.get("third_sprint_name") is None:
            third_sprint_event = None
        else:
            third_sprint_event = {
                "event_time": third_sprint_time,
                "event_name": request.form.get("third_sprint_name"),
                "event_categories": third_sprint_categories
            }
        if request.form.get("fourth_sprint_name") is None:
            fourth_sprint_event = None
        else:
            fourth_sprint_event = {
                "event_time": fourth_sprint_time,
                "event_name": request.form.get("fourth_sprint_name"),
                "event_categories": fourth_sprint_categories
            }
        if request.form.get("first_middle_name") is None:
            first_middle_event = None
        else:
            first_middle_event = {
                "event_time": first_middle_time,
                "event_name": request.form.get("first_middle_name"),
                "event_categories": first_middle_categories
            }
        if request.form.get("second_middle_name") is None:
            second_middle_event = None
        else:
            second_middle_event = {
                "event_time": second_middle_time,
                "event_name": request.form.get("second_middle_name"),
                "event_categories": second_middle_categories
            }
        if request.form.get("first_distance_name") is None:
            first_distance_event = None
        else:
            first_distance_event = {
                "event_time": first_distance_time,
                "event_name": request.form.get("first_distance_name"),
                "event_categories": first_distance_categories
            }
        if request.form.get("second_distance_name") is None:
            second_distance_event = None
        else:
            second_distance_event = {
                "event_time": second_distance_time,
                "event_name": request.form.get("second_distance_name"),
                "event_categories": second_distance_categories
            }
        if request.form.get("third_distance_name") is None:
            third_distance_event = None
        else:
            third_distance_event = {
                "event_time": third_distance_time,
                "event_name": request.form.get("third_distance_name"),
                "event_categories": third_distance_categories
            }
        if request.form.get("fourth_distance_name") is None:
            fourth_distance_event = None
        else:
            fourth_distance_event = {
                "event_time": fourth_distance_time,
                "event_name": request.form.get("fourth_distance_name"),
                "event_categories": fourth_distance_categories
            }
        if request.form.get("first_relay_name") is None:
            first_relay_event = None
        else:
            first_relay_event = {
                "event_time": first_relay_time,
                "event_name": request.form.get("first_relay_name"),
                "event_categories": first_relay_categories
            }
        if request.form.get("second_relay_name") is None:
            second_relay_event = None
        else:
            second_relay_event = {
                "event_time": second_relay_time,
                "event_name": request.form.get("second_relay_name"),
                "event_categories": second_relay_categories
            }
        if request.form.get("first_jump_name") is None:
            first_jump_event = None
        else:
            first_jump_event = {
                "event_time": first_jump_time,
                "event_name": request.form.get("first_jump_name"),
                "event_categories": first_jump_categories
            }
        if request.form.get("second_jump_name") is None:
            second_jump_event = None
        else:
            second_jump_event = {
                "event_time": second_jump_time,
                "event_name": request.form.get("second_jump_name"),
                "event_categories": second_jump_categories
            }
        if request.form.get("third_jump_name") is None:
            third_jump_event = None
        else:
            third_jump_event = {
                "event_time": third_jump_time,
                "event_name": request.form.get("third_jump_name"),
                "event_categories": third_jump_categories
            }
        if request.form.get("fourth_jump_name") is None:
            fourth_jump_event = None
        else:
            fourth_jump_event = {
                "event_time": fourth_jump_time,
                "event_name": request.form.get("fourth_jump_name"),
                "event_categories": fourth_jump_categories
            }
        if request.form.get("first_throw_name") is None:
            first_throw_event = None
        else:
            first_throw_event = {
                "event_time": first_throw_time,
                "event_name": request.form.get("first_throw_name"),
                "event_categories": first_throw_categories
            }
        if request.form.get("second_throw_name") is None:
            second_throw_event = None
        else:
            second_throw_event = {
                "event_time": second_throw_time,
                "event_name": request.form.get("second_throw_name"),
                "event_categories": second_throw_categories
            }
        if request.form.get("third_throw_name") is None:
            third_throw_event = None
        else:
            third_throw_event = {
                "event_time": third_throw_time,
                "event_name": request.form.get("third_throw_name"),
                "event_categories": third_throw_categories
            }
        if request.form.get("fourth_throw_name") is None:
            fourth_throw_event = None
        else:
            fourth_throw_event = {
                "event_time": fourth_throw_time,
                "event_name": request.form.get("fourth_throw_name"),
                "event_categories": fourth_throw_categories
            }
        # Match timetable array compiler
        match_timetable = [
            first_sprint_event,
            second_sprint_event,
            third_sprint_event,
            fourth_sprint_event,
            first_middle_event,
            second_middle_event,
            first_distance_event,
            second_distance_event,
            third_distance_event,
            fourth_distance_event,
            first_relay_event,
            second_relay_event,
            first_jump_event,
            second_jump_event,
            third_jump_event,
            fourth_jump_event,
            first_throw_event,
            second_throw_event,
            third_throw_event,
            fourth_throw_event
        ]
        # Remove null values
        match_timetable = list(filter(None, match_timetable))
        timetable = {
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
        mongo.db.matches.update({"_id": ObjectId(match_id)}, timetable)
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
    first_sprint_hours = mongo.db.first_sprint_hours.find().sort(
        "hour")
    first_sprint_minutes = mongo.db.first_sprint_minutes.find().sort(
        "minute")
    first_sprint_events = mongo.db.first_sprint_events.find().sort(
        "event_name")
    second_sprint_hours = mongo.db.second_sprint_hours.find().sort(
        "hour")
    second_sprint_minutes = mongo.db.second_sprint_minutes.find().sort(
        "minute")
    second_sprint_events = mongo.db.second_sprint_events.find().sort(
        "event_name")
    third_sprint_hours = mongo.db.third_sprint_hours.find().sort(
        "hour")
    third_sprint_minutes = mongo.db.third_sprint_minutes.find().sort(
        "minute")
    third_sprint_events = mongo.db.third_sprint_events.find().sort(
        "event_name")
    fourth_sprint_hours = mongo.db.fourth_sprint_hours.find().sort(
        "hour")
    fourth_sprint_minutes = mongo.db.fourth_sprint_minutes.find().sort(
        "minute")
    fourth_sprint_events = mongo.db.fourth_sprint_events.find().sort(
        "event_name")
    first_middle_hours = mongo.db.first_middle_hours.find().sort(
        "hour")
    first_middle_minutes = mongo.db.first_middle_minutes.find().sort(
        "minute")
    first_middle_events = mongo.db.first_middle_events.find().sort(
        "event_name")
    second_middle_hours = mongo.db.second_middle_hours.find().sort(
        "hour")
    second_middle_minutes = mongo.db.second_middle_minutes.find().sort(
        "minute")
    second_middle_events = mongo.db.second_middle_events.find().sort(
        "event_name")
    first_distance_hours = mongo.db.first_distance_hours.find().sort(
        "hour")
    first_distance_minutes = mongo.db.first_distance_minutes.find().sort(
        "minute")
    first_distance_events = mongo.db.first_distance_events.find().sort(
        "event_name")
    second_distance_hours = mongo.db.second_distance_hours.find().sort(
        "hour")
    second_distance_minutes = mongo.db.second_distance_minutes.find().sort(
        "minute")
    second_distance_events = mongo.db.second_distance_events.find().sort(
        "event_name")
    third_distance_hours = mongo.db.third_distance_hours.find().sort(
        "hour")
    third_distance_minutes = mongo.db.third_distance_minutes.find().sort(
        "minute")
    third_distance_events = mongo.db.third_distance_events.find().sort(
        "event_name")
    fourth_distance_hours = mongo.db.fourth_distance_hours.find().sort(
        "hour")
    fourth_distance_minutes = mongo.db.fourth_distance_minutes.find().sort(
        "minute")
    fourth_distance_events = mongo.db.fourth_distance_events.find().sort(
        "event_name")
    first_relay_hours = mongo.db.first_relay_hours.find().sort(
        "hour")
    first_relay_minutes = mongo.db.first_relay_minutes.find().sort(
        "minute")
    first_relay_events = mongo.db.first_relay_events.find().sort(
        "event_name")
    second_relay_hours = mongo.db.second_relay_hours.find().sort(
        "hour")
    second_relay_minutes = mongo.db.second_relay_minutes.find().sort(
        "minute")
    second_relay_events = mongo.db.second_relay_events.find().sort(
        "event_name")
    first_jump_hours = mongo.db.first_jump_hours.find().sort(
        "hour")
    first_jump_minutes = mongo.db.first_jump_minutes.find().sort(
        "minute")
    first_jump_events = mongo.db.first_jump_events.find().sort(
        "event_name")
    second_jump_hours = mongo.db.second_jump_hours.find().sort(
        "hour")
    second_jump_minutes = mongo.db.second_jump_minutes.find().sort(
        "minute")
    second_jump_events = mongo.db.second_jump_events.find().sort(
        "event_name")
    third_jump_hours = mongo.db.third_jump_hours.find().sort(
        "hour")
    third_jump_minutes = mongo.db.third_jump_minutes.find().sort(
        "minute")
    third_jump_events = mongo.db.third_jump_events.find().sort(
        "event_name")
    fourth_jump_hours = mongo.db.fourth_jump_hours.find().sort(
        "hour")
    fourth_jump_minutes = mongo.db.fourth_jump_minutes.find().sort(
        "minute")
    fourth_jump_events = mongo.db.fourth_jump_events.find().sort(
        "event_name")
    first_throw_hours = mongo.db.first_throw_hours.find().sort(
        "hour")
    first_throw_minutes = mongo.db.first_throw_minutes.find().sort(
        "minute")
    first_throw_events = mongo.db.first_throw_events.find().sort(
        "event_name")
    second_throw_hours = mongo.db.second_throw_hours.find().sort(
        "hour")
    second_throw_minutes = mongo.db.second_throw_minutes.find().sort(
        "minute")
    second_throw_events = mongo.db.second_throw_events.find().sort(
        "event_name")
    third_throw_hours = mongo.db.third_throw_hours.find().sort(
        "hour")
    third_throw_minutes = mongo.db.third_throw_minutes.find().sort(
        "minute")
    third_throw_events = mongo.db.third_throw_events.find().sort(
        "event_name")
    fourth_throw_hours = mongo.db.fourth_throw_hours.find().sort(
        "hour")
    fourth_throw_minutes = mongo.db.fourth_throw_minutes.find().sort(
        "minute")
    fourth_throw_events = mongo.db.fourth_throw_events.find().sort(
        "event_name")
    return render_template(
        "add_timetable.html",
        match=match,
        seasons=seasons,
        weekdays=weekdays,
        monthdays=monthdays,
        months=months,
        venues=venues,
        first_sprint_hours=first_sprint_hours,
        first_sprint_minutes=first_sprint_minutes,
        first_sprint_events=first_sprint_events,
        second_sprint_hours=second_sprint_hours,
        second_sprint_minutes=second_sprint_minutes,
        second_sprint_events=second_sprint_events,
        third_sprint_hours=third_sprint_hours,
        third_sprint_minutes=third_sprint_minutes,
        third_sprint_events=third_sprint_events,
        fourth_sprint_hours=fourth_sprint_hours,
        fourth_sprint_minutes=fourth_sprint_minutes,
        fourth_sprint_events=fourth_sprint_events,
        first_middle_hours=first_middle_hours,
        first_middle_minutes=first_middle_minutes,
        first_middle_events=first_middle_events,
        second_middle_hours=second_middle_hours,
        second_middle_minutes=second_middle_minutes,
        second_middle_events=second_middle_events,
        first_distance_hours=first_distance_hours,
        first_distance_minutes=first_distance_minutes,
        first_distance_events=first_distance_events,
        second_distance_hours=second_distance_hours,
        second_distance_minutes=second_distance_minutes,
        second_distance_events=second_distance_events,
        third_distance_hours=third_distance_hours,
        third_distance_minutes=third_distance_minutes,
        third_distance_events=third_distance_events,
        fourth_distance_hours=fourth_distance_hours,
        fourth_distance_minutes=fourth_distance_minutes,
        fourth_distance_events=fourth_distance_events,
        first_relay_hours=first_relay_hours,
        first_relay_minutes=first_relay_minutes,
        first_relay_events=first_relay_events,
        second_relay_hours=second_relay_hours,
        second_relay_minutes=second_relay_minutes,
        second_relay_events=second_relay_events,
        first_jump_hours=first_jump_hours,
        first_jump_minutes=first_jump_minutes,
        first_jump_events=first_jump_events,
        second_jump_hours=second_jump_hours,
        second_jump_minutes=second_jump_minutes,
        second_jump_events=second_jump_events,
        third_jump_hours=third_jump_hours,
        third_jump_minutes=third_jump_minutes,
        third_jump_events=third_jump_events,
        fourth_jump_hours=fourth_jump_hours,
        fourth_jump_minutes=fourth_jump_minutes,
        fourth_jump_events=fourth_jump_events,
        first_throw_hours=first_throw_hours,
        first_throw_minutes=first_throw_minutes,
        first_throw_events=first_throw_events,
        second_throw_hours=second_throw_hours,
        second_throw_minutes=second_throw_minutes,
        second_throw_events=second_throw_events,
        third_throw_hours=third_throw_hours,
        third_throw_minutes=third_throw_minutes,
        third_throw_events=third_throw_events,
        fourth_throw_hours=fourth_throw_hours,
        fourth_throw_minutes=fourth_throw_minutes,
        fourth_throw_events=fourth_throw_events,
        access=access
    )


@app.route("/edit_timetable/<match_id>", methods=["GET", "POST"])
def edit_timetable(match_id):
    if request.method == "POST":
        # Additional information for venues
        if request.form.get("match_venue") == "Tilsley Park":
            venue_address = "Dunmore Road, Abingdon, Oxfordshire"
            venue_postcode = "OX14 1PU"
            venue_latitude = 51.68851413424184
            venue_longitude = -1.2844304304305583
        elif request.form.get(
            "match_venue") == "Horspath Athletics and Sports Ground":
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
        elif request.form.get(
            "match_venue") == "Crookham Common Athletics Track":
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
        match_date = request.form.get(
            "match_season") + numeric_month + numeric_monthday
        # Time compiler
        if request.form.get("first_sprint_hour") is None:
            first_sprint_time = None
        elif request.form.get("first_sprint_minute") is None:
            first_sprint_time = None
        else:
            first_sprint_time = request.form.get(
                "first_sprint_hour") + ":" + request.form.get(
                    "first_sprint_minute")
        if request.form.get("second_sprint_hour") is None:
            second_sprint_time = None
        elif request.form.get("second_sprint_minute") is None:
            second_sprint_time = None
        else:
            second_sprint_time = request.form.get(
                "second_sprint_hour") + ":" + request.form.get(
                    "second_sprint_minute")
        if request.form.get("third_sprint_hour") is None:
            third_sprint_time = None
        elif request.form.get("third_sprint_minute") is None:
            third_sprint_time = None
        else:
            third_sprint_time = request.form.get(
                "third_sprint_hour") + ":" + request.form.get(
                    "third_sprint_minute")
        if request.form.get("fourth_sprint_hour") is None:
            fourth_sprint_time = None
        elif request.form.get("fourth_sprint_minute") is None:
            fourth_sprint_time = None
        else:
            fourth_sprint_time = request.form.get(
                "fourth_sprint_hour") + ":" + request.form.get(
                    "fourth_sprint_minute")
        if request.form.get("first_middle_hour") is None:
            first_middle_time = None
        elif request.form.get("first_middle_minute") is None:
            first_middle_time = None
        else:
            first_middle_time = request.form.get(
                "first_middle_hour") + ":" + request.form.get(
                    "first_middle_minute")
        if request.form.get("second_middle_hour") is None:
            second_middle_time = None
        elif request.form.get("second_middle_minute") is None:
            second_middle_time = None
        else:
            second_middle_time = request.form.get(
                "second_middle_hour") + ":" + request.form.get(
                    "second_middle_minute")
        if request.form.get("first_distance_hour") is None:
            first_distance_time = None
        elif request.form.get("first_distance_minute") is None:
            first_distance_time = None
        else:
            first_distance_time = request.form.get(
                "first_distance_hour") + ":" + request.form.get(
                    "first_distance_minute")
        if request.form.get("second_distance_hour") is None:
            second_distance_time = None
        elif request.form.get("second_distance_minute") is None:
            second_distance_time = None
        else:
            second_distance_time = request.form.get(
                "second_distance_hour") + ":" + request.form.get(
                    "second_distance_minute")
        if request.form.get("third_distance_hour") is None:
            third_distance_time = None
        elif request.form.get("third_distance_minute") is None:
            third_distance_time = None
        else:
            third_distance_time = request.form.get(
                "third_distance_hour") + ":" + request.form.get(
                    "third_distance_minute")
        if request.form.get("fourth_distance_hour") is None:
            fourth_distance_time = None
        elif request.form.get("fourth_distance_minute") is None:
            fourth_distance_time = None
        else:
            fourth_distance_time = request.form.get(
                "fourth_distance_hour") + ":" + request.form.get(
                    "fourth_distance_minute")
        if request.form.get("first_relay_hour") is None:
            first_relay_time = None
        elif request.form.get("first_relay_minute") is None:
            first_relay_time = None
        else:
            first_relay_time = request.form.get(
                "first_relay_hour") + ":" + request.form.get(
                    "first_relay_minute")
        if request.form.get("second_relay_hour") is None:
            second_relay_time = None
        elif request.form.get("second_relay_minute") is None:
            second_relay_time = None
        else:
            second_relay_time = request.form.get(
                "second_relay_hour") + ":" + request.form.get(
                    "second_relay_minute")
        if request.form.get("first_jump_hour") is None:
            first_jump_time = None
        elif request.form.get("first_jump_minute") is None:
            first_jump_time = None
        else:
            first_jump_time = request.form.get(
                "first_jump_hour") + ":" + request.form.get(
                    "first_jump_minute")
        if request.form.get("second_jump_hour") is None:
            second_jump_time = None
        elif request.form.get("second_jump_minute") is None:
            second_jump_time = None
        else:
            second_jump_time = request.form.get(
                "second_jump_hour") + ":" + request.form.get(
                    "second_jump_minute")
        if request.form.get("third_jump_hour") is None:
            third_jump_time = None
        elif request.form.get("third_jump_minute") is None:
            third_jump_time = None
        else:
            third_jump_time = request.form.get(
                "third_jump_hour") + ":" + request.form.get(
                    "third_jump_minute")
        if request.form.get("fourth_jump_hour") is None:
            fourth_jump_time = None
        elif request.form.get("fourth_jump_minute") is None:
            fourth_jump_time = None
        else:
            fourth_jump_time = request.form.get(
                "fourth_jump_hour") + ":" + request.form.get(
                    "fourth_jump_minute")
        if request.form.get("first_throw_hour") is None:
            first_throw_time = None
        elif request.form.get("first_throw_minute") is None:
            first_throw_time = None
        else:
            first_throw_time = request.form.get(
                "first_throw_hour") + ":" + request.form.get(
                    "first_throw_minute")
        if request.form.get("second_throw_hour") is None:
            second_throw_time = None
        elif request.form.get("second_throw_minute") is None:
            second_throw_time = None
        else:
            second_throw_time = request.form.get(
                "second_throw_hour") + ":" + request.form.get(
                    "second_throw_minute")
        if request.form.get("third_throw_hour") is None:
            third_throw_time = None
        elif request.form.get("third_throw_minute") is None:
            third_throw_time = None
        else:
            third_throw_time = request.form.get(
                "third_throw_hour") + ":" + request.form.get(
                    "third_throw_minute")
        if request.form.get("fourth_throw_hour") is None:
            fourth_throw_time = None
        elif request.form.get("fourth_throw_minute") is None:
            fourth_throw_time = None
        else:
            fourth_throw_time = request.form.get(
                "fourth_throw_hour") + ":" + request.form.get(
                    "fourth_throw_minute")
        # Categories array compiler
        first_sprint_categories = [
            request.form.get("first_sprint_M35A"),
            request.form.get("first_sprint_M35B"),
            request.form.get("first_sprint_M50"),
            request.form.get("first_sprint_M60"),
            request.form.get("first_sprint_MNS"),
            request.form.get("first_sprint_W35A"),
            request.form.get("first_sprint_W35B"),
            request.form.get("first_sprint_W50"),
            request.form.get("first_sprint_W60"),
            request.form.get("first_sprint_WNS")
        ]
        second_sprint_categories = [
            request.form.get("second_sprint_M35A"),
            request.form.get("second_sprint_M35B"),
            request.form.get("second_sprint_M50"),
            request.form.get("second_sprint_M60"),
            request.form.get("second_sprint_MNS"),
            request.form.get("second_sprint_W35A"),
            request.form.get("second_sprint_W35B"),
            request.form.get("second_sprint_W50"),
            request.form.get("second_sprint_W60"),
            request.form.get("second_sprint_WNS")
        ]
        third_sprint_categories = [
            request.form.get("third_sprint_M35A"),
            request.form.get("third_sprint_M35B"),
            request.form.get("third_sprint_M50"),
            request.form.get("third_sprint_M60"),
            request.form.get("third_sprint_MNS"),
            request.form.get("third_sprint_W35A"),
            request.form.get("third_sprint_W35B"),
            request.form.get("third_sprint_W50"),
            request.form.get("third_sprint_W60"),
            request.form.get("third_sprint_WNS")
        ]
        fourth_sprint_categories = [
            request.form.get("fourth_sprint_M35A"),
            request.form.get("fourth_sprint_M35B"),
            request.form.get("fourth_sprint_M50"),
            request.form.get("fourth_sprint_M60"),
            request.form.get("fourth_sprint_MNS"),
            request.form.get("fourth_sprint_W35A"),
            request.form.get("fourth_sprint_W35B"),
            request.form.get("fourth_sprint_W50"),
            request.form.get("fourth_sprint_W60"),
            request.form.get("fourth_sprint_WNS")
        ]
        first_middle_categories = [
            request.form.get("first_middle_M35A"),
            request.form.get("first_middle_M35B"),
            request.form.get("first_middle_M50"),
            request.form.get("first_middle_M60"),
            request.form.get("first_middle_MNS"),
            request.form.get("first_middle_W35A"),
            request.form.get("first_middle_W35B"),
            request.form.get("first_middle_W50"),
            request.form.get("first_middle_W60"),
            request.form.get("first_middle_WNS")
        ]
        second_middle_categories = [
            request.form.get("second_middle_M35A"),
            request.form.get("second_middle_M35B"),
            request.form.get("second_middle_M50"),
            request.form.get("second_middle_M60"),
            request.form.get("second_middle_MNS"),
            request.form.get("second_middle_W35A"),
            request.form.get("second_middle_W35B"),
            request.form.get("second_middle_W50"),
            request.form.get("second_middle_W60"),
            request.form.get("second_middle_WNS")
        ]
        first_distance_categories = [
            request.form.get("first_distance_M35"),
            request.form.get("first_distance_M35A"),
            request.form.get("first_distance_M35B"),
            request.form.get("first_distance_M50"),
            request.form.get("first_distance_M60"),
            request.form.get("first_distance_MNS"),
            request.form.get("first_distance_W35"),
            request.form.get("first_distance_W35A"),
            request.form.get("first_distance_W35B"),
            request.form.get("first_distance_W50"),
            request.form.get("first_distance_W60"),
            request.form.get("first_distance_WNS")
        ]
        second_distance_categories = [
            request.form.get("second_distance_M35"),
            request.form.get("second_distance_M35A"),
            request.form.get("second_distance_M35B"),
            request.form.get("second_distance_M50"),
            request.form.get("second_distance_M60"),
            request.form.get("second_distance_MNS"),
            request.form.get("second_distance_W35"),
            request.form.get("second_distance_W35A"),
            request.form.get("second_distance_W35B"),
            request.form.get("second_distance_W50"),
            request.form.get("second_distance_W60"),
            request.form.get("second_distance_WNS")
        ]
        third_distance_categories = [
            request.form.get("third_distance_M35"),
            request.form.get("third_distance_M35A"),
            request.form.get("third_distance_M35B"),
            request.form.get("third_distance_M50"),
            request.form.get("third_distance_M60"),
            request.form.get("third_distance_MNS"),
            request.form.get("third_distance_W35"),
            request.form.get("third_distance_W35A"),
            request.form.get("third_distance_W35B"),
            request.form.get("third_distance_W50"),
            request.form.get("third_distance_W60"),
            request.form.get("third_distance_WNS")
        ]
        fourth_distance_categories = [
            request.form.get("fourth_distance_M35"),
            request.form.get("fourth_distance_M35A"),
            request.form.get("fourth_distance_M35B"),
            request.form.get("fourth_distance_M50"),
            request.form.get("fourth_distance_M60"),
            request.form.get("fourth_distance_MNS"),
            request.form.get("fourth_distance_W35"),
            request.form.get("fourth_distance_W35A"),
            request.form.get("fourth_distance_W35B"),
            request.form.get("fourth_distance_W50"),
            request.form.get("fourth_distance_W60"),
            request.form.get("fourth_distance_WNS")
        ]
        first_relay_categories = [
            request.form.get("first_relay_M35"),
            request.form.get("first_relay_W35")
        ]
        second_relay_categories = [
            request.form.get("second_relay_M35"),
            request.form.get("second_relay_W35")
        ]
        first_jump_categories = [
            request.form.get("first_jump_M35"),
            request.form.get("first_jump_M50"),
            request.form.get("first_jump_M60"),
            request.form.get("first_jump_MNS"),
            request.form.get("first_jump_W35"),
            request.form.get("first_jump_W50"),
            request.form.get("first_jump_W60"),
            request.form.get("first_jump_WNS")
        ]
        second_jump_categories = [
            request.form.get("second_jump_M35"),
            request.form.get("second_jump_M50"),
            request.form.get("second_jump_M60"),
            request.form.get("second_jump_MNS"),
            request.form.get("second_jump_W35"),
            request.form.get("second_jump_W50"),
            request.form.get("second_jump_W60"),
            request.form.get("second_jump_WNS")
        ]
        third_jump_categories = [
            request.form.get("third_jump_M35"),
            request.form.get("third_jump_M50"),
            request.form.get("third_jump_M60"),
            request.form.get("third_jump_MNS"),
            request.form.get("third_jump_W35"),
            request.form.get("third_jump_W50"),
            request.form.get("third_jump_W60"),
            request.form.get("third_jump_WNS")
        ]
        fourth_jump_categories = [
            request.form.get("fourth_jump_M35"),
            request.form.get("fourth_jump_M50"),
            request.form.get("fourth_jump_M60"),
            request.form.get("fourth_jump_MNS"),
            request.form.get("fourth_jump_W35"),
            request.form.get("fourth_jump_W50"),
            request.form.get("fourth_jump_W60"),
            request.form.get("fourth_jump_WNS")
        ]
        first_throw_categories = [
            request.form.get("first_throw_M35"),
            request.form.get("first_throw_M50"),
            request.form.get("first_throw_M60"),
            request.form.get("first_throw_MNS"),
            request.form.get("first_throw_W35"),
            request.form.get("first_throw_W50"),
            request.form.get("first_throw_W60"),
            request.form.get("first_throw_WNS")
        ]
        second_throw_categories = [
            request.form.get("second_throw_M35"),
            request.form.get("second_throw_M50"),
            request.form.get("second_throw_M60"),
            request.form.get("second_throw_MNS"),
            request.form.get("second_throw_W35"),
            request.form.get("second_throw_W50"),
            request.form.get("second_throw_W60"),
            request.form.get("second_throw_WNS")
        ]
        third_throw_categories = [
            request.form.get("third_throw_M35"),
            request.form.get("third_throw_M50"),
            request.form.get("third_throw_M60"),
            request.form.get("third_throw_MNS"),
            request.form.get("third_throw_W35"),
            request.form.get("third_throw_W50"),
            request.form.get("third_throw_W60"),
            request.form.get("third_throw_WNS")
        ]
        fourth_throw_categories = [
            request.form.get("fourth_throw_M35"),
            request.form.get("fourth_throw_M50"),
            request.form.get("fourth_throw_M60"),
            request.form.get("fourth_throw_MNS"),
            request.form.get("fourth_throw_W35"),
            request.form.get("fourth_throw_W50"),
            request.form.get("fourth_throw_W60"),
            request.form.get("fourth_throw_WNS")
        ]
        # Remove null values in categories arrays
        first_sprint_categories = list(
            filter(None, first_sprint_categories))
        second_sprint_categories = list(
            filter(None, second_sprint_categories))
        third_sprint_categories = list(
            filter(None, third_sprint_categories))
        fourth_sprint_categories = list(
            filter(None, fourth_sprint_categories))
        first_middle_categories = list(
            filter(None, first_middle_categories))
        second_middle_categories = list(
            filter(None, second_middle_categories))
        first_distance_categories = list(
            filter(None, first_distance_categories))
        second_distance_categories = list(
            filter(None, second_distance_categories))
        third_distance_categories = list(
            filter(None, third_distance_categories))
        fourth_distance_categories = list(
            filter(None, fourth_distance_categories))
        first_relay_categories = list(
            filter(None, first_relay_categories))
        second_relay_categories = list(
            filter(None, second_relay_categories))
        first_jump_categories = list(
            filter(None, first_jump_categories))
        second_jump_categories = list(
            filter(None, second_jump_categories))
        third_jump_categories = list(
            filter(None, third_jump_categories))
        fourth_jump_categories = list(
            filter(None, fourth_jump_categories))
        first_throw_categories = list(
            filter(None, first_throw_categories))
        second_throw_categories = list(
            filter(None, second_throw_categories))
        third_throw_categories = list(
            filter(None, third_throw_categories))
        fourth_throw_categories = list(
            filter(None, fourth_throw_categories))
        # Match event dictionary compiler
        if request.form.get("first_sprint_name") is None:
            first_sprint_event = None
        else:
            first_sprint_event = {
                "event_time": first_sprint_time,
                "event_name": request.form.get("first_sprint_name"),
                "event_categories": first_sprint_categories
            }
        if request.form.get("second_sprint_name") is None:
            second_sprint_event = None
        else:
            second_sprint_event = {
                "event_time": second_sprint_time,
                "event_name": request.form.get("second_sprint_name"),
                "event_categories": second_sprint_categories
            }
        if request.form.get("third_sprint_name") is None:
            third_sprint_event = None
        else:
            third_sprint_event = {
                "event_time": third_sprint_time,
                "event_name": request.form.get("third_sprint_name"),
                "event_categories": third_sprint_categories
            }
        if request.form.get("fourth_sprint_name") is None:
            fourth_sprint_event = None
        else:
            fourth_sprint_event = {
                "event_time": fourth_sprint_time,
                "event_name": request.form.get("fourth_sprint_name"),
                "event_categories": fourth_sprint_categories
            }
        if request.form.get("first_middle_name") is None:
            first_middle_event = None
        else:
            first_middle_event = {
                "event_time": first_middle_time,
                "event_name": request.form.get("first_middle_name"),
                "event_categories": first_middle_categories
            }
        if request.form.get("second_middle_name") is None:
            second_middle_event = None
        else:
            second_middle_event = {
                "event_time": second_middle_time,
                "event_name": request.form.get("second_middle_name"),
                "event_categories": second_middle_categories
            }
        if request.form.get("first_distance_name") is None:
            first_distance_event = None
        else:
            first_distance_event = {
                "event_time": first_distance_time,
                "event_name": request.form.get("first_distance_name"),
                "event_categories": first_distance_categories
            }
        if request.form.get("second_distance_name") is None:
            second_distance_event = None
        else:
            second_distance_event = {
                "event_time": second_distance_time,
                "event_name": request.form.get("second_distance_name"),
                "event_categories": second_distance_categories
            }
        if request.form.get("third_distance_name") is None:
            third_distance_event = None
        else:
            third_distance_event = {
                "event_time": third_distance_time,
                "event_name": request.form.get("third_distance_name"),
                "event_categories": third_distance_categories
            }
        if request.form.get("fourth_distance_name") is None:
            fourth_distance_event = None
        else:
            fourth_distance_event = {
                "event_time": fourth_distance_time,
                "event_name": request.form.get("fourth_distance_name"),
                "event_categories": fourth_distance_categories
            }
        if request.form.get("first_relay_name") is None:
            first_relay_event = None
        else:
            first_relay_event = {
                "event_time": first_relay_time,
                "event_name": request.form.get("first_relay_name"),
                "event_categories": first_relay_categories
            }
        if request.form.get("second_relay_name") is None:
            second_relay_event = None
        else:
            second_relay_event = {
                "event_time": second_relay_time,
                "event_name": request.form.get("second_relay_name"),
                "event_categories": second_relay_categories
            }
        if request.form.get("first_jump_name") is None:
            first_jump_event = None
        else:
            first_jump_event = {
                "event_time": first_jump_time,
                "event_name": request.form.get("first_jump_name"),
                "event_categories": first_jump_categories
            }
        if request.form.get("second_jump_name") is None:
            second_jump_event = None
        else:
            second_jump_event = {
                "event_time": second_jump_time,
                "event_name": request.form.get("second_jump_name"),
                "event_categories": second_jump_categories
            }
        if request.form.get("third_jump_name") is None:
            third_jump_event = None
        else:
            third_jump_event = {
                "event_time": third_jump_time,
                "event_name": request.form.get("third_jump_name"),
                "event_categories": third_jump_categories
            }
        if request.form.get("fourth_jump_name") is None:
            fourth_jump_event = None
        else:
            fourth_jump_event = {
                "event_time": fourth_jump_time,
                "event_name": request.form.get("fourth_jump_name"),
                "event_categories": fourth_jump_categories
            }
        if request.form.get("first_throw_name") is None:
            first_throw_event = None
        else:
            first_throw_event = {
                "event_time": first_throw_time,
                "event_name": request.form.get("first_throw_name"),
                "event_categories": first_throw_categories
            }
        if request.form.get("second_throw_name") is None:
            second_throw_event = None
        else:
            second_throw_event = {
                "event_time": second_throw_time,
                "event_name": request.form.get("second_throw_name"),
                "event_categories": second_throw_categories
            }
        if request.form.get("third_throw_name") is None:
            third_throw_event = None
        else:
            third_throw_event = {
                "event_time": third_throw_time,
                "event_name": request.form.get("third_throw_name"),
                "event_categories": third_throw_categories
            }
        if request.form.get("fourth_throw_name") is None:
            fourth_throw_event = None
        else:
            fourth_throw_event = {
                "event_time": fourth_throw_time,
                "event_name": request.form.get("fourth_throw_name"),
                "event_categories": fourth_throw_categories
            }
        # Match timetable array compiler
        match_timetable = [
            first_sprint_event,
            second_sprint_event,
            third_sprint_event,
            fourth_sprint_event,
            first_middle_event,
            second_middle_event,
            first_distance_event,
            second_distance_event,
            third_distance_event,
            fourth_distance_event,
            first_relay_event,
            second_relay_event,
            first_jump_event,
            second_jump_event,
            third_jump_event,
            fourth_jump_event,
            first_throw_event,
            second_throw_event,
            third_throw_event,
            fourth_throw_event
        ]
        # Remove null values
        match_timetable = list(filter(None, match_timetable))
        timetable = {
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
        mongo.db.matches.update({"_id": ObjectId(match_id)}, timetable)
        flash("Timetable successfully updated")
        return redirect(url_for("matches"))

    access = mongo.db.users.find_one(
        {"username": session["user"]})["access"]
    match = mongo.db.matches.find_one({"_id": ObjectId(match_id)})
    seasons = mongo.db.seasons.find().sort("season_year")
    weekdays = mongo.db.weekdays.find()
    monthdays = mongo.db.monthdays.find()
    months = mongo.db.months.find()
    venues = mongo.db.venues.find().sort("venue_name", 1)
    first_sprint_hours = mongo.db.first_sprint_hours.find().sort(
        "hour")
    first_sprint_minutes = mongo.db.first_sprint_minutes.find().sort(
        "minute")
    first_sprint_events = mongo.db.first_sprint_events.find().sort(
        "event_name")
    second_sprint_hours = mongo.db.second_sprint_hours.find().sort(
        "hour")
    second_sprint_minutes = mongo.db.second_sprint_minutes.find().sort(
        "minute")
    second_sprint_events = mongo.db.second_sprint_events.find().sort(
        "event_name")
    third_sprint_hours = mongo.db.third_sprint_hours.find().sort(
        "hour")
    third_sprint_minutes = mongo.db.third_sprint_minutes.find().sort(
        "minute")
    third_sprint_events = mongo.db.third_sprint_events.find().sort(
        "event_name")
    fourth_sprint_hours = mongo.db.fourth_sprint_hours.find().sort(
        "hour")
    fourth_sprint_minutes = mongo.db.fourth_sprint_minutes.find().sort(
        "minute")
    fourth_sprint_events = mongo.db.fourth_sprint_events.find().sort(
        "event_name")
    first_middle_hours = mongo.db.first_middle_hours.find().sort(
        "hour")
    first_middle_minutes = mongo.db.first_middle_minutes.find().sort(
        "minute")
    first_middle_events = mongo.db.first_middle_events.find().sort(
        "event_name")
    second_middle_hours = mongo.db.second_middle_hours.find().sort(
        "hour")
    second_middle_minutes = mongo.db.second_middle_minutes.find().sort(
        "minute")
    second_middle_events = mongo.db.second_middle_events.find().sort(
        "event_name")
    first_distance_hours = mongo.db.first_distance_hours.find().sort(
        "hour")
    first_distance_minutes = mongo.db.first_distance_minutes.find().sort(
        "minute")
    first_distance_events = mongo.db.first_distance_events.find().sort(
        "event_name")
    second_distance_hours = mongo.db.second_distance_hours.find().sort(
        "hour")
    second_distance_minutes = mongo.db.second_distance_minutes.find().sort(
        "minute")
    second_distance_events = mongo.db.second_distance_events.find().sort(
        "event_name")
    third_distance_hours = mongo.db.third_distance_hours.find().sort(
        "hour")
    third_distance_minutes = mongo.db.third_distance_minutes.find().sort(
        "minute")
    third_distance_events = mongo.db.third_distance_events.find().sort(
        "event_name")
    fourth_distance_hours = mongo.db.fourth_distance_hours.find().sort(
        "hour")
    fourth_distance_minutes = mongo.db.fourth_distance_minutes.find().sort(
        "minute")
    fourth_distance_events = mongo.db.fourth_distance_events.find().sort(
        "event_name")
    first_relay_hours = mongo.db.first_relay_hours.find().sort(
        "hour")
    first_relay_minutes = mongo.db.first_relay_minutes.find().sort(
        "minute")
    first_relay_events = mongo.db.first_relay_events.find().sort(
        "event_name")
    second_relay_hours = mongo.db.second_relay_hours.find().sort(
        "hour")
    second_relay_minutes = mongo.db.second_relay_minutes.find().sort(
        "minute")
    second_relay_events = mongo.db.second_relay_events.find().sort(
        "event_name")
    first_jump_hours = mongo.db.first_jump_hours.find().sort(
        "hour")
    first_jump_minutes = mongo.db.first_jump_minutes.find().sort(
        "minute")
    first_jump_events = mongo.db.first_jump_events.find().sort(
        "event_name")
    second_jump_hours = mongo.db.second_jump_hours.find().sort(
        "hour")
    second_jump_minutes = mongo.db.second_jump_minutes.find().sort(
        "minute")
    second_jump_events = mongo.db.second_jump_events.find().sort(
        "event_name")
    third_jump_hours = mongo.db.third_jump_hours.find().sort(
        "hour")
    third_jump_minutes = mongo.db.third_jump_minutes.find().sort(
        "minute")
    third_jump_events = mongo.db.third_jump_events.find().sort(
        "event_name")
    fourth_jump_hours = mongo.db.fourth_jump_hours.find().sort(
        "hour")
    fourth_jump_minutes = mongo.db.fourth_jump_minutes.find().sort(
        "minute")
    fourth_jump_events = mongo.db.fourth_jump_events.find().sort(
        "event_name")
    first_throw_hours = mongo.db.first_throw_hours.find().sort(
        "hour")
    first_throw_minutes = mongo.db.first_throw_minutes.find().sort(
        "minute")
    first_throw_events = mongo.db.first_throw_events.find().sort(
        "event_name")
    second_throw_hours = mongo.db.second_throw_hours.find().sort(
        "hour")
    second_throw_minutes = mongo.db.second_throw_minutes.find().sort(
        "minute")
    second_throw_events = mongo.db.second_throw_events.find().sort(
        "event_name")
    third_throw_hours = mongo.db.third_throw_hours.find().sort(
        "hour")
    third_throw_minutes = mongo.db.third_throw_minutes.find().sort(
        "minute")
    third_throw_events = mongo.db.third_throw_events.find().sort(
        "event_name")
    fourth_throw_hours = mongo.db.fourth_throw_hours.find().sort(
        "hour")
    fourth_throw_minutes = mongo.db.fourth_throw_minutes.find().sort(
        "minute")
    fourth_throw_events = mongo.db.fourth_throw_events.find().sort(
        "event_name")
    return render_template(
        "edit_timetable.html",
        match=match,
        seasons=seasons,
        weekdays=weekdays,
        monthdays=monthdays,
        months=months,
        venues=venues,
        first_sprint_hours=first_sprint_hours,
        first_sprint_minutes=first_sprint_minutes,
        first_sprint_events=first_sprint_events,
        second_sprint_hours=second_sprint_hours,
        second_sprint_minutes=second_sprint_minutes,
        second_sprint_events=second_sprint_events,
        third_sprint_hours=third_sprint_hours,
        third_sprint_minutes=third_sprint_minutes,
        third_sprint_events=third_sprint_events,
        fourth_sprint_hours=fourth_sprint_hours,
        fourth_sprint_minutes=fourth_sprint_minutes,
        fourth_sprint_events=fourth_sprint_events,
        first_middle_hours=first_middle_hours,
        first_middle_minutes=first_middle_minutes,
        first_middle_events=first_middle_events,
        second_middle_hours=second_middle_hours,
        second_middle_minutes=second_middle_minutes,
        second_middle_events=second_middle_events,
        first_distance_hours=first_distance_hours,
        first_distance_minutes=first_distance_minutes,
        first_distance_events=first_distance_events,
        second_distance_hours=second_distance_hours,
        second_distance_minutes=second_distance_minutes,
        second_distance_events=second_distance_events,
        third_distance_hours=third_distance_hours,
        third_distance_minutes=third_distance_minutes,
        third_distance_events=third_distance_events,
        fourth_distance_hours=fourth_distance_hours,
        fourth_distance_minutes=fourth_distance_minutes,
        fourth_distance_events=fourth_distance_events,
        first_relay_hours=first_relay_hours,
        first_relay_minutes=first_relay_minutes,
        first_relay_events=first_relay_events,
        second_relay_hours=second_relay_hours,
        second_relay_minutes=second_relay_minutes,
        second_relay_events=second_relay_events,
        first_jump_hours=first_jump_hours,
        first_jump_minutes=first_jump_minutes,
        first_jump_events=first_jump_events,
        second_jump_hours=second_jump_hours,
        second_jump_minutes=second_jump_minutes,
        second_jump_events=second_jump_events,
        third_jump_hours=third_jump_hours,
        third_jump_minutes=third_jump_minutes,
        third_jump_events=third_jump_events,
        fourth_jump_hours=fourth_jump_hours,
        fourth_jump_minutes=fourth_jump_minutes,
        fourth_jump_events=fourth_jump_events,
        first_throw_hours=first_throw_hours,
        first_throw_minutes=first_throw_minutes,
        first_throw_events=first_throw_events,
        second_throw_hours=second_throw_hours,
        second_throw_minutes=second_throw_minutes,
        second_throw_events=second_throw_events,
        third_throw_hours=third_throw_hours,
        third_throw_minutes=third_throw_minutes,
        third_throw_events=third_throw_events,
        fourth_throw_hours=fourth_throw_hours,
        fourth_throw_minutes=fourth_throw_minutes,
        fourth_throw_events=fourth_throw_events,
        access=access
    )



if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
