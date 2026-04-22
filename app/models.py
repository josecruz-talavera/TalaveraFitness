from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_admin.contrib.sqla import ModelView
from flask import Flask, redirect, render_template, request, flash, url_for, session
from wtforms import PasswordField, StringField, Form, IntegerField, DateField
from wtforms.validators import DataRequired, Email, Optional
from datetime import date, timedelta

db = SQLAlchemy()


class Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)
    workout_pic_link = db.Column(db.String, nullable=True)


class WorkoutForm(Form):
    workout_name = StringField('Workout Name', validators=[DataRequired()])
    body_part = StringField('Body Part', validators=[DataRequired()])
    muscle_targeted = StringField('Muscle Targeted', validators=[Optional()])
    workout_link = StringField('Workout Link', validators=[Optional()])
    workout_pic_link = StringField('Workout PIC', validators=[Optional()])


class WorkoutsView(ModelView):
    column_list = ["id", "workout_name", "body_part", "muscle_targeted", "workout_link", "workout_pic_link"]
    column_searchable_list = ["workout_name", "muscle_targeted"]
    form = WorkoutForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating workout: {str(e)}", "error")


class Test_Workouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)
    workout_link = db.Column(db.String, nullable=True)
    workout_pic_link = db.Column(db.String, nullable=True)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(20), nullable=True)
    beginning_day_id = db.Column(db.Integer, nullable=True)
    current_day_id = db.Column(db.Integer, nullable=True)
    routine_change_date = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(50))
    level = db.Column(db.String)
    days_logged_in = db.Column(db.Integer)
    user_routine = db.Column(db.Integer, db.ForeignKey("routine.id"))
    progress = db.relationship("UserProgress", back_populates="user", lazy=True)


class UserForm(Form):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = StringField('Role', validators=[Optional()])
    level = StringField('Level', validators=[Optional()])
    user_routine = IntegerField('User Routine', validators=[Optional()])
    days_logged_in = IntegerField('Days Logged In', validators=[Optional()])
    routine_change_date = DateField('Routine Change Date', validators=[Optional()])
    goal = StringField('Goal', validators=[Optional()])
    beginning_day_id = IntegerField('Beginning Day ID', validators=[Optional()])
    current_day_id = IntegerField('Current Day ID', validators=[Optional()])


class UserView(ModelView):
    column_list = [
        "id",
        "username",
        "email",
        "first_name",
        "last_name",
        "user_routine",
        "role",
        "level",
        "days_logged_in",
        "routine_change_date",
        "progress"
    ]
    
    form = UserForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            if is_created:
                model.password = form.password.data
                # Set default values for new users
                model.days_logged_in = 0
                model.routine_change_date = date.today() + timedelta(weeks=6)
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user: {str(e)}", "error")

    def on_model_delete(self, model):
        try:
            super().on_model_delete(model)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error deleting user: {str(e)}", "error")


class UserProgress(db.Model):
    __tablename__ = "user_progress"
    id = db.Column("id", db.Integer, primary_key=True)
    workout_done = db.Column(db.String)
    sets = db.Column(db.Integer)
    reps = db.Column(db.Integer)
    weight_lifted = db.Column(db.Integer)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", back_populates="progress")


class UserProgressForm(Form):
    sets = IntegerField('Sets', validators=[DataRequired()])


class UserProgressView(ModelView):
    column_list = ["id", "sets", "reps", "weight_lifted", "date"]
    form = UserProgressForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user progress: {str(e)}", "error")


class Test_User(db.Model):
    __tablename__ = "test_users"
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    goal = db.Column(db.String(20), nullable=True)
    beginning_day_id = db.Column(db.Integer, nullable=True)
    current_day_id = db.Column(db.Integer, nullable=True)
    routine_change_date = db.Column(db.Date, nullable=True)
    role = db.Column(db.String(50))
    level = db.Column(db.String, nullable=False)
    days_logged_in = db.Column(db.Integer)
    user_routine = db.Column(db.Integer, db.ForeignKey("routine.id"))


# each user will have their own routine set up to them
# here we will store our days for the routines


class Routine(db.Model):
    # routine could store just the day model
    __tablename__ = "routine"
    id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String, unique=True)
    workouts = db.relationship("Day_of_routine", backref="routine")
    routine_level = db.Column(db.String, nullable=True)
    users_with_routine = db.relationship("User", backref="routine")


class Day_of_routine(db.Model):

    # w stands for workout
    # Day could be the list of workouts that goes into Days
    id = db.Column(db.Integer, primary_key=True)
    workout_day_name = db.Column(db.String)
    w1 = db.Column(db.String)
    w2 = db.Column(db.String)
    w3 = db.Column(db.String)
    w4 = db.Column(db.String)
    w5 = db.Column(db.String, nullable=True)
    w6 = db.Column(db.String, nullable=True)
    w7 = db.Column(db.String, nullable=True)
    w8 = db.Column(db.String, nullable=True)

    routine_name = db.Column(db.String, db.ForeignKey("routine.routine_name"))


class RoutineForm(Form):
    routine_name = StringField('Routine Name', validators=[DataRequired()])
    routine_level = StringField('Routine Level', validators=[DataRequired()])


class RoutineView(ModelView):
    column_list = [
        "id",
        "routine_name",
        "workouts",
        "routine_level",
        "users_with_routine",
    ]
    form = RoutineForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating routine: {str(e)}", "error")


class DayForm(Form):
    workout_day_name = StringField('Workout Day Name', validators=[DataRequired()])
    w1 = StringField('Workout 1', validators=[Optional()])
    w2 = StringField('Workout 2', validators=[Optional()])
    w3 = StringField('Workout 3', validators=[Optional()])
    w4 = StringField('Workout 4', validators=[Optional()])
    w5 = StringField('Workout 5', validators=[Optional()])
    w6 = StringField('Workout 6', validators=[Optional()])
    w7 = StringField('Workout 7', validators=[Optional()])
    w8 = StringField('Workout 8', validators=[Optional()])
    routine_name = StringField('Routine Name', validators=[DataRequired()])


class DayView(ModelView):
    column_list = [
        "id",
        "workout_day_name",
        "w1",
        "w2",
        "w3",
        "w4",
        "w5",
        "w6",
        "w7",
        "w8",
        "routine_name",
    ]
    form = DayForm

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login"))

    def on_model_change(self, form, model, is_created):
        try:
            super().on_model_change(form, model, is_created)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating day: {str(e)}", "error")


class Test_Day_of_routine(db.Model):

    # w stands for workout
    # Day could be the list of workouts that goes into Days
    id = db.Column(db.Integer, primary_key=True)
    workout_day_name = db.Column(db.String)
    w1 = db.Column(db.String)
    w2 = db.Column(db.String)
    w3 = db.Column(db.String)
    w4 = db.Column(db.String)
    w5 = db.Column(db.String, nullable=True)
    w6 = db.Column(db.String, nullable=True)
    w7 = db.Column(db.String, nullable=True)
    w8 = db.Column(db.String, nullable=True)

    routine_name = db.Column(db.String, db.ForeignKey("routine.routine_name"))


class Test_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_name = db.Column(db.String, nullable=False)
    body_part = db.Column(db.String)
    muscle_targeted = db.Column(db.String, nullable=True)


class AdminView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("day"))  # Redirect non-admins to login


# Custom admin view
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == "admin"

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("day"))
