from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextField
from wtforms.validators import DataRequired
import os


basedir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY-TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ramanujan1729!'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[FLASK APP]'
app.config['MAIL_SENDER'] = 'ADMIN <ntrichy99@gmail.com>'
app.config['ADMIN'] = os.environ.get('ADMIN')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
# db.init_app(app)


def send_mail(to, subject, template, **kwargs):
    msg = Message(app.config['MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(10), unique=True, nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    query = db.Column(db.String(100))


class QueryForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone_number = IntegerField("phone number", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    query = StringField("query", validators=[DataRequired()])
    submit = SubmitField("submit")


@ app.route("/", methods=['GET', 'POST'])
def index():
    form = QueryForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data, email=form.email.data,
                        phone_number=form.phone_number.data, subject=form.subject.data, query=form.query.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Your Query Has Been Submitted Sucessfully')
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'], 'NEW QUERY',
                      'mail/new_query', user=new_user)
        return redirect(url_for('index'))
    return render_template('base.html', form=form)


@ app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@ app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
