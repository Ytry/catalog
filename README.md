# catalog

CATALOG WEB SITE
=====================

This program was written and tested in python 3. It may work in python 2 but has not been tested

Frameworks / apis
=================

- oAuth - http://oauth.net/

- sql alchemy - http://www.sqlalchemy.org/

- flask - http://flask.pocoo.org/

- bootstrap - http://getbootstrap.com/

SETUP
============

To setup and run the website install the required dependiences listed above then run datebase_setup.py

Once you have the database generated run lotsofitems.py to populate it

Once that is done make sure you have port 5000 forwarded, and run project.py

APIs
=========

All of the database information is available via JSON

the urls for such information are as follows:

JSON APIs to view a category of items
/category/category_id>/JSON

JSON APIs to view categories
/categories/JSON

JSON APIs to view all items
/items/JSON

AUTHORS / CREDITS
===================

Kyle Lick

I used code from projects done in the oAuth class as well fullstack fundamentals class for udacity so credits to the authors of that code

