from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate attendance score
def calculate_attendance_score(absences):
    score = 100 - (10 * absences)
    return "FAILED" if absences >= 4 else score

# Function to calculate class standing
def calculate_class_standing(quizzes, requirements, recitations):
    return (0.40 * quizzes) + (0.30 * requirements) + (0.30 * recitations)

# Function to calculate overall prelim grade
def calculate_overall_prelim_grade(prelim, attendance, class_standing):
    return (0.60 * prelim) + (0.10 * attendance) + (0.30 * class_standing)

# Function to determine pass/fail
def determine_pass_fail(overall_grade):
    return "Pass" if overall_grade >= 75 else "Fail"

# Function to calculate required grades
def calculate_required_grades(prelim, target_grade):
    return (target_grade - (0.2 * prelim)) / 0.8

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get form data
            absences = int(request.form['absences'])
            prelim = float(request.form['prelim'])
            quizzes = float(request.form['quizzes'])
            requirements = float(request.form['requirements'])
            recitations = float(request.form['recitations'])

            # Calculate attendance
            attendance_result = calculate_attendance_score(absences)
            if attendance_result == "FAILED":
                return render_template('index.html', failed=True)

            # Calculate class standing and overall prelim grade
            class_standing = calculate_class_standing(quizzes, requirements, recitations)
            overall_prelim = calculate_overall_prelim_grade(prelim, attendance_result, class_standing)
            result = determine_pass_fail(overall_prelim)

            # Calculate required midterm and final grades
            required_grade_75 = calculate_required_grades(prelim, 75)
            required_grade_90 = calculate_required_grades(overall_prelim, 90)

            # Format all float values to 2 decimal places
            attendance_result = f"{attendance_result:.2f}"
            class_standing = f"{class_standing:.2f}"
            overall_prelim = f"{overall_prelim:.2f}"
            required_grade_75 = f"{required_grade_75:.2f}"
            required_grade_90 = f"{required_grade_90:.2f}"

            return render_template('index.html', 
                                   attendance_result=attendance_result, 
                                   class_standing=class_standing, 
                                   overall_prelim=overall_prelim, 
                                   result=result,
                                   required_grade_75=required_grade_75, 
                                   required_grade_90=required_grade_90)
        except ValueError:
            return render_template('index.html', error=True)
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
