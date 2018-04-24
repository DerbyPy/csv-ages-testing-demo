Integration and Unit Testing Examples
=====================================

This repo is a simple demonstration of testing a small flask app.  It also demonstrates
refactoring integration tests into unit tests.


Running the Tests
-----------------

Assuming you have [pipenv](https://docs.pipenv.org/) installed:

```
$ pipenv run pytest step*
...................                 [100%]
19 passed in 0.34 seconds

```

Running the App
---------------

```
FLASK_APP=step1.py pipenv run flask run
```


Brief Explanation
------------------

The goal of the app in each of the four steps is to display a form with a CSV upload.  Upon uploading a CSV file to the form, the app calculates the age of the people in the file and displays that value.

It's assumed the CSV is in the form of `name, dob` and in later steps it can also be `name, dob, gender`.  Example:


```
foo, 2000-06-18
bar, 1977-12-29, m
```

* `step1.py`: Tests are present, but high level.  Everything is tested by going through the entire WSGI stack.
* `step2.py`: Our logic is getting more complex.  Blank names are skipped and females older than 39 have their age fixed at 39.  The code and the tests are both starting to feel bloated.
* `step3.py`: We begin to refactor the "integration" tests into unit tests and fix a bug in the process.
* `step4.py`: We finish the refactor creating a hierarchy of tests.

