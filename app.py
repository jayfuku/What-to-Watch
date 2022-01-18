from re import A
from flask import Flask,render_template, request, flash

from watch import *


app = Flask(__name__)

def find_anime(username, time_pref):
    ptw = generate_ptw(username)
    ptw = sort_ptw(ptw)
    return get_suggestion(ptw,time_pref)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods = ["POST"])
def submit():
    if request.method == 'POST':
        user = request.form['username']
        time = request.form['Time Preference']
        year = request.form['year']

        if user == '':
            return render_template('index.html', message = "1")
        elif verify_account(user):
            return render_template('index.html', message = "2")
        elif not verify_year(year):
            return render_template('index.html', message = "4")
        else:
            result = find_anime(user,time+" "+str(year))
            if result == {}:
                return render_template('index.html', message = "3")
        return render_template('success.html', link=generate_link(result),image=generate_image(result), name = result['node']['title'])

if __name__ == "__main__":
    app.debug = True
    app.run()