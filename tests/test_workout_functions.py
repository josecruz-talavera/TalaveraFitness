import pytest
import os
import random
PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)

from app.workout_functions import (
    filter_video_name,
    video_to_add_to_model,
    add_links_to_routine_days,
    add_workouts_to_model,
    
)
from app.starting_app import app
from app.models import db, Test_Workouts, Workouts
from testing_data import fake, Day_data, workouts


class Test_Workout_Functions:



    def test_filter_video_name(self):

        assert (
            filter_video_name(
                "https://causey.s3.us-east-2.amazonaws.com/workout_pics/incline_barbell_benchpress.mov",
                "workout_pics"
            )
            == "incline barbell benchpress"
        )
    """
    def test_video_to_add_to_model(self):
        assert (
            video_to_add_to_model(
                "incline barbell benchpress",
                [
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_dumbell_press.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/dumbell_bench_press.mov",
                ], "workout_vids"
            )
            == "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov"
            
        )
"""
    def test_video_does_not_exist(self):
        assert (
            video_to_add_to_model(
                "pike push ups",
                [
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_dumbell_press.mov",
                    "https://causey.s3.us-east-2.amazonaws.com/workout_vids/dumbell_bench_press.mov",
                ], "workout_vids"
            )
            == "https://causey.s3.us-east-2.amazonaws.com/workout_pics/no_image.JPG"
            
        )

    """

    def test_add_links_to_routine_days(self):
        

        assert add_links_to_routine_days(
            Day_data(fake),
            workouts
        ) == {
            "decline barbell benchpress": "https://causey.s3.us-east-2.amazonaws.com/workout_vids/decline_barbell_benchpress.mp4",
            "dumbell bench press": "https://causey.s3.us-east-2.amazonaws.com/workout_vids/dumbell_bench_press.mp4",
            "incline barbell benchpress": "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mp4",
            "rope pulldown": "https://causey.s3.us-east-2.amazonaws.com/workout_vids/rope_pulldown.mp4",
            "overhead tricep extension": "https://causey.s3.us-east-2.amazonaws.com/workout_vids/overhead_tricep_extension.mp4",
        }
"""