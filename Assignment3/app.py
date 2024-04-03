from datetime import datetime, timedelta
from flask import Flask,jsonify, render_template, url_for, flash, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import text # textual queries

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 15)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)




class Person(db.Model):
    __tablename__ = 'Person'
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(100), primary_key=True, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    type = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Person('{self.username}','{self.email}')"

class RemarkRequest(db.Model):
    __tablename__ = 'Remarks'
    student = db.Column(db.String(200), primary_key=True)
    test_type = db.Column(db.String(100), primary_key=True)
    reason = db.Column(db.String(200))

    def __init__(self, student, test_type, reason):
        self.student = student
        self.test_type = test_type
        self.reason = reason

class Grades(db.Model):
    __tablename__ = 'Grades'
    email = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    A1 = db.Column(db.Numeric, nullable=True)
    A2 = db.Column(db.Numeric, nullable=True)
    A3 = db.Column(db.Numeric, nullable=True)
    tutorials = db.Column(db.Numeric, nullable=True)
    midterm = db.Column(db.Numeric, nullable=True)
    exam = db.Column(db.Numeric, nullable=True)
    final = db.Column(db.Numeric, nullable=True)


class Feedback(db.Model):
    __tablename__ = 'Feedback'
    email = db.Column(db.String(100), unique=False, nullable=False, primary_key=True)
    feed_1 = db.Column(db.String, nullable=False)
    feed_2 = db.Column(db.String, nullable=False)
    feed_3 =  db.Column(db.String, nullable=False)
    feed_4 = db.Column(db.String, nullable=False)
    feed_5 =  db.Column(db.String, nullable=False)


with app.app_context():
    db.create_all()


def home():
    if 'name' in session and session['name'][1] == 'Student':
        flash('already logged in!!')
        return redirect(url_for('student', name = session['name'][0]))
    if 'name' in session and session['name'][1] == 'Instructor':
        flash('already logged in!!')
        return redirect(url_for('instructor', name = session['name'][0]))
    else:
        return render_template('login.html')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        name = request.form['Name']
        username = request.form['Username']
        email = request.form['Email']
        type = request.form['Type']
        password = request.form['Password']
        if not username or not name or not email or not type or not password:
            flash('Please fill in all fields.')
            return redirect(url_for('register'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        reg_details =(
            username,
            name,
            email,
            type,
            hashed_password
        )
        existing_user = Person.query.filter_by(email=email).first()

        if existing_user:
            flash('Email already in use!')
            return redirect(url_for('register'))
        existing_user = Person.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already in use!')
            return redirect(url_for('register'))

        add_users(reg_details)
        flash('Registration Successful! Please login now:')
        return redirect(url_for('login'))
    
@app.route('/')   
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('student', name = session['name'][0]))
        return render_template('login.html')
    else:
        username = request.form['Username']
        password = request.form['Password']
        person = Person.query.filter_by(username = username).first()
        if not person or not bcrypt.check_password_hash(person.password, password):
            flash('Please check your login details and try again', 'error')
            return render_template('login.html')
        else:
            name = person.name
            session['name'] = [name, person.type]
            session.permanent = True
            if person.type == 'student':
                return redirect(url_for('student', name = name))
            return redirect(url_for('student', name = name))
        
@app.route('/<name>/CSCB20', methods = ['GET', 'POST'])
def student(name):
    if 'name' in session and session['name'][1] == "student" :
        return render_template('index.html')
    if 'name' in session and session['name'][1] == "instructor" :
        return render_template('index.html')
    return render_template('login.html')

    

@app.route('/<name>/calendar.html')
def calendar(name):
    if 'name' in session:
        return render_template('calendar.html')
    else:
        return render_template('login.html')
@app.route('/<name>/index.html')
def index(name):
    if 'name' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')
@app.route('/<name>/news.html')
def news(name):
    if 'name' in session:
        return render_template('news.html')
    else:
        return render_template('login.html')

@app.route('/<name>/lectures.html')
def lectures(name):
    if 'name' in session:
        return render_template('lectures.html')
    else:
        return render_template('login.html')

@app.route('/<name>/labs.html')
def labs(name):
    if 'name' in session:
        return render_template('labs.html')
    else:
        return render_template('login.html')
@app.route('/<name>/assignments.html')
def assignments(name):
    if 'name' in session:
        return render_template('assignments.html')
    else:
        return render_template('login.html')
@app.route('/<name>/tests.html')
def tests(name):
    if 'name' in session:
        return render_template('tests.html')
    else:
        return render_template('login.html')
    
@app.route('/<name>/resources.html')
def resources(name):
    if 'name' in session:
        return render_template('resources.html')
    else:
        return render_template('login.html')
@app.route('/<name>/team.html')
def team(name):
    if 'name' in session:
        return render_template('team.html')
    else:
        return render_template('login.html')
    
@app.route('/<name>/grades.html')
def grades(name):
    if 'name' in session and session['name'][1] == 'student':
        return render_template('grades.html')
    elif 'name' in session and session['name'][1] == 'instructor':
        return render_template('index.html')
    return render_template('login.html')
@app.route('/<name>/feedback.html')
def feedback(name):
    if 'name' in session:
        return render_template('feedback.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('name', default = None)
    session.pop('name', default = None)
    return redirect(url_for('register'))



def add_users(reg_details):
    person = Person(username = reg_details[0],name = reg_details[1] , email = reg_details[2],type = reg_details[3], password = reg_details[4])
    db.session.add(person)
    db.session.commit()


@app.route('/submit-remark-request', methods=['POST'])
def submit_remark_request():

    test_type = request.form['test_type']
    reason = request.form['reason']
    name = session['name'][0]

    existing_record = RemarkRequest.query.filter_by(student=name, test_type=test_type).first()
    if existing_record:
        return jsonify({'message': 'Remark already submitted'})

    # Create a new RemarkRequest object and add it to the database
    remark_request = RemarkRequest(name,test_type=test_type, reason=reason)

    db.session.add(remark_request)
    db.session.commit()

    return jsonify({'message': 'Remark request submitted successfully'})












if __name__ == '__main__':
    app.run(debug=True)
