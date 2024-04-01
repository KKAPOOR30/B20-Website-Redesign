from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, flash, redirect, request, session
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
    

with app.app_context():
    db.create_all()

@app.route('/')
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

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            flash('already logged in!!')
            return redirect(url_for('student', name = session['name'][0]))
        else:
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
            if person.type == 'Student':
                return redirect(url_for('student', name = name))
            return redirect(url_for('instructor', name = name))
        
@app.route('/<name>/CSCB20', methods = ['GET', 'POST'])
def student(name):
    if name == session['name'][0]:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))

@app.route('/<name>/CSCB20', methods = ['GET', 'POST'])
def instructor(name):
    return render_template('index.html')







@app.route('/logout')
def logout():
    session.pop('name', default = None)
    session.pop('name', default = None)
    return redirect(url_for('register'))



def add_users(reg_details):
    person = Person(username = reg_details[0],name = reg_details[1] , email = reg_details[2],type = reg_details[3], password = reg_details[4])
    db.session.add(person)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)
