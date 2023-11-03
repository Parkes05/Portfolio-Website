import os
from flask import Flask, render_template, url_for, redirect, abort, jsonify, send_from_directory, request
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, InputForm


def current_date():
    dt = datetime.now()
    date = dt.strftime('%B, %Y')
    return date

date = current_date()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'sqlite:///projects.db')
db = SQLAlchemy(app)

Bootstrap5(app)


login_manager = LoginManager(app)
@login_manager.user_loader
def load_user(id):
    return db.get_or_404(User, id)


class Python(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    github_url = db.Column(db.String(250), nullable=False)

class ML(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    github_url = db.Column(db.String(250), nullable=False)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    data_python = db.session.execute(db.select(Python)).scalars().all()
    data_ml = db.session.execute(db.select(ML)).scalars().all()
    return render_template('index.html', date=date, page='home', py=data_python, ml=data_ml)


@app.route('/python')
def python():
    data_python = db.session.execute(db.select(Python)).scalars().all()
    return render_template('projects.html', date=date, page='python', projects=data_python)


@app.route('/machine-learning')
def machine_learning():
    data_ml = db.session.execute(db.select(ML)).scalars().all()
    return render_template('projects.html', date=date, page='ml', projects=data_ml)


@app.route('/secrets', methods=['GET', 'POST'])
def secrets():
    login = LoginForm()
    if login.validate_on_submit():
        email = login.email.data
        passw = login.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user.id == 1:
            if check_password_hash(user.password, passw):
                login_user(user)
            return redirect(url_for('input'))
        else:
            return abort(403)
    return render_template('forms.html', login=login, date=date, status=True)


@app.route('/input', methods=['GET', 'POST'])
@login_required
def input():
    input = InputForm()
    if input.validate_on_submit():
        if input.table.data.lower() == 'python' or input.table.data.lower() == 'py':
            data = Python(
                title=input.title.data,
                description=input.description.data,
                img_url=input.img_url.data,
                github_url=input.github_url.data,
            )
        elif input.table.data.lower() == 'ml':
            data = ML(
                title=input.title.data,
                description=input.description.data,
                img_url=input.img_url.data,
                github_url=input.github_url.data,
            )
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('forms.html', input=input, date=date, status=False)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = LoginForm()
    if login.validate_on_submit():
        password = generate_password_hash(login.password.data)
        new_user = User(
            email=login.email.data,
            password=password
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('secrets'))
    return render_template('forms.html', login=login, date=date, status=True)


@app.route('/download')
def download():
    return send_from_directory('static', path='file/Benjamin_Muoka_Resume.pdf', as_attachment=True)


@app.route('/update')
def update():
    input = InputForm()
    if input.validate_on_submit():
        if input.table.data.lower() == 'python' or input.table.data.lower() == 'py':
            data = db.session.execute(db.select(Python).where(Python.title == input.title.data)).scalar()
            data.description = input.description.data
            data.img_url = input.img_url.data
            data.github_url = input.github_url.data
            db.session.commit()
        elif input.table.data.lower() == 'ml':
            data = db.session.execute(db.select(Python).where(Python.title == input.title.data)).scalar()
            data.description = input.description.data
            data.img_url = input.img_url.data
            data.github_url = input.github_url.data
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('forms.html', input=input, date=date, status=False)    


#API Calls
@app.route('/all')
def all():
    table = request.args.get('table', type=str)
    if table == 'py':
        data =  db.session.execute(db.select(Python)).scalars().all()
    elif table == 'ml':
        data =  db.session.execute(db.select(ML)).scalars().all()

    data_list = []
    for i in data:
        data_dictionary = {item.name:getattr(i, item.name) for item in i.__table__.c if item.name != 'img_url'}
        data_list.append(data_dictionary)
    return jsonify(projects=data_list)


if __name__ == '__main__':
    app.run(debug=True)


