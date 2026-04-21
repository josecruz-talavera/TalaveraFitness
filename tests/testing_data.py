from faker import Faker
import random

fake = Faker()

from faker.providers import BaseProvider

class Workout:
    def __init__(self, workout_name, body_part, muscle_targeted, workout_link, workout_pic_link):
        self.workout_name = workout_name
        self.body_part = body_part
        self.muscle_targeted = muscle_targeted
        self.workout_link = workout_link
        self.workout_pic_link = workout_pic_link




workouts = [
    Workout("decline barbell benchpress", "", "", "https://causey.s3.us-east-2.amazonaws.com/workout_vids/decline_barbell_benchpress.mp4", ""),
    Workout("dumbell bench press", "", "", "https://causey.s3.us-east-2.amazonaws.com/workout_vids/dumbell_bench_press.mp4", ""),
    Workout("incline barbell benchpress", "", "", "https://causey.s3.us-east-2.amazonaws.com/workout_vids/incline_barbell_benchpress.mp4", ""),
    Workout("rope pulldown", "", "", "https://causey.s3.us-east-2.amazonaws.com/workout_vids/rope_pulldown.mp4", ""),
    Workout("overhead tricep extension", "", "", "https://causey.s3.us-east-2.amazonaws.com/workout_vids/overhead_tricep_extension.mp4", ""),
]

class Day_data(BaseProvider):

    routine_name = "Free weight and cables"

    workout_day_name = "chest and triceps"
    w1 = "incline barbell benchpress"
    w2 = "dumbell bench press"

    w3 = "decline barbell benchpress"

    w4 = "overhead tricep extension"

    w5 = "rope pulldown"


fake.add_provider(Day_data)
