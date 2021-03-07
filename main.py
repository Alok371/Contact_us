from flask import Flask, render_template,session,redirect,url_for,flash,request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail,Message
import os


basedir= os.path.abspath(os.path.dirname(__file__))



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'
app.config['SQLALCHEMY-TRACK_MODIFICATIONS']= False
app.config['SECRET_KEY'] = 'ramanujan1729!'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USERNAME']= os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']= os.environ.get('MAIL_PASSWORD')
app.config['MAIL_SUBJECT_PREFIX'] = '[FLASK APP]'
app.config['MAIL_SERVER'] = 'ADMIN <ntrichy99@gmail.com>'
app.config['ADMIN']= os.environ.get('ADMIN')
db= SQLAlchemy(app)
migrate= Migrate(app,db)
mail=Mail(app)
#db.init_app(app)

def send_mail(to,subject,template,**kwargs):
     msg = Message(app.config['MAIL_SUBJECT_PREFIX']+ subject,sender=app.config['MAIL_SENDER'],recipients=[to])
     msg.body = render_template(template + '.txt', **kwargs)
     msg.html = render_template(template + '.html',**kwargs)
     mail.send(msg)

class users(db.Model):
    id=db.Column(db.Integer,primary_key= True)
    firstname= db.Column(db.String(20), nullable=False)
    lastname= db.Column(db.String(20), nullable= False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phonenumber= db.Column(db.String(20), unique=True, nullable= False)
    query = db.Column(db.String(100))



@app.route("/",methods=['GET','POST'])
def index():
    if request.method == "POST":
        flash('Thanks for submitting your query')
        return redirect(url_for('index')) 
        if app.config['ADMIN']:
            send_mail(app.config['ADMIN'],'New User', 'mail/new_user')
    return render_template('base.html', success=True)

  
@app.errorhandler(404)
def page_not_found(e): 
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
