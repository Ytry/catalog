# import flask dependencies
from flask import Flask, render_template, url_for, redirect, request

# import sqlalchemy dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import oauth dependencies
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# import database classes
from database_setup import Base, Category, Item

# import python modules
import random
import string
import httplib2
import json
import requests


app = Flask(__name__)

# oAuth2 client info file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Catalog App"


# Route to login page
@app.route('/login')
def showLogin():

    # generate an anti-forgery state key to prevent session hijacking
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)

# connect to database and create a session to perform CRUD opperations on it
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# route to website homepage / category page
@app.route('/')
def showCategories():

    return redirect(url_for('showItems', category_id=1))


# route to categories page for a specific category of items
@app.route('/category/<int:category_id>')
def showItems(category_id):

    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    return render_template(
        'categories.html', items=items, categories=categories)


# route to edit an item
@app.route('/edit/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id, category_id):

    editedItem = session.query(Item).filter_by(id=item_id).one()

    if request.method == 'POST':

        if request.form['name']:

            editedItem.name = request.form['name']

        if request.form['description']:

            editedItem.description = request.form['description']

        session.add(editedItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
            'edit.html', category_id=category_id, item_id=item_id, item=editedItem)  # noqa


# Delete an item from the database
@app.route('/delete/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
def deleteItem(item_id, category_id):

    deletedItem = session.query(Item).filter_by(id=item_id).one()

    if request.method == 'POST':

        if request.form['name'] == deletedItem.name:

            session.delete(deletedItem)
            session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item_id=item_id, item=deletedItem)  # noqa


# add an item to the database
@app.route('/new/<int:category_id>/', methods=['GET', 'POST'])
def addItem(category_id):

    category = session.query(Category).filter_by(id=category_id).one()

    if request.method == 'POST':

        newItem = Item(name=request.form['add_name'], description=request.form[
            'add_description'], category=category)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('addItem.html', category_id=category_id)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
