import csv

import arrow
import flask
from flask import request
import flask_webtest
from freezegun import freeze_time
import webtest

app = flask.Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        csv_file = request.files['csv_file']

        age_sum = 0

        csv_lines = csv_file.read().decode('utf-8').splitlines()
        for row in csv.reader(csv_lines):
            if len(row) == 2:
                name, dob = row
                gender = None
            else:
                name, dob, gender = row

            if name == '':
                continue

            age_sum += calc_age(dob, gender)

        return 'Age sum: {}'.format(age_sum)
    else:
        return flask.render_template('page.html')


def calc_age(dob, gender):
    date_delta = arrow.now() - arrow.get(dob)
    age = date_delta.days // 365
    if gender == 'f' and age > 39:
        return 39
    return age


class TestWeb:
    @classmethod
    def setup_class(cls):
        app.testing = True

    def test_get(self):
        ta = flask_webtest.TestApp(app)
        resp = ta.get('/')
        assert 'Upload CSV file' in resp.text

    def test_age_sum(self):
        ta = flask_webtest.TestApp(app)
        resp = ta.get('/')

        resp.form['csv_file'] = webtest.Upload(
            'foo.csv',
            b'foo, 2000-01-01\nbar, 1980-01-01',
            content_type='text/csv'
        )
        resp = resp.form.submit()

        assert resp.text == 'Age sum: 56'

    def test_age_sum_blank_name_not_counted(self):
        ta = flask_webtest.TestApp(app)
        resp = ta.get('/')

        resp.form['csv_file'] = webtest.Upload(
            'foo.csv',
            b'foo, 2000-01-01\nbar, 1980-01-01\n,2010-01-01',
            content_type='text/csv'
        )
        resp = resp.form.submit()

        assert resp.text == 'Age sum: 56'


class TestCalcAge:

    @freeze_time('2020-06-01')
    def test_normal(self):
        assert calc_age('2000-04-13', None) == 20

    @freeze_time('2020-06-01')
    def test_male_over_39(self):
        assert calc_age('1970-04-13', 'm') == 50

    @freeze_time('2020-06-01')
    def test_female_over_39(self):
        assert calc_age('1970-04-13', 'f') == 39
