from gol_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=True)
    about = db.Column(db.Text, nullable=True)
    scores = db.relationship('Scores', backref='user')

    @staticmethod
    def user_in_database(name):
        return User.query.filter_by(username=name).first()

    def save_in_db(self):
        db.session.add(self)
        db.session.commit()


class Scores(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.String, nullable=False)
