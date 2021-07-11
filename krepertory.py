

from flask.helpers import flash
from flask.helpers import url_for
from flask.templating import render_template
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect
from os import environ
from rubrics import iDefault
from rubrics import rubricsdb
import config

# FLASK_ENV="production"
# uwsgi --ini wsgi.ini

rublist = [rub for rub in rubricsdb.keys()]

app = Flask(__name__)
# key for session
# app.secret_key = ''.join(random.SystemRandom().choice(
#     string.ascii_uppercase + string.digits + string.ascii_lowercase) 
#     for _ in range(32)
#     )

environment = environ.get("FLASK_ENV", default="development")
if environment == "production":
   cfg = config.ProductionConfig()
else:
    cfg = config.DevelopmentConfig()
 
app.config.from_object(cfg)

@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/krep/api/v1/test')
def test():
    return "this is just a test string"

@app.route('/krep/api/v1/rubrics/all')
def rubricsAll():
    return jsonify(rublist)

@app.route('/krep/api/v1/rubrics/meds')
def rubricsMeds():
    if 'name' not in request.args:
        return pageNotFound(404)
    rub = request.args['name']
    return jsonify(rubricsdb[rub])


@app.route('/krep/')
def home():
    if "selected" not in session.keys():
        session['selected'] = []
        session['meds'] = []
        print('selected added')
    return render_template('home.html',
        selected = session['selected'],
        meds = session['meds'],
        available = rublist, 
        skey = app.secret_key
        )

@app.route('/krep/api/v1/addRubric/<string:rub>')
def addRubric(rub):
    if "selected" not in session.keys():
        flash('Server resetted, kindly re-select', 'error')
        return redirect(url_for('home'))
    if rub not in session['selected']: 
        session['selected'].append(rub)
        session.modified = True
        flash("added: "+ rub, category='info')
    else:
        flash("already selected: "+ rub, category='warning')
    apposition()
    return redirect(url_for('home'))

@app.route('/krep/api/v1/removeRubric/<string:rub>')
def removeRubric(rub):
    if "selected" not in session.keys():
        flash('Server resetted, kindly re-select', 'error')
        return redirect(url_for('home'))
    session['selected'].remove(rub)
    session.modified = True
    flash("removed: "+ rub, category='info')
    apposition()
    return redirect(url_for('home'))

def apposition():
    if "selected" not in session.keys() or len(session["selected"]) < 1:
        session["meds"].clear()
        return
    resultset = {val for val in iDefault.keys()}
    for rub in session["selected"]:
        resultset = resultset.intersection(
            {val for val in rubricsdb[rub].keys()}
        )
    session['meds'] = [v for v in resultset]
    session.modified = True

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001
    )
    # done