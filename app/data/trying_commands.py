from app.models import Workouts
from app.starting_app import app

import subprocess
"""
li = []
result = subprocess.run(
    ["ls", "/Users/kenpachi/my_projects/PT_flask"], capture_output=True, text=True
)
mov_vids = subprocess.run(
    ["ls", "/Users/kenpachi/Desktop/brisblogsunformattedvids"],
    capture_output=True,
    text=True,
)
# Print the output
print(result.stdout.split())
print(mov_vids.stdout.split())

for vid in mov_vids.stdout.split():
    split_vid = vid.split(".")
    # print(split_vid[0])
    # print("/Users/kenpachi/Desktop/Causey/Formatted_workout_vids/" + split_vid[0] + ".mp4")

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            "/Users/kenpachi/Desktop/brisblogsunformattedvids/" + vid,  # Input file
            "-vcodec",
            "h264",  # Video codec
            "-acodec",
            "aac",  # Audio codec
            "/Users/kenpachi/Desktop/talaverafitness/Formatted_workout_vids/"
            + split_vid[0]
            + ".mp4",  # Output file
        ]
    )
# the command to format videos
# ffmpeg -i video.mov -vcodec h264 -acodec aac video.mp4
# pwd /Users/kenpachi/my_projects/PT_flask

"""
with app.app_context():
    workouts_without_links = []
    for workout in Workouts.query.all():
        
        if workout.workout_link == "":
            workouts_without_links.append(workout.workout_name)
    for w in sorted(workouts_without_links):
        print(w)
    
    print(len(workouts_without_links))
  
