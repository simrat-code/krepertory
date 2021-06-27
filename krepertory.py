
from rubrics import iDefault
from rubrics import rubricsdb

from flask import Flask
from flask import jsonify
from flask import request


rublist = [rub for rub in rubricsdb.keys()]

app = Flask(__name__)

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


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=50001,
        debug=True
    )
    # done