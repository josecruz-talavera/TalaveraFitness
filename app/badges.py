from datetime import date, timedelta


# Badge definitions — easy to add more here later
BADGE_DEFINITIONS = [
    {
        "id": "first_workout",
        "name": "First Step",
        "description": "Completed your first workout",
        "icon": "🏁",
        "color": "#27ae60",
    },
    {
        "id": "sessions_10",
        "name": "Getting Started",
        "description": "Logged 10 sessions",
        "icon": "💪",
        "color": "#2980b9",
    },
    {
        "id": "sessions_50",
        "name": "Dedicated",
        "description": "Logged 50 sessions",
        "icon": "🔥",
        "color": "#e67e22",
    },
    {
        "id": "sessions_100",
        "name": "Century Club",
        "description": "Logged 100 sessions",
        "icon": "🏆",
        "color": "#f1c40f",
    },
    {
        "id": "streak_7",
        "name": "Week Warrior",
        "description": "7-day training streak",
        "icon": "⚡",
        "color": "#8e44ad",
    },
    {
        "id": "streak_30",
        "name": "Unstoppable",
        "description": "30-day training streak",
        "icon": "👑",
        "color": "#c0392b",
    },
    {
        "id": "first_pr",
        "name": "Personal Best",
        "description": "Beat your own weight record on an exercise",
        "icon": "🎯",
        "color": "#16a085",
    },
    {
        "id": "consistency_king",
        "name": "Consistency King",
        "description": "Logged 30 sessions in a single month",
        "icon": "📅",
        "color": "#d35400",
    },
]


def compute_badges(user, progress_entries):
    """
    Given a user and their list of UserProgress entries,
    return a list of earned badge dicts and a list of locked badge dicts.
    """
    earned_ids = set()

    # Distinct dates trained
    trained_dates = sorted(
        set(e.date for e in progress_entries), reverse=True
    )
    total_sessions = len(trained_dates)

    # --- Session milestones ---
    if total_sessions >= 1:
        earned_ids.add("first_workout")
    if total_sessions >= 10:
        earned_ids.add("sessions_10")
    if total_sessions >= 50:
        earned_ids.add("sessions_50")
    if total_sessions >= 100:
        earned_ids.add("sessions_100")

    # --- Streak ---
    streak = 0
    check = date.today()
    for d in trained_dates:
        if d == check or d == check - timedelta(days=1):
            streak += 1
            check = d - timedelta(days=1)
        else:
            break

    if streak >= 7:
        earned_ids.add("streak_7")
    if streak >= 30:
        earned_ids.add("streak_30")

    # --- Personal Record ---
    # Group by exercise, check if any entry beat a previous max weight
    exercise_maxes = {}
    for entry in sorted(progress_entries, key=lambda e: (e.date, e.id)):
        name = entry.workout_done
        if name not in exercise_maxes:
            exercise_maxes[name] = entry.weight_lifted or 0
        else:
            if (entry.weight_lifted or 0) > exercise_maxes[name]:
                earned_ids.add("first_pr")
                exercise_maxes[name] = entry.weight_lifted

    # --- Consistency King: 30 sessions in one calendar month ---
    from collections import defaultdict
    month_counts = defaultdict(set)
    for e in progress_entries:
        month_counts[(e.date.year, e.date.month)].add(e.date)
    if any(len(days) >= 30 for days in month_counts.values()):
        earned_ids.add("consistency_king")

    # Build result lists
    earned = []
    locked = []
    for badge in BADGE_DEFINITIONS:
        if badge["id"] in earned_ids:
            earned.append(badge)
        else:
            locked.append(badge)

    return earned, locked, streak, total_sessions