from flask import Flask, render_template,session,redirect,url_for,flash
app = Flask(__name__)

app.config['SECRET_KEY'] = 'ramanujan1729!'
@app.route("/",methods=['GET','POST'])
def index():
    flash('Thanks for submitting your query')
    return render_template('home.html')