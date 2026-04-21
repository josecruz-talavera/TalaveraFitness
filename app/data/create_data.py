"""
This file is used to create the data inserting into the workouts model.
"""
from app.starting_app import app
from app.user_functions import create_user
from app.workout_functions import (
    add_workouts_to_model,
    list_of_videos,
)
from app.models import Workouts, db, User
from info_to_insert import *



def main():

    create_user(
        User,
        "jcruz6003",
        "jcruz6003@gmail.com",
        "jose",
        "cruz",
        "loka1234",
        "build_muscle",
        "beginner",
        "admin",
        None,
    )
    create_user(
        User,
        "chris",
        "chris6003@gmail.com",
        "Christian",
        "Causey",
        "loka1234",
        "build_muscle",
        "advanced",
        None,
        1,
    )
    create_user(
        User,
        "juan1975",
        "juantech2011@gmail.com",
        "juan",
        "echevarria",
        "Moses711",
        "build_muscle",
        "advanced",
        None,
        1,
    )
    add_workouts_to_model(
        Workouts, upper_chest_workouts, "chest", "upper chest", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, mid_chest_workouts, "chest", "mid chest", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, lower_chest_workouts, "chest", "lower chest", list_of_videos()
    )
    add_workouts_to_model(Workouts, workouts_for_back, "back", None, list_of_videos())
    add_workouts_to_model(
        Workouts,
        front_delt_workouts,
        "shoulders",
        "anterior deltoids",
        list_of_videos(),
    )
    add_workouts_to_model(
        Workouts,
        mid_delt_workouts,
        "shoulders",
        "mid deltoids",
        list_of_videos(),
    )
    add_workouts_to_model(
        Workouts,
        rear_delt_workouts,
        "shoulders",
        "rear deltoids",
        list_of_videos(),
    )
    add_workouts_to_model(
        Workouts, workouts_for_tricep, "arms", "triceps", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_bicep, "arms", "biceps", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_legs, "legs", "fundamental legs", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_glutes, "legs", "glutes", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_groin, "legs", "groin", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_quads, "legs", "quads", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_hamstrings, "legs", "hamstrings", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, workouts_for_calves, "legs", "calves", list_of_videos()
    )

    add_workouts_to_model(
        Workouts, upper_abs_workouts, "abdomen", "abs", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, lower_abs_workouts, "abdomen", "abs", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, sixpack_workouts, "abdomen", "abs", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, oblique_workouts, "abdomen", "abs", list_of_videos()
    )
    add_workouts_to_model(
        Workouts, complete_abs_workouts, "abdomen", "abs", list_of_videos()
    )
    add_workouts_to_model(Workouts, core_workouts, "abdomen", "abs", list_of_videos())
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        main()
