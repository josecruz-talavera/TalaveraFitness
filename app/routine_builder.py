from flask_sqlalchemy import SQLAlchemy
from app.starting_app import app
from app.models import Workouts, db
import random


def make_routine(
    model,
    body_part,
    muscle_targeted1=None,
    muscle_targeted2=None,
    muscle_targeted3=None,
    muscle_targeted4=None,
    muscle_targeted5=None,
):
    day = []
    if body_part == "chest":

        muscles_targeted = [muscle_targeted1, muscle_targeted2, muscle_targeted3, muscle_targeted4]

        for muscle in muscles_targeted:

            workout = random.choice(model.query.filter_by(muscle_targeted=muscle).all())

            if workout not in day:

                day.append(workout.workout_name)
    elif body_part == "back":

        while len(day) <= 4:
            workout = random.choice(model.query.filter_by(body_part=body_part).all())

            if workout not in day:
                day.append(workout.workout_name)

    elif body_part == "legs":
        muscles_targeted = [muscle_targeted1, muscle_targeted2, muscle_targeted3, muscle_targeted4, muscle_targeted5]

        for muscle in muscles_targeted:

            workout = random.choice(model.query.filter_by(muscle_targeted=muscle).all())

            if workout not in day:

                day.append(workout.workout_name)
    
    elif body_part == "arms":
        muscles_targeted = [muscle_targeted1, muscle_targeted2, muscle_targeted3, muscle_targeted4, muscle_targeted5]

        for muscle in muscles_targeted:

            workout = random.choice(model.query.filter_by(muscle_targeted=muscle).all())

            if workout not in day:

                day.append(workout.workout_name)

    return day


def main():

    print("'Chest': \n", make_routine(Workouts, "chest", "upper chest", "mid chest", "lower chest", "mid deltoids"), ",")
    
    print("'Back': \n", make_routine(Workouts, "back"), ",")

    print("'Legs': \n", make_routine(Workouts, "legs", "fundamental legs", "glutes", "quads", "hamstrings", "calves"), ",")
    print("'Arms': \n", make_routine(Workouts, "arms", "anterior deltoids", "triceps", "triceps", "biceps", "biceps"), ",")


if __name__ == "__main__":
    with app.app_context():
        main()
