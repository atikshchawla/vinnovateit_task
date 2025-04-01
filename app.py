from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random
import string

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///url.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)  # Fix: Direct initialization


class Urls(db.Model):
    id_ = db.Column(db.Integer, primary_key=True)
    long = db.Column(db.String(), nullable=False)  # Fix: Ensure URL is not NULL
    short = db.Column(db.String(10), unique=True, nullable=False)  # Fix: Unique short URLs

    def __init__(self, long, short):
        self.long = long
        self.short = short


def shorten_url():
    letters = string.ascii_letters  # Fix: Combined uppercase & lowercase
    while True:
        rand_letters = ''.join(random.choices(letters, k=3))  # Fix: Join directly
        if not Urls.query.filter_by(short=rand_letters).first():
            return rand_letters


@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        url_received = request.form["nm"]
        found_url = Urls.query.filter_by(long=url_received).first()

        if found_url:
            return redirect(url_for("display_short_url", url=found_url.short))
        else:
            short_url = shorten_url()
            new_url = Urls(url_received, short_url)
            db.session.add(new_url)
            db.session.commit()
            return redirect(url_for("display_short_url", url=short_url))
    return render_template('url_page.html')


@app.route('/<short_url>')
def redirection(short_url):
    long_url = Urls.query.filter_by(short=short_url).first()
    if long_url:
        return redirect(long_url.long)
    else:
        return '<h1>URL does not exist</h1>', 404  # Fix: Return HTTP 404 status


@app.route('/display/<url>')
def display_short_url(url):
    return render_template('shorturl.html', short_url_display=url)


@app.route('/all_urls')
def display_all():
    return render_template('all_urls.html', vals=Urls.query.all())


if __name__ == '__main__':
    with app.app_context():  # Fix: Ensure DB tables are created properly
        db.create_all()
    app.run(port=5000, debug=True)
