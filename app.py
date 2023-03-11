from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import Column, String, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from quizes import display_questions

app = Flask(__name__, static_folder= "static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

# User Model
class Gamer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username
    
    # Relationship to QuizScore Model
    quiz_scores = db.relationship('QuizScore', backref='gamer', lazy=True)


# QuizScore Model
class QuizScore(db.Model):
    __tablename__ = 'quiz_scores'
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)

    # Foreign Key to User Model
    user_id = db.Column(db.Integer, db.ForeignKey('gamer.id'), nullable=False)

# Create all the tables
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('questions'))
    return render_template("home.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            error = "Passwords do not match. Please try again."
            return render_template('register.html', error=error)

        existing_user = Gamer.query.filter_by(username=username).first()
        if existing_user:
            error = "Username already exists. Please choose another one."
            return render_template('register.html', error=error)

        user = Gamer(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # query the database for the user
        user = Gamer.query.filter_by(email=email, password=password).first()
        if user is None:
            error = 'Invalid email or password. Please try again.'
        else:
            # set the user as logged in
            session['user_id'] = user.id
            session['logged_in'] = True
            # redirect to the questions page
            return redirect(url_for('questions'))

    # render the login page
    return render_template('login.html', error=error)

@app.route("/questions")
def questions():
    # Check if user is logged in
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    # Render the questions page
    return render_template("questions.html", display_questions=display_questions)


@app.route("/results", methods=["POST"])
def results():
    score = 0
    for question in display_questions:
        answered = request.form.get(question["question"])
        if answered == question["answer"]:
            score += 1

    # Create a new QuizScore object and add it to the database
    quiz_score = QuizScore(score=score, user_id=session['user_id'])
    db.session.add(quiz_score)
    db.session.commit()

    return render_template("results.html", score=score, display_questions=display_questions)

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    session.pop('logged_in', False)
    session.clear()
    return redirect(url_for('index'))


