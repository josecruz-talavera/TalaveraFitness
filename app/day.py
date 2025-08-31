"""
This file takes the data in all_routines.py and adds them to our days_of_routine model.
"""

import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)
from flask_sqlalchemy import SQLAlchemy
from app.models import db, Day_of_routine
from app.starting_app import app
from app.all_routines import routines


def add_days_to_routine(model, routine, routine_name):

    for workout_day in routine:

        if len(routine[workout_day]) == 8:
            d = model(
                workout_day_name=workout_day,
                w1=routine[workout_day][0],
                w2=routine[workout_day][1],
                w3=routine[workout_day][2],
                w4=routine[workout_day][3],
                w5=routine[workout_day][4],
                w6=routine[workout_day][5],
                w7=routine[workout_day][6],
                w8=routine[workout_day][7],
                routine_name=routine_name,
            )

        elif len(routine[workout_day]) == 6:
            d = model(
                workout_day_name=workout_day,
                w1=routine[workout_day][0],
                w2=routine[workout_day][1],
                w3=routine[workout_day][2],
                w4=routine[workout_day][3],
                w5=routine[workout_day][4],
                w6=routine[workout_day][5],
                routine_name=routine_name,
            )

        else:
            d = model(
                workout_day_name=workout_day,
                w1=routine[workout_day][0],
                w2=routine[workout_day][1],
                w3=routine[workout_day][2],
                w4=routine[workout_day][3],
                w5=routine[workout_day][4],
                routine_name=routine_name,
            )
        db.session.add(d)

    return d


def main():
    for routine in routines:
        routine_in_db = Day_of_routine.query.filter_by(routine_name=routine).first()
        if routine_in_db:
            print(f"Routine {routine} already exists")
        else:
            added_day = add_days_to_routine(Day_of_routine, routines[routine], routine)
            db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
