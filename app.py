from flask import Flask, redirect, request, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.sql import func

from PerfectcomAPI import OcrReader

app = Flask(__name__, template_folder='templates', static_folder='static')
app.debug = True
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = '911a6862-f62d-11eb-848b-0242ac1c0002'
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate()
test = OcrReader()


def create_app():
    db.init_app(app)
    migrate.init_app(app, db)
    return app


@migrate.configure
def configure_alembic(config):
    # modify config object
    return config


class Profile(db.Model):
    __tablename__ = 'Profile'
    id = db.Column(db.Integer, primary_key=True)
    Identification_Number = db.Column(db.Integer, unique=False, nullable=False)
    PrefixTH = db.Column(db.String(20), unique=False, nullable=False)
    NameTH = db.Column(db.String(30), unique=False, nullable=False)
    LastNameTH = db.Column(db.String(30), unique=False, nullable=False)
    PrefixEN = db.Column(db.String(20), unique=False, nullable=False)
    NameEN = db.Column(db.String(30), unique=False, nullable=False)
    LastNameEN = db.Column(db.String(30), unique=False, nullable=False)
    BirthdayTH = db.Column(db.String(20), unique=False, nullable=False)
    BirthdayEN = db.Column(db.String(20), unique=False, nullable=False)
    Religion = db.Column(db.String(20), unique=False, nullable=False)
    Address = db.Column(db.String(100), unique=False, nullable=False)
    Issuedate_TH = db.Column(db.String(20), unique=False, nullable=False)
    Expirydate_TH = db.Column(db.String(20), unique=False, nullable=False)
    Issuedate_EN = db.Column(db.String(20), unique=False, nullable=False)
    Expirydate_EN = db.Column(db.String(20), unique=False, nullable=False)

    def __repr__(self):
        return f'<Profile {self.NameTH}>'


@app.route('/')
def index():
    profiles = Profile.query.all()
    return render_template('index.html', profiles=profiles)


@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')


# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
    url = request.form["url"]
    text = test.extract_data(url)
    card_info = []
    for i in text:
        card_info.append(i)
    if card_info[0] != '' and card_info[1] != '' and card_info[2] != '' and card_info[3] != '' and card_info[
        4] != '' and card_info[5] != '' and card_info[6] != '' and card_info[7] != '' and card_info[8] != '' and \
            card_info[9] != '' and card_info[10] != '' and card_info[11] != '' and card_info[12] != '' and card_info[
        13] != '' and card_info[14] is not None:
        p = Profile(Identification_Number=card_info[0], PrefixTH=card_info[1], NameTH=card_info[2],
                    LastNameTH=card_info[3], PrefixEN=card_info[4], NameEN=card_info[5], LastNameEN=card_info[6],
                    BirthdayTH=card_info[7], BirthdayEN=card_info[8], Religion=card_info[9], Address=card_info[10],
                    Issuedate_TH=card_info[11], Expirydate_TH=card_info[13], Issuedate_EN=card_info[12],
                    Expirydate_EN=card_info[14])
        db.session.add(p)
        db.session.commit()
        return redirect('/')
    else:
        return redirect('/')


@app.route('/delete/<int:id>')
def erase(id):
    # deletes the data on the basis of unique id and
    # directs to home page
    data = Profile.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run()
