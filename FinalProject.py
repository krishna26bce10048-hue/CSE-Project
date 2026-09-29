from datetime import datetime


subjects = []


def line():
    print("=" * 65)


def pause():
    input("\nPress Enter to continue...")


def get_positive_number(message):
    while True:
        value = input(message).strip()

        try:
            value = float(value)

            if value > 0:
                return value

            print("Enter a number greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_percentage(message):
    while True:
        value = input(message).strip()

        try:
            value = float(value)

            if 0 <= value <= 100:
                return value

            print("Enter a percentage between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")


def get_difficulty():
    while True:
        print("\nDifficulty Level")
        print("1. Easy")
        print("2. Medium")
        print("3. Hard")

        choice = input("Choose difficulty: ").strip()

        if choice == "1":
            return "Easy"

        elif choice == "2":
            return "Medium"

        elif choice == "3":
            return "Hard"

        else:
            print("Invalid choice.")


def get_exam_date():
    while True:
        date = input("Enter exam date (DD-MM-YYYY): ").strip()

        try:
            exam_date = datetime.strptime(date, "%d-%m-%Y")
            today = datetime.now()

            if exam_date.date() >= today.date():
                return exam_date

            print("Exam date cannot be in the past.")

        except ValueError:
            print("Enter the date in DD-MM-YYYY format.")


def calculate_days_left(exam_date):
    today = datetime.now()
    difference = exam_date.date() - today.date()
    return difference.days


def calculate_priority(subject):
    difficulty_score = {
        "Easy": 1,
        "Medium": 2,
        "Hard": 3
    }

    difficulty = difficulty_score[subject["difficulty"]]

    days_left = subject["days_left"]

    if days_left <= 0:
        urgency = 10
    elif days_left <= 2:
        urgency = 10
    elif days_left <= 5:
        urgency = 8
    elif days_left <= 10:
        urgency = 6
    elif days_left <= 20:
        urgency = 4
    else:
        urgency = 2

    preparation_score = (100 - subject["preparation"]) / 10

    priority = (
        difficulty * 3
        + urgency * 4
        + preparation_score * 3
    )

    return round(priority, 2)


def get_priority_level(priority):
    if priority >= 70:
        return "Very High"

    elif priority >= 50:
        return "High"

    elif priority >= 30:
        return "Medium"

    else:
        return "Low"


def add_subject():
    line()
    print("ADD NEW SUBJECT")
    line()

    name = input("Enter subject name: ").strip()

    if name == "":
        print("Subject name cannot be empty.")
        return

    for subject in subjects:
        if subject["name"].lower() == name.lower():
            print("This subject already exists.")
            return

    chapters = int(
        get_positive_number("Enter number of chapters: ")
    )

    difficulty = get_difficulty()

    preparation = get_percentage(
        "Enter current preparation percentage: "
    )

    exam_date = get_exam_date()

    study_hours = get_positive_number(
        "Available study hours per day: "
    )

    days_left = calculate_days_left(exam_date)

    subject = {
        "name": name,
        "chapters": chapters,
        "completed_chapters": 0,
        "difficulty": difficulty,
        "preparation": preparation,
        "exam_date": exam_date,
        "days_left": days_left,
        "study_hours": study_hours,
        "priority": 0,
        "priority_level": ""
    }

    subject["priority"] = calculate_priority(subject)

    subject["priority_level"] = get_priority_level(
        subject["priority"]
    )

    subjects.append(subject)

    print()
    print("Subject added successfully!")
    print(f"Priority: {subject['priority_level']}")


def display_subject(subject, number=None):
    if number is not None:
        print(f"\nSubject {number}")

    print(f"Name: {subject['name']}")
    print(f"Chapters: {subject['chapters']}")
    print(f"Completed Chapters: {subject['completed_chapters']}")
    print(f"Difficulty: {subject['difficulty']}")
    print(f"Preparation: {subject['preparation']}%")
    print(
        f"Exam Date: {subject['exam_date'].strftime('%d-%m-%Y')}"
    )
    print(f"Days Left: {subject['days_left']}")
    print(f"Study Hours/Day: {subject['study_hours']}")
    print(f"Priority Score: {subject['priority']}")
    print(f"Priority Level: {subject['priority_level']}")


def view_subjects():
    line()
    print("ALL SUBJECTS")
    line()

    if len(subjects) == 0:
        print("No subjects added yet.")
        return

    for i, subject in enumerate(subjects, 1):
        display_subject(subject, i)


def find_subject():
    if len(subjects) == 0:
        print("No subjects available.")
        return None

    name = input("Enter subject name: ").strip()

    for subject in subjects:
        if subject["name"].lower() == name.lower():
            return subject

    print("Subject not found.")
    return None


def update_progress():
    line()
    print("UPDATE STUDY PROGRESS")
    line()

    subject = find_subject()

    if subject is None:
        return

    print(f"\nSubject: {subject['name']}")
    print(f"Current preparation: {subject['preparation']}%")
    print(
        f"Completed chapters: "
        f"{subject['completed_chapters']}/{subject['chapters']}"
    )

    print("\n1. Update preparation percentage")
    print("2. Update completed chapters")

    choice = input("Choose option: ").strip()

    if choice == "1":
        preparation = get_percentage(
            "Enter new preparation percentage: "
        )

        subject["preparation"] = preparation

    elif choice == "2":
        while True:
            try:
                completed = int(
                    input("Enter completed chapters: ")
                )

                if 0 <= completed <= subject["chapters"]:
                    subject["completed_chapters"] = completed
                    break

                print(
                    f"Enter a value between 0 and "
                    f"{subject['chapters']}."
                )

            except ValueError:
                print("Enter a valid whole number.")

    else:
        print("Invalid choice.")
        return

    subject["priority"] = calculate_priority(subject)

    subject["priority_level"] = get_priority_level(
        subject["priority"]
    )

    print("\nProgress updated successfully!")


def calculate_progress(subject):
    if subject["chapters"] == 0:
        return 0

    chapter_progress = (
        subject["completed_chapters"]
        / subject["chapters"]
    ) * 100

    average_progress = (
        chapter_progress + subject["preparation"]
    ) / 2

    return round(average_progress, 2)


def show_progress():
    line()
    print("STUDY PROGRESS")
    line()

    if len(subjects) == 0:
        print("No subjects available.")
        return

    total_progress = 0

    for subject in subjects:
        progress = calculate_progress(subject)

        total_progress += progress

        print(f"\n{subject['name']}")
        print(f"Progress: {progress}%")

        if progress >= 80:
            print("Status: Excellent")

        elif progress >= 60:
            print("Status: Good")

        elif progress >= 40:
            print("Status: Needs Improvement")

        else:
            print("Status: Needs Attention")

    overall = total_progress / len(subjects)

    print("\n" + "-" * 65)
    print(f"Overall Preparation: {round(overall, 2)}%")


def sort_by_priority():
    if len(subjects) == 0:
        print("No subjects available.")
        return []

    sorted_subjects = sorted(
        subjects,
        key=lambda subject: subject["priority"],
        reverse=True
    )

    return sorted_subjects


def generate_study_plan():
    line()
    print("SMART STUDY PLAN")
    line()

    if len(subjects) == 0:
        print("Add subjects first.")
        return

    sorted_subjects = sort_by_priority()

    total_hours = get_positive_number(
        "How many hours can you study today? "
    )

    remaining_hours = total_hours

    print("\nTODAY'S PLAN")
    print("-" * 65)

    for subject in sorted_subjects:

        if remaining_hours <= 0:
            break

        priority = subject["priority"]

        if priority >= 70:
            recommended = 2
        elif priority >= 50:
            recommended = 1.5
        elif priority >= 30:
            recommended = 1
        else:
            recommended = 0.5

        recommended = min(
            recommended,
            subject["study_hours"],
            remaining_hours
        )

        if recommended <= 0:
            continue

        print(
            f"{subject['name']}: "
            f"{recommended} hour(s)"
        )

        print(
            f"Reason: {subject['priority_level']} priority"
        )

        print(
            f"Exam in {subject['days_left']} day(s)"
        )

        remaining_hours -= recommended

    if remaining_hours > 0:
        print(
            f"\nFree study time remaining: "
            f"{round(remaining_hours, 2)} hour(s)"
        )


def show_priority_list():
    line()
    print("SUBJECT PRIORITY LIST")
    line()

    if len(subjects) == 0:
        print("No subjects available.")
        return

    sorted_subjects = sort_by_priority()

    for i, subject in enumerate(sorted_subjects, 1):
        print(
            f"{i}. {subject['name']} "
            f"| Priority: {subject['priority']} "
            f"| {subject['priority_level']}"
        )

        print(
            f"   Exam: "
            f"{subject['exam_date'].strftime('%d-%m-%Y')} "
            f"| Days left: {subject['days_left']}"
        )

        print(
            f"   Preparation: "
            f"{subject['preparation']}%"
        )


def search_subject():
    line()
    print("SEARCH SUBJECT")
    line()

    if len(subjects) == 0:
        print("No subjects available.")
        return

    search = input(
        "Enter subject name or keyword: "
    ).strip().lower()

    found = False

    for subject in subjects:
        if search in subject["name"].lower():
            display_subject(subject)
            found = True

    if not found:
        print("No matching subject found.")


def remove_subject():
    line()
    print("REMOVE SUBJECT")
    line()

    subject = find_subject()

    if subject is None:
        return

    confirm = input(
        f"Are you sure you want to remove "
        f"{subject['name']}? (yes/no): "
    ).strip().lower()

    if confirm == "yes":
        subjects.remove(subject)
        print("Subject removed successfully.")

    else:
        print("Operation cancelled.")


def performance_analysis():
    line()
    print("PERFORMANCE ANALYSIS")
    line()

    if len(subjects) == 0:
        print("No subjects available.")
        return

    highest = subjects[0]
    lowest = subjects[0]

    for subject in subjects:
        if calculate_progress(subject) > calculate_progress(highest):
            highest = subject

        if calculate_progress(subject) < calculate_progress(lowest):
            lowest = subject

    total = 0

    for subject in subjects:
        total += calculate_progress(subject)

    average = total / len(subjects)

    print(
        f"Overall preparation: {round(average, 2)}%"
    )

    print(
        f"Strongest subject: {highest['name']} "
        f"({calculate_progress(highest)}%)"
    )

    print(
        f"Subject needing most attention: "
        f"{lowest['name']} "
        f"({calculate_progress(lowest)}%)"
    )

    print("\nRecommendations:")

    for subject in subjects:
        progress = calculate_progress(subject)

        if progress < 40:
            print(
                f"- Spend more time on {subject['name']}."
            )

        elif subject["days_left"] <= 3:
            print(
                f"- {subject['name']} exam is very close."
            )

        elif subject["difficulty"] == "Hard":
            print(
                f"- Give extra revision time to "
                f"{subject['name']}."
            )

        else:
            print(
                f"- Maintain your progress in "
                f"{subject['name']}."
            )


def refresh_days_and_priorities():
    for subject in subjects:
        subject["days_left"] = calculate_days_left(
            subject["exam_date"]
        )

        subject["priority"] = calculate_priority(
            subject
        )

        subject["priority_level"] = get_priority_level(
            subject["priority"]
        )


def main_menu():
    while True:

        refresh_days_and_priorities()

        line()
        print("           SMART STUDY PLANNER")
        line()

        print("1. Add Subject")
        print("2. View All Subjects")
        print("3. Update Study Progress")
        print("4. Generate Smart Study Plan")
        print("5. View Priority List")
        print("6. View Overall Progress")
        print("7. Performance Analysis")
        print("8. Search Subject")
        print("9. Remove Subject")
        print("10. Exit")

        line()

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_subject()
            pause()

        elif choice == "2":
            view_subjects()
            pause()

        elif choice == "3":
            update_progress()
            pause()

        elif choice == "4":
            generate_study_plan()
            pause()

        elif choice == "5":
            show_priority_list()
            pause()

        elif choice == "6":
            show_progress()
            pause()

        elif choice == "7":
            performance_analysis()
            pause()

        elif choice == "8":
            search_subject()
            pause()

        elif choice == "9":
            remove_subject()
            pause()

        elif choice == "10":
            line()
            print("Thank you for using Smart Study Planner!")
            print("Good luck with your studies!")
            line()
            break

        else:
            print("Invalid choice.")
            pause()


main_menu()
