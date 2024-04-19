from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacation.db'
db = SQLAlchemy(app)
app.secret_key = 'your_secret_key'

# Define Vacation model
class Vacation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_number = db.Column(db.String(50))
    selected_weeks = db.Column(db.String(200))
    round_number = db.Column(db.Integer)

# Placeholder for employee information (badge number to name and email mapping)
employee_info = {
    "77763": {"name": "Louay Kanafani", "email": "goshp4christ@gmail.com"},
    "12345": {"name": "Lou Kan", "email": "Louay.kanafani@ttc.ca"},
    "54321": {"name": "John Doe", "email": "Louay.Kanafani@gmail.com"}
}

# Placeholder for entitlement (badge number to entitled vacation weeks mapping)
entitlements = {
    "77763": ["Week 1", "Week 2", "Week 3"],
    "12345": ["Week 1", "Week 2", "Week 3"],
    "54321": ["Week 1", "Week 2", "Week 3", "Prime Week 1", "Prime Week 2"]
}

# Placeholder for tracking which weeks have been taken
taken_weeks = {
    "Week 1": False,
    "Week 2": False,
    "Week 3": False,
    "Prime Week 1": False,
    "Prime Week 2": False
}

# Function to update taken_weeks when a week is selected by an employee
def update_taken_weeks(selected_weeks):
    for week in selected_weeks:
        taken_weeks[week] = True

# Placeholder for round number (to track the vacation selection rounds)
round_number = 1

# Placeholder for tracking the current employee index
current_employee_index = 0

# Function to get the next person on the seniority list
def get_next_person():
    global current_employee_index
    current_employee_index = (current_employee_index + 1) % len(employee_info)
    return list(employee_info.keys())[current_employee_index]

# Update the function to send email to the next person on the list
def send_email_to_next_person(badge_number):
    next_person_badge_number = get_next_person()
    next_person_info = employee_info[next_person_badge_number]
    next_person_email = next_person_info["email"]
    sender_email = "gosikhena@gmail.com"
    password = "xtje mvzm czed jnzd"  # Use an app-specific password if 2FA is enabled
    
    message = MIMEText("It's your turn to pick your vacation. Please enter the system and make your selection.")
    message["Subject"] = "Vacation Selection Reminder"
    message["From"] = sender_email
    message["To"] = next_person_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, next_person_email, message.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    badge_number = request.form['badge_number']
    session['badge_number'] = badge_number
    if badge_number in employee_info:
        return redirect(url_for('show_vacation_selection'))
    else:
        return "Invalid badge number, please try again."

# Update the vacation_selection route to handle prime week selection correctly
@app.route('/process_vacation_selection', methods=['POST'])
def process_vacation_selection():
    badge_number = session.get('badge_number')
    selected_weeks = [key for key in request.form.keys() if key.startswith('week')]  # Corrected key extraction

    if not selected_weeks:
        return "Please select at least one vacation week."


    # Check if selected weeks exceed entitlement
    entitled_weeks = entitlements.get(badge_number)
    if len(selected_weeks) > len(entitled_weeks):
        return "You have selected more weeks than your entitlement. Please try again."


    # Handle prime weeks selection
    prime_weeks_selected = [week for week in selected_weeks if week.startswith("Prime Week")]
    if len(prime_weeks_selected) > 2:
        return "You can only select up to 2 Prime Weeks. Please try again."
        
    # Ensure that all entitled weeks are selected if no prime weeks are selected
    if not prime_weeks_selected and set(selected_weeks) != set(entitled_weeks):
        return "You must select all your entitled vacation weeks. Please try again."

    # Update taken_weeks if a week is selected
    update_taken_weeks(selected_weeks)

    # Update database with selected vacation weeks and round number
    new_vacation = Vacation(badge_number=badge_number, selected_weeks=','.join(selected_weeks), round_number=round_number)
    db.session.add(new_vacation)
    db.session.commit()

    # Send email to the next person on the list
    send_email_to_next_person(badge_number)

    return redirect(url_for('confirm_selection'))

# Define Employee model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    badge_number = db.Column(db.String(20))  # Changed from db.Integer(20) to db.String(20)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
                      
# Route for adding a new employee
@app.route('/add_employee', methods=['POST'])
def add_employee():
    badge_number = request.form['badge_number']
    name = request.form['name']
    email = request.form['email']
    
    new_employee = Employee(badge_number=badge_number, name=name, email=email)
    db.session.add(new_employee)
    db.session.commit()

    return "New employee added successfully."

@app.route('/show_vacation_selection', methods=['GET'])
def show_vacation_selection():
    badge_number = session.get('badge_number')
    if badge_number:
        user_info = employee_info.get(badge_number)
        if user_info:
            return render_template('vacation_selection.html', user_name=user_info['name'], badge_number=badge_number)
    return redirect(url_for('index'))


# Route for confirmation page
@app.route('/confirm_selection', methods=['GET', 'POST'])
def confirm_selection():
    if request.method == 'GET':
        badge_number = session.get('badge_number')
        user_name = employee_info.get(badge_number)["name"]
        selected_weeks = request.form.getlist('selected_weeks')
        return render_template('confirm_selection.html')
    elif request.method == 'POST':
        badge_number = session.get('badge_number')
        selected_weeks = Vacation.query.filter_by(badge_number=badge_number).first().selected_weeks.split(',')
        
        if current_employee_index != len(employee_info) - 1:
            send_email_to_next_person(badge_number)

        round_number += 1
        return "Vacation selection confirmed. Email sent to the next person on the list."

@app.route('/employee_information')
def employee_information():
    return render_template('employee_information.html', employee_info=employee_info, entitlements=entitlements, taken_weeks=taken_weeks)

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
    
    # Run the Flask app
    app.run(debug=True)
