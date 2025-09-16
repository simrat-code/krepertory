
from flask.helpers import flash
from flask.helpers import url_for
from flask.templating import render_template
from flask import Flask
from flask import jsonify
from flask import request
from flask import session
from flask import redirect
from flask import current_app
from os import environ
from .kreprubrics import iDefault
from .kreprubrics import rubricsdb

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

rublist = [rub for rub in rubricsdb.keys()]

bp = Blueprint('krepapp', __name__, url_prefix='/krep')


@bp.errorhandler(404)
def pageNotFound(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@bp.route('/api/v1/test')
def test():
    return "this is just a test string"

@bp.route('/api/v1/rubrics/all')
def rubricsAll():
    return jsonify(rublist)

@bp.route('/api/v1/rubrics/meds')
def rubricsMeds():
    if 'name' not in request.args:
        return pageNotFound(404)
    rub = request.args['name']
    return jsonify(rubricsdb[rub])


@bp.route('/home', methods=['GET'])
def home():
    if "selected" not in session.keys():
        session['selected'] = []
        session['meds'] = []
        print('[=] list "selected" added to session')

    return render_template('home.html',
        selected = session['selected'],
        meds = session['meds'],
        available = rublist, 
        skey = current_app.secret_key
        )


@bp.route("/reset")
def reset():
    session["selected"].clear()
    session["meds"].clear()
    flash('All selections cleared', 'warning')
    return redirect(url_for('krepapp.home'))


@bp.route('/api/v1/add/<string:rub>')
def addRubric(rub):
    if "selected" not in session.keys():
        flash('Server resetted, kindly re-select', 'error')
        return redirect(url_for('krepapp.home'))
    if rub not in session['selected']: 
        session['selected'].append(rub)
        session.modified = True
        flash("added: "+ rub, category='info')
    else:
        flash("already selected: "+ rub, category='warning')
    apposition()
    return redirect(url_for('krepapp.home'))


@bp.route('/api/v1/remove/<string:rub>')
def removeRubric(rub):
    if "selected" not in session.keys():
        flash('Server resetted, kindly re-select', 'error')
        return redirect(url_for('krepapp.home'))
    session['selected'].remove(rub)
    session.modified = True
    flash("removed: "+ rub, category='info')
    apposition()
    return redirect(url_for('krepapp.home'))


def apposition():
    if "selected" not in session.keys() or len(session["selected"]) == 0:
        session["meds"].clear()
        return
    resultset = {val for val in iDefault.keys()}
    for rub in session["selected"]:
        resultset = resultset.intersection(
            {val for val in rubricsdb[rub].keys()}
        )
    session['meds'] = [v for v in resultset]
    session.modified = True

# if __name__ == "__main__":
#     app.run(
#         host="0.0.0.0",
#         port=5001
#     )
    # done
