
import random
import string
from flask.helpers import flash
from flask.helpers import url_for
from flask.templating import render_template
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect

from rubrics import iDefault
from rubrics import rubricsdb


rublist = [rub for rub in rubricsdb.keys()]

app = Flask(__name__)
# key for session
# app.secret_key = "Ph38fTX3Krztt9NFy9zUoe71UivbYvI9"     # need to CHANGE it to random generation
app.secret_key = ''.join(random.SystemRandom().choice(
    string.ascii_uppercase + string.digits + string.ascii_lowercase) 
    for _ in range(32)
    )

@app.errorhandler(404)
def pageNotFound(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.route('/api/v1/test')
def test():
    return "this is just a test string"

@app.route('/api/v1/rubrics/all')
def rubricsAll():
    return jsonify(rublist)

@app.route('/api/v1/rubrics/meds')
def rubricsMeds():
    if 'name' not in request.args:
        return pageNotFound(404)
    rub = request.args['name']
    return jsonify(rubricsdb[rub])

@app.route('/')
def home():
    if "selected" not in session.keys():
        session['selected'] = []
        print('selected added')
    return render_template('home.html',
        selected = session['selected'],
        available = rublist, 
        skey=app.secret_key
        )

@app.route('/api/v1/addRubric/<string:rub>')
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
    return redirect(url_for('home'))

@app.route('/api/v1/removeRubric/<string:rub>')
def removeRubric(rub):
    if "selected" not in session.keys():
        flash('Server resetted, kindly re-select', 'error')
        return redirect(url_for('home'))
    session['selected'].remove(rub)
    session.modified = True
    flash("removed: "+ rub, category='info')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=True
    )
    # done