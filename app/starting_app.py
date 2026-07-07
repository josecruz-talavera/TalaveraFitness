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

# PT_flask = os.environ["PWD"]
import sys
import random
from datetime import date, timedelta

# sys.path.insert(0, PT_flask)

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
    RoutineDays,
    RoutineDaysView,
    MenuLink,
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
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


# app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
migrate = Migrate(app, db)

db.init_app(app)
with app.app_context():
    db.create_all()

# Initialize admin views with error handling
try:
    admin.add_view(UserView(User, db.session))
    admin.add_view(RoutineView(Routine, db.session))
    admin.add_view(DayView(Day_of_routine, db.session))
    admin.add_view(WorkoutsView(Workouts, db.session))
    admin.add_view(UserProgressView(UserProgress, db.session))
    admin.add_view(RoutineDaysView(RoutineDays, db.session))
    admin.add_link(MenuLink(name='Logout', url='/logout'))
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
        video_url = request.args.get("video_url")
        if request.method == "POST":
            return redirect(url_for("day"))
        else:
            workout_name = filter_video_name(video_url, "workout_vids")
            workout = Workouts.query.filter_by(workout_name=workout_name).first()
            description = workout.description if workout else None
            return render_template(
                "play_video.html",
                video_url=video_url,
                workout_name=workout_name,
                description=description,
            )
    return redirect(url_for("login"))


