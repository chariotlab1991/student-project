"""Generate dummy CSV data for the edtech dataset."""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
NUM_STUDENTS = 300


def generate_students() -> list[dict[str, str]]:
    """Create student profiles with deterministic but varied attributes."""
    locales = [
        "en_US",
        "en_IN",
        "en_GB",
        "es_ES",
        "fr_FR",
        "de_DE",
        "pt_BR",
        "hi_IN",
        "zh_CN",
        "ja_JP",
    ]
    device_types = ["mobile", "desktop", "tablet"]

    students: list[dict[str, str]] = []
    for student_id in range(1, NUM_STUDENTS + 1):
        if student_id == 1:
            students.append(
                {"id": "1", "age": "22", "locale": "en_US", "device_type": "mobile"}
            )
            continue
        if student_id == 2:
            students.append(
                {"id": "2", "age": "19", "locale": "en_IN", "device_type": "desktop"}
            )
            continue

        age = str(random.randint(18, 55))
        locale = locales[(student_id + random.randint(0, len(locales) - 1)) % len(locales)]
        device_type = device_types[(student_id + random.randint(0, len(device_types) - 1)) % len(device_types)]

        students.append(
            {"id": str(student_id), "age": age, "locale": locale, "device_type": device_type}
        )

    return students


def generate_courses() -> list[dict[str, str]]:
    """Define a fixed course catalog, preserving existing course entries."""
    courses = [
        {"id": "101", "subject": "Python", "level": "beginner", "est_hours": "20"},
        {"id": "102", "subject": "Data Science", "level": "intermediate", "est_hours": "40"},
        {"id": "103", "subject": "Web Development", "level": "beginner", "est_hours": "25"},
        {"id": "104", "subject": "Machine Learning", "level": "advanced", "est_hours": "60"},
        {"id": "105", "subject": "Cloud Computing", "level": "intermediate", "est_hours": "35"},
        {"id": "106", "subject": "Cybersecurity", "level": "beginner", "est_hours": "30"},
        {"id": "107", "subject": "UI/UX Design", "level": "beginner", "est_hours": "20"},
        {"id": "108", "subject": "Data Engineering", "level": "advanced", "est_hours": "55"},
    ]
    return courses


def generate_enrollments(students: list[dict[str, str]], courses: list[dict[str, str]]) -> list[dict[str, str]]:
    """Assign each student to a course cohort and enrollment date."""
    start_date = date(2024, 1, 10)
    cohorts = ["A", "B", "C", "D"]
    enrollments: list[dict[str, str]] = []

    for index, student in enumerate(students):
        course = courses[index % len(courses)]
        cohort = cohorts[index % len(cohorts)]
        enrolled_at = start_date + timedelta(days=(index % 60))

        enrollments.append(
            {
                "student_id": student["id"],
                "course_id": course["id"],
                "cohort": cohort,
                "enrolled_at": enrolled_at.isoformat(),
            }
        )

    return enrollments


def generate_events(enrollments: list[dict[str, str]]) -> list[dict[str, str]]:
    """Create two basic event records per enrollment: a video watch and a quiz submission."""
    events: list[dict[str, str]] = []

    for enrollment in enrollments:
        student_id = enrollment["student_id"]
        course_id = enrollment["course_id"]
        enrolled_at = date.fromisoformat(enrollment["enrolled_at"])

        # Video watch event
        video_seconds = random.randint(180, 480)
        events.append(
            {
                "student_id": student_id,
                "course_id": course_id,
                "ts": enrolled_at.isoformat(),
                "event_type": "video_watch",
                "seconds_spent": str(video_seconds),
                "score_delta": "0",
            }
        )

        # Quiz submission event one day later
        quiz_seconds = random.randint(60, 180)
        score_delta = random.randint(0, 10)
        events.append(
            {
                "student_id": student_id,
                "course_id": course_id,
                "ts": (enrolled_at + timedelta(days=1)).isoformat(),
                "event_type": "quiz_submit",
                "seconds_spent": str(quiz_seconds),
                "score_delta": str(score_delta),
            }
        )

    # Override the first student's events to match the original sample data.
    events[0] = {
        "student_id": "1",
        "course_id": "101",
        "ts": "2024-01-10",
        "event_type": "video_watch",
        "seconds_spent": "300",
        "score_delta": "0",
    }
    events[1] = {
        "student_id": "1",
        "course_id": "101",
        "ts": "2024-01-11",
        "event_type": "quiz_submit",
        "seconds_spent": "100",
        "score_delta": "5",
    }

    return events


def generate_outcomes(enrollments: list[dict[str, str]]) -> list[dict[str, str]]:
    """Create a course outcome per enrollment with simple mastery and drop indicators."""
    outcomes: list[dict[str, str]] = []

    for index, enrollment in enumerate(enrollments):
        dropped = 1 if random.random() < 0.12 else 0
        if enrollment["student_id"] == "1":
            final_mastery = 80
            dropped = 0
        elif dropped:
            final_mastery = random.randint(0, 40)
        else:
            final_mastery = random.randint(60, 100)

        outcomes.append(
            {
                "student_id": enrollment["student_id"],
                "course_id": enrollment["course_id"],
                "final_mastery_pct": str(final_mastery),
                "dropped": str(dropped),
            }
        )

    return outcomes


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    random.seed(42)

    students = generate_students()
    courses = generate_courses()
    enrollments = generate_enrollments(students, courses)
    events = generate_events(enrollments)
    outcomes = generate_outcomes(enrollments)

    write_csv(
        DATA_DIR / "students.csv",
        ["id", "age", "locale", "device_type"],
        students,
    )
    write_csv(
        DATA_DIR / "courses.csv",
        ["id", "subject", "level", "est_hours"],
        courses,
    )
    write_csv(
        DATA_DIR / "enrollments.csv",
        ["student_id", "course_id", "cohort", "enrolled_at"],
        enrollments,
    )
    write_csv(
        DATA_DIR / "events.csv",
        ["student_id", "course_id", "ts", "event_type", "seconds_spent", "score_delta"],
        events,
    )
    write_csv(
        DATA_DIR / "outcomes.csv",
        ["student_id", "course_id", "final_mastery_pct", "dropped"],
        outcomes,
    )


if __name__ == "__main__":
    main()
