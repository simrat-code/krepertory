# KRepertory
Homeopathy card repertory based using RESTful API for Web-Application.

Card Repertory is a visual sorting system, which helps physician by eliminating the non-common medicines between the choosen rubics. 
For example, intersection between two or more sets.

for local run:
$ gunicorn --bind 127.0.0.1:5000 wsgi:app

launch browser > enter "http://127.0.0.1:5000/krep/home"
