 ### README File for Employee Leave Management System

#### Introduction:
This documentation provides an overview of the Employee Leave Management System codes and functionalities. The system facilitates employee vacation selection, tracks entitlements, and manages vacation information efficiently.

#### System Components:

1. **Index Page (`index.html`):**
    - Displays the initial login form for employees to enter their badge number.
    - On successful login, redirects to the vacation selection page.

2. **Vacation Selection Page (`vacation_selection.html`):**
    - Greets the user by name and presents options to select vacation weeks.
 - Uses checkboxes for each available week.
    - Allows selection of prime weeks with restrictions.
    - Provides a confirmation dialog before final selection.
    - Invokes JavaScript functions for form submission and confirmation.

3. ** Page (`confirm_selection.html`):**
    - Confirms the successful vacation week selection.
    - Updates vacation information in the database.
    - Triggers an email reminder to the next employee in line.

4. **Employee Information Page (`employee_information.html`):**
    - Displays a tabular view of employee vacation information.
    - Shows badge numbers, names, entitled weeks, selected weeks, and remaining weeks.

#### JavaScript Functionality:
- Handles the confirmation dialog and form submission.
- Ensures the selection of at least one vacation week.
- Updates the employee table dynamically upon form submission.
- Handles AJAX requests for form submission and response handling.

#### Email Sending:
- Automatically reminds the next employee to their vacation week.
- Initiates email sending using SMTP and secured connection methods.

#### Database Integration:
- Utilizes SQLite for database functionality.
- Defines models for `Vac` and `Employee` to store vacation selections and employee details.

#### Flask Routes:
- `/login`: Validates the badge number and redirects to the vacation selection page.
- `/process_vacation_selection`: Processes vacation week selection, updates database, and triggers the email reminder.
- `/confirm_selection`: Confirms the selection, updates the round number, and sends an email to the next person.
- `/add_employee`: Adds a new employee to the database and acknowledges success.

#### Python Libraries Used:
- Flask
- SQLAlchemy
- smtplib
- email.mime
- request
- redirect

#### Running the Application:
- Ensure Flask and related dependencies are installed.
- Run the script to launch the Employee Leave Management System.
- Access the system through appropriate routes to manage vacation selections effectively.

This README gives a comprehensive understanding of the system's structure, functionalities, and how to run and utilize the Employee Leave Management System effectively.

For any further questions or assistance, please refer to the provided documentation or contact the system administrator directly.

### End of README File.  
