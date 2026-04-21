import pytest
import os

PT_flask = os.environ["PWD"]
import sys

sys.path.insert(0, PT_flask)

from app.starting_app import app
from app.models import db, Test_day

from app.day import add_a_day_to_db, days
from testing_data import fake


class Test_Day_Functions:

    def test_add_a_day_to_db(self):
        with app.app_context():

            day = add_a_day_to_db(Test_day, "chest", fake.day())

        assert (day.workout_day_name, day.w1, day.w2, day.w3, day.w4) == (
            "chest",
            "incline barbell chest press",
            "flat barbell bench press",
            "decline barbell bench press",
            "rope pulldowns",
        )
