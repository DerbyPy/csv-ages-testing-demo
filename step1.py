import csv

import arrow
import flask
from flask import request
import flask_webtest
import webtest

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        csv_file = request.files['csv_file']

        age_sum = 0

        csv_lines = csv_file.read().decode('utf-8').splitlines()
        for row in csv.reader(csv_lines):
            date_delta = arrow.now() - arrow.get(row[1])
            age_sum += date_delta.days // 365

        return 'Age sum: {}'.format(age_sum)
    else:
        return flask.render_template('page.html')


class TestStep:
    @classmethod
    def setup_class(cls):
        app.testing = True

    def test_get(self):
        ta = flask_webtest.TestApp(app)
        resp = ta.get('/')
        assert 'Upload CSV file' in resp.text

    def test_post(self):
        ta = flask_webtest.TestApp(app)
        resp = ta.get('/')

        resp.form['csv_file'] = webtest.Upload(
            'foo.csv',
            b'foo, 2000-01-01\nbar, 1980-01-01',
            content_type='text/csv'
        )
        resp = resp.form.submit()

        assert resp.text == 'Age sum: 56'
