from flask import Flask, redirect, render_template, request, flash, url_for, session
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_mail import Mail, Message
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
import os
from dotenv import load_dotenv

#PT_flask = os.environ["PWD"]
import sys
import random
from datetime import date, timedelta

#sys.path.insert(0, PT_flask)

from datetime import timedelta
from app.models import (
    Workouts,
    WorkoutsView,
    User,
    UserView,
    UserProgress,
    UserProgressView,
    Routine,
    RoutineView,
    Day_of_routine,
    DayView,
    Test_data,
    db,
    Admin,
    AdminView,
    MyAdminIndexView,
)
from app.data.info_to_insert import *
from app.workout_functions import (
    list_of_videos,
    routine_with_videos,
    add_links_to_routine_days,
    filter_video_name,
    about_me_loop_vid,
)
from app.forms import ContactForm

from app.user_functions import user_exists, create_user

load_dotenv()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["PYTHONPATH"] = os.getenv("PYTHONPATH")

admin = Admin(app, index_view=MyAdminIndexView())

# Email configuration
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")


# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)

db.init_app(app)

# Initialize admin views with error handling
try:
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoutineView(Routine, db.session))
    admin.add_view(DayView(Day_of_routine, db.session))
    admin.add_view(WorkoutsView(Workouts, db.session))
    admin.add_view(UserProgressView(UserProgress, db.session))
except Exception as e:
    print(f"Error initializing admin views: {str(e)}")

login_manager = LoginManager(app)
mail = Mail(app)
bcrypt = Bcrypt(app)
app.permanent_session_lifetime = timedelta(days=1)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# new code


@app.route("/video")
def video():
    video_url = list_of_videos()

    return render_template("video.html", video_urls=video_url)


@app.route("/play", methods=["POST", "GET"])
def play_video():
    if "user_id" in session:
        video_url = request.args.get(
            "video_url"
        )  # Get the video URL from query parameter
        if request.method == "POST":
            return redirect(url_for("day"))
        else:
            
            return render_template(
                "play_video.html",
                video_url=video_url,
                workout_name=filter_video_name(video_url, "workout_vids"),
            )

    return redirect(url_for("login"))


@app.route("/", methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("day"))
    if request.method == "POST":
        session.permanent = True
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username.lower()).first()
        if user and user.password == password:
            session["user_id"] = user.id

            login_user(user)

            if user.role == None:
                routine = Routine.query.filter_by(id=user.user_routine).first()
                
                session["beginning_day"] = routine.workouts[0].id
                
                user.days_logged_in += 1
                db.session.commit()
                flash("Login succesful!")
                if date(2024, 10, 23) > user.routine_change_date:

                    user.routine_change_date = date.today() + timedelta(weeks=6)
                    next_routine = Routine.query.filter_by(
                        routine_level=user.level
                    ).all()

                    while True:

                        choice = random.choice(next_routine).id
                        if choice != user.user_routine:

                            user.user_routine = choice

                            break

                    db.session.commit()
                    return redirect(url_for("day"))

                return redirect(url_for("day"))
            return redirect(url_for("admin.index"))
        elif user is None:
            return redirect(url_for("create_account"))

    return render_template("login.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if "user_id" in session:
        return redirect(url_for("day"))
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        password = request.form["password"]
        #goal = request.form["goal"]
        #level = request.form["level"]

        if user_exists(User, username):
            flash("You already have an account")
            return redirect(url_for("login"))

        else:
            routine = Routine.query.filter_by(id=1).all()
            
            assigned_routine = random.choice(routine)

            create_user(
                User,
                username,
                email,
                first_name,
                last_name,
                password,
                None,
                None,
                user_routine=assigned_routine.id,
            )
            flash("Account was created")
            return redirect(url_for("login"))
    return render_template("create_account.html")


@app.route("/logout")
def logout():
    if "user_id" in session:
        flash(f"You have been logged out!", "info")
    session.pop("user_id", None)
    session.pop("username", None)
    session.pop("email", None)
    return redirect(url_for("login"))


@app.route("/about_me")
def about_me():
    

    return render_template("about_me.html", about_me_vid=about_me_loop_vid("push ups"))


@app.route("/routine", methods=["POST", "GET"])
def routine():
    if "user_id" in session:
        
        routines = Routine.query.filter_by(id=session["user_id"]).first()
        
        routines1 = routine_with_videos(User.query.filter_by(id=session["user_id"]).first(), Workouts.query.all())
        
        return render_template("routine.html", routine_days=routines1)
    else:
        return redirect(url_for("login"))


@app.route("/day", methods=["POST", "GET"])
def day():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()

        if user.current_day_id == None:
            user.current_day_id = session["beginning_day"]
            db.session.commit()
        
        day = Day_of_routine.query.filter_by(id=user.current_day_id).first()
        workout_day = add_links_to_routine_days(day, Workouts.query.all())
        
        
        
        return render_template(
            "day.html", workout_day=workout_day, day=day.workout_day_name
        )
    else:
        return redirect(url_for("login"))


@app.route("/change_day_id", methods=["POST", "GET"])
def change_day_id():

    user = User.query.filter_by(id=session["user_id"]).first()
    routine = Routine.query.filter_by(id=user.user_routine).first()

    if user.current_day_id >= routine.workouts[0].id + 3:
        user.current_day_id = routine.workouts[0].id
    else:
        user.current_day_id = user.current_day_id + 1
    # we will be adding a for loop right here
    # the day_id should be user.current_day_id
    # day_id = request.form["day_id"]
    # sets = request.form["sets"]
    # reps = request.form["reps"]

    db.session.commit()
    return redirect(url_for("day"))


@app.route("/contact_us", methods=["POST", "GET"])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject="Contact form submission",
                sender=form.email.data,
                recipients=["jcruz6003@gmail.com"],
                body=f"Message from: {form.name.data}\nEmail: {form.email.data}\n\nMessage:\n{form.message.data}"
            )
            mail.send(msg)
            flash("Message sent successfully!", "success")
            return redirect(url_for("contact_us"))
        except Exception as e:
            flash(f"Failed to send message. Please try again. Error: {str(e)}", "error")
            return redirect(url_for("contact_us"))

    return render_template("contact_us.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        print("Creating database ", db)
        db.create_all()

        app.run(debug=True)
