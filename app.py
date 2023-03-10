from flask import Flask, render_template, request, redirect, url_for, session
from sqlalchemy import Column, String, DateTime
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from quizes import display_questions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = 'mysecretkey'
db = SQLAlchemy(app)

class Gamer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    date_created = Column(DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<User %r>' % self.username

with app.app_context():
    db.create_all()


@app.route("/")
def index():
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
            # redirect to the home page
            return redirect(url_for('index'))
    # render the login page
    return render_template('login.html', error=error)

@app.route("/results", methods=["POST"])
def results():
    score = 0
    for question in display_questions:
        answered = request.form.get(question["question"])
        if answered == question["answer"]:
            score += 1
    return render_template("results.html", score=score, display_questions=display_questions)
