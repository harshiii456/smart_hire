from datetime import datetime, timedelta

def generate_time_slots(start_time="10:00", end_time="21:00", interval_minutes=30):
    """
    Generate 30-minute time slots between start_time and end_time.
    """
    slots = []
    current = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    while current < end:
        slots.append(current.strftime("%I:%M %p"))
        current += timedelta(minutes=interval_minutes)
    return slots

def schedule_interviews(candidates: list) -> list:
    """
    Assigns interview date and time to shortlisted candidates.
    Moves to the next day if all slots are filled.
    """
    print("📅 Scheduling interviews...")

    # Start from the day after today
    start_day = datetime.now() + timedelta(days=1)
    time_slots = generate_time_slots()
    total_slots = len(time_slots)

    for i, candidate in enumerate(candidates):
        interview_day = start_day + timedelta(days=i // total_slots)
        time_slot = time_slots[i % total_slots]

        candidate["interview_date"] = interview_day.strftime("%Y-%m-%d")
        candidate["interview_time"] = time_slot
        candidate["status"] = "scheduled"

        print(f"📍 {candidate['name']} scheduled at {time_slot} on {candidate['interview_date']}")

    return candidates
