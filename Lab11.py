import os
import matplotlib.pyplot as plt

# Data structures to store information
assignments = {}  # Maps assignment_id to (name, points)
students = {}  # Maps student_id to name
submissions = []  # List of tuples (student_id, assignment_id, score_percentage)

# Load assignments data from 'assignments.txt'
def load_assignments(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            assignment_name = lines[i].strip()
            assignment_id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[assignment_id] = (assignment_name, points)

# Load students data from 'students.txt'
def load_students(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Try to split the ID and name, assuming ID is the first 3 digits
            student_id_str = line[:3]  # Extract the first 3 characters as the ID
            student_name = line[3:].strip()  # The rest is the student's name

            try:
                student_id = int(student_id_str)  # Convert the ID to an integer
                students[student_id] = student_name  # Store the student info in the dictionary
            except ValueError:
                print(f"Skipping invalid entry: {line.strip()}")
                continue  # Skip any invalid lines


# Load submissions data from a directory
def load_submissions(submission_dir):
    for filename in os.listdir(submission_dir):
        file_path = os.path.join(submission_dir, filename)
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line by the pipe ('|') character
                parts = line.strip().split('|')

                if len(parts) == 3:
                    try:
                        # Convert each part to an integer (student_id, assignment_id, score)
                        student_id = int(parts[0])
                        assignment_id = int(parts[1])
                        score = int(parts[2])

                        # Add the submission data to the submissions list
                        submissions.append((student_id, assignment_id, score))
                    except ValueError:
                        print(f"Skipping invalid submission: {line.strip()}")
                        continue  # Skip lines with invalid data
                else:
                    print(f"Skipping malformed submission line: {line.strip()}")
                    continue  # Skip lines that don't have exactly 3 values


# Function to calculate the total grade for a student
def calculate_student_grade(student_id):
    total_score = 0
    total_points = 0
    for student_sub, assignment_sub, score in submissions:
        if student_sub == student_id:
            assignment_name, assignment_points = assignments[assignment_sub]
            total_score += (score / 100) * assignment_points
            total_points += assignment_points
    return round((total_score / total_points) * 100)

# Function to generate assignment statistics (min, avg, max scores)
def assignment_statistics(assignment_id):
    scores = [score for student_id, ass_id, score in submissions if ass_id == assignment_id]
    min_score = min(scores)
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)

    # Format the avg_score to 2 decimal places
    formatted_avg_score = f"{avg_score:.0f}"

    return min_score, formatted_avg_score, max_score


# Function to generate histogram of scores for an assignment
def plot_assignment_histogram(assignment_id):
    scores = [score for student_id, ass_id, score in submissions if ass_id == assignment_id]
    plt.hist(scores, bins=[0, 25, 50, 75, 100])
    plt.title(f'Score Distribution for {assignments[assignment_id][0]}')
    plt.xlabel('Score (%)')
    plt.ylabel('Number of Students')
    plt.show()

# Helper functions to find student and assignment IDs based on their names
def find_student_id(student_name):
    for student_id, name in students.items():
        if name.lower() == student_name.lower():
            return student_id
    return None

def find_assignment_id(assignment_name):
    for assignment_id, (name, points) in assignments.items():
        if name.lower() == assignment_name.lower():
            return assignment_id
    return None

# Function to display the menu and handle user input
def display_menu():
    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = int(input("Enter your selection: "))

    if choice == 1:
        student_name = input("What is the student's name: ")
        student_id = find_student_id(student_name)
        if student_id:
            grade = calculate_student_grade(student_id)
            print(f"{grade}%")
        else:
            print("Student not found.")
    elif choice == 2:
        assignment_name = input("What is the assignment name: ")
        assignment_id = find_assignment_id(assignment_name)
        if assignment_id:
            min_score, avg_score, max_score = assignment_statistics(assignment_id)
            print(f"Min: {min_score}%")
            print(f"Avg: {avg_score}%")
            print(f"Max: {max_score}%")
        else:
            print("Assignment not found.")
    elif choice == 3:
        assignment_name = input("What is the assignment name: ")
        assignment_id = find_assignment_id(assignment_name)
        if assignment_id:
            plot_assignment_histogram(assignment_id)
        else:
            print("Assignment not found.")
    else:
        print("Invalid selection")

# Main function to load data and run the menu
def main():
    # Paths to the files (replace these with actual paths)
    assignments_path = '/Users/evanlowther/PycharmProjects/Lab11/assignments.txt'
    students_path = '/Users/evanlowther/PycharmProjects/Lab11/students.txt'
    submissions_dir = '/Users/evanlowther/PycharmProjects/Lab11/submissions'

    # Load all data
    load_assignments(assignments_path)
    load_students(students_path)
    load_submissions(submissions_dir)

    # Run the menu to interact with the program
    display_menu()

if __name__ == "__main__":
    main()
