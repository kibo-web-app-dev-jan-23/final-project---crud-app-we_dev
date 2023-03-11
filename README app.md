
<!-- This Flask app is a simple quiz application that allows users to register, login, take a quiz, and view their quiz scores. The app uses SQLite as its database and SQLAlchemy as its ORM. -->

#Schema Tables

The app has two tables in its database schema:

#Gamer

-id (integer): primary key for each user
-username (string): unique username for each user
-email (string): unique email for each user
-password (string): password for each user
-date_created (DateTime): timestamp for user creation

#QuizScore

-id (integer): primary key for each quiz score
-score (integer): score achieved by user on a quiz
-user_id (integer): foreign key to Gamer table for the corresponding user

#Setting Up the App

To set up the app locally, follow these steps:

-Clone the repository.
-Install the required packages using pip install -r requirements.txt.
-In the terminal, navigate to the project directory.
-Create a virtual environment using python -m venv env.
-Activate the virtual environment using source env/bin/activate (on Mac/Linux) or .\env\Scripts\activate (on Windows).
-Set the FLASK_APP environment variable using export FLASK_APP=app.py (on Mac/Linux) or set FLASK_APP=app.py (on Windows).
-Set the FLASK_ENV environment variable to "development" using export FLASK_ENV=development (on Mac/Linux) or set FLASK_ENV=development (on  Windows).
-Create the SQLite database by running flask db init, flask db migrate, and flask db upgrade.
-Run the app using flask run.
-The app should now be running at http://localhost:5000.

Note: You will need to create a config.py file in the root directory of the project and add a SECRET_KEY variable for the app.secret_key. You can generate a secret key by running python -c "import secrets; print(secrets.token_hex(16))" in the terminal.

#Using the App

Once the app is set up and running, you can access it at http://localhost:5000.

1)Register
To register, click on the "Register" link on the homepage and fill out the registration form. If the registration is successful, you will be redirected to the login page.

2)Login
To login, click on the "Login" link on the homepage and enter your email and password. If the login is successful, you will be redirected to the quiz page.

3)Take Quiz
To take the quiz, select your answer for each question and click the "Submit" button. You will then be redirected to the results page, where you can view your score and the correct answers.

4)View Quiz Scores
To view your quiz scores, click on the "View Scores" link on the homepage. You will be redirected to a page that displays your quiz score

5)Logout
To logout, click on the "Logout" button on the quiz or scores pages. You will be redirected to the homepage.