@app.route("/")
def welcome():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    return render_template("welcome.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(id=session["user_id"]).first()
    routine = Routine.query.filter_by(id=user.user_routine).first()

    # Current day info
    current_day = Day_of_routine.query.filter_by(id=user.current_day_id).first()

    # Last session — most recent progress entry
    last_entry = UserProgress.query.filter_by(user_id=user.id).order_by(
        UserProgress.date.desc(), UserProgress.id.desc()
    ).first()

    # Streak — count consecutive days with progress logged
    all_dates = db.session.query(UserProgress.date).filter_by(
        user_id=user.id
    ).distinct().order_by(UserProgress.date.desc()).all()
    all_dates = [d[0] for d in all_dates]

    streak = 0
    check = date.today()
    for d in all_dates:
        if d == check or d == check - timedelta(days=1):
            streak += 1
            check = d - timedelta(days=1)
        else:
            break

    # Total sessions logged
    total_sessions = db.session.query(UserProgress.date).filter_by(
        user_id=user.id
    ).distinct().count()

    # Day number in routine
    if routine and current_day:
        day_ids = [d.id for d in routine.workouts]
        day_number = day_ids.index(user.current_day_id) + 1 if user.current_day_id in day_ids else 1
        total_days = len(day_ids)
    else:
        day_number = 1
        total_days = 0

    return render_template(
        "dashboard.html",
        user=user,
        routine=routine,
        current_day=current_day,
        last_entry=last_entry,
        streak=streak,
        total_sessions=total_sessions,
        day_number=day_number,
        total_days=total_days,
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
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

                if date(2024, 10, 23) > user.routine_change_date:
                    user.routine_change_date = date.today() + timedelta(weeks=6)
                    next_routine = Routine.query.filter_by(routine_level=user.level).all()
                    while True:
                        choice = random.choice(next_routine).id
                        if choice != user.user_routine:
                            user.user_routine = choice
                            new_routine = Routine.query.filter_by(id=choice).first()
                            user.beginning_day_id = new_routine.workouts[0].id
                            user.current_day_id = new_routine.workouts[0].id
                            session["beginning_day"] = user.beginning_day_id
                            break
                    db.session.commit()
                    return redirect(url_for("dashboard"))

                return redirect(url_for("dashboard"))
            return redirect(url_for("admin.index"))
        elif user is None:
            return redirect(url_for("create_account"))

    return render_template("login.html")


@app.route("/create_account", methods=["POST", "GET"])
def create_account():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        username   = request.form["username"]
        email      = request.form["email"]
        first_name = request.form["first_name"]
        last_name  = request.form["last_name"]
        password   = request.form["password"]
        goal       = request.form.get("goal", "maintain")
        level      = request.form.get("level", "beginner")
        frequency  = int(request.form.get("frequency", 3))

        if user_exists(User, username):
            flash("You already have an account")
            return redirect(url_for("login"))

        # Map level to DB value
        level_map = {
            "beginner":     "beginner",
            "intermediate": "intermediate",
            "advanced":     "intermediate",  # fallback until advanced routines exist
        }
        db_level = level_map.get(level, "beginner")

        # Get all routines matching the user's level
        matching = Routine.query.filter_by(routine_level=db_level).all()

        # If no match, fall back to beginner
        if not matching:
            matching = Routine.query.filter_by(routine_level="beginner").all()

        # Pick the best routine based on frequency
        # Prefer routines whose name contains the frequency number
        preferred = [r for r in matching if str(frequency) in r.routine_name]
        pool = preferred if preferred else matching
        assigned_routine = random.choice(pool)

        beginning_day_id = (
            assigned_routine.workouts[0].id if assigned_routine.workouts else None
        )

        create_user(
            User,
            username.lower(),
            email,
            first_name,
            last_name,
            password,
            goal,
            level,
            user_routine=assigned_routine.id,
            beginning_day_id=beginning_day_id,
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
    return redirect(url_for("welcome"))


@app.route("/nutrition")
def nutrition():
    if "user_id" in session:
        return render_template("nutrition.html")
    return redirect(url_for("login"))


@app.route("/about_me")
def about_me():

    return render_template("about_me.html", about_me_vid=about_me_loop_vid("push ups"))


@app.route("/routine", methods=["POST", "GET"])
def routine():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()
        routines1 = routine_with_videos(user, Workouts.query.all())
        return render_template("routine.html", routine_days=routines1)
    else:
        return redirect(url_for("login"))


@app.route("/day", methods=["POST", "GET"])
def day():
    if "user_id" in session:
        user = User.query.filter_by(id=session["user_id"]).first()

        # Guard: check routine exists
        routine = Routine.query.filter_by(id=user.user_routine).first()
        if routine is None or len(routine.workouts) == 0:
            flash("No routine assigned. Please contact support.")
            return redirect(url_for("login"))

        # Get valid day IDs for current routine
        valid_day_ids = [d.id for d in routine.workouts]

        # If current_day_id is None or belongs to old routine, reset it
        if user.current_day_id is None or user.current_day_id not in valid_day_ids:
            user.current_day_id = user.beginning_day_id
            db.session.commit()

        day = Day_of_routine.query.filter_by(id=user.current_day_id).first()
        if day is None:
            user.current_day_id = routine.workouts[0].id
            db.session.commit()
            day = Day_of_routine.query.filter_by(id=user.current_day_id).first()

        workout_day = add_links_to_routine_days(day, Workouts.query.all())
        return render_template(
            "day.html", workout_day=workout_day, day=day.workout_day_name, user=user
        )
    else:
        return redirect(url_for("login"))


@app.route("/change_day_id", methods=["POST", "GET"])
def change_day_id():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = User.query.filter_by(id=session["user_id"]).first()
    routine = Routine.query.filter_by(id=user.user_routine).first()

    workout_names = request.form.getlist("workout_names")
    sets_list     = request.form.getlist("sets")
    reps_list     = request.form.getlist("reps")
    weight_list   = request.form.getlist("weight")

    for i, workout_name in enumerate(workout_names):
        sets   = int(sets_list[i])   if i < len(sets_list)   and sets_list[i]   else 0
        reps   = int(reps_list[i])   if i < len(reps_list)   and reps_list[i]   else 0
        weight = int(weight_list[i]) if i < len(weight_list) and weight_list[i] else 0
        progress = UserProgress(
            workout_done=workout_name,
            sets=sets,
            reps=reps,
            weight_lifted=weight,
            date=date.today(),
            user_id=user.id,
        )
        db.session.add(progress)

    day_ids = [d.id for d in routine.workouts]
    if user.current_day_id not in day_ids:
        user.current_day_id = user.beginning_day_id
    else:
        idx = day_ids.index(user.current_day_id)
        user.current_day_id = day_ids[(idx + 1) % len(day_ids)]

    db.session.commit()
    return redirect(url_for("day"))


@app.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    from itsdangerous import URLSafeTimedSerializer
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        user = User.query.filter_by(email=email).first()
        flash("If that email is registered you'll receive a reset link shortly.")
        if user:
            s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
            token = s.dumps(email, salt="password-reset")
            reset_url = url_for("reset_password", token=token, _external=True)
            try:
                msg = Message(
                    subject="TalaveraTraining — Password Reset",
                    sender=app.config["MAIL_USERNAME"],
                    recipients=[email],
                    body=(
                        f"Hi {user.first_name},\n\n"
                        f"Click the link below to reset your password. "
                        f"This link expires in 1 hour.\n\n"
                        f"{reset_url}\n\n"
                        f"If you didn't request this, ignore this email.\n\n"
                        f"— TalaveraTraining"
                    ),
                )
                mail.send(msg)
            except Exception as e:
                print(f"Email error: {e}")
        return redirect(url_for("login"))
    return render_template("forgot_password.html")


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
    s = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = s.loads(token, salt="password-reset", max_age=3600)
    except SignatureExpired:
        flash("This reset link has expired. Please request a new one.")
        return redirect(url_for("forgot_password"))
    except BadSignature:
        flash("Invalid reset link.")
        return redirect(url_for("forgot_password"))
    if request.method == "POST":
        password = request.form.get("password", "")
        confirm  = request.form.get("confirm_password", "")
        if len(password) < 6:
            flash("Password must be at least 6 characters.")
            return render_template("reset_password.html", token=token)
        if password != confirm:
            flash("Passwords do not match.")
            return render_template("reset_password.html", token=token)
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = password
            db.session.commit()
            flash("Password updated! You can now log in.")
        return redirect(url_for("login"))
    return render_template("reset_password.html", token=token)


@app.route("/progress")
def progress_history():
    if "user_id" not in session:
        return redirect(url_for("login"))
    entries = UserProgress.query.filter_by(user_id=session["user_id"]).order_by(
        UserProgress.date.desc(), UserProgress.id.desc()
    ).all()
    return render_template("progress.html", entries=entries)


@app.route("/progress/edit/<int:progress_id>", methods=["GET", "POST"])
def edit_progress(progress_id):
    if "user_id" not in session:
        return redirect(url_for("login"))
    progress = UserProgress.query.filter_by(
        id=progress_id, user_id=session["user_id"]
    ).first()
    if not progress:
        flash("Progress entry not found.")
        return redirect(url_for("progress_history"))
    if request.method == "POST":
        progress.sets          = int(request.form.get("sets", 0) or 0)
        progress.reps          = int(request.form.get("reps", 0) or 0)
        progress.weight_lifted = int(request.form.get("weight", 0) or 0)
        db.session.commit()
        flash("Progress updated!")
        return redirect(url_for("progress_history"))
    return render_template("edit_progress.html", progress=progress)


@app.route("/contact_us", methods=["POST", "GET"])
def contact_us():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            msg = Message(
                subject="Contact form submission",
                sender=form.email.data,
                recipients=["jcruz6003@gmail.com"],
                body=f"Message from: {form.name.data}\nEmail: {form.email.data}\n\nMessage:\n{form.message.data}",
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