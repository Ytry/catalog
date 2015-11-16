# import flask dependencies
from flask import Flask, render_template, url_for, redirect, request, flash
from flask import session as login_session
from flask import make_response, jsonify

# import sqlalchemy dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import oauth dependencies
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

# import database classes
from database_setup import Base, Category, Item, User

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

# connect to database and create a session to perform CRUD opperations on it
engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Route to login page
@app.route('/login')
def showLogin():

    # generate an anti-forgery state key to prevent session hijacking
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state

    return render_template('login.html', STATE=state)


# route to google plus connection
@app.route('/gconnect', methods=['POST'])
def gconnect():

    # check to make sure the token sent to the server and client are the same
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:

        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    # Failed to upgrade authorization code
    except FlowExchangeError:

        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    # If there was an error in the access token info, abort.
    if result.get('error') is not None:

        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:

        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:

        response = make_response(
            json.dumps("Token's client ID doesn't match app's."), 401)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_credentials is not None and gplus_id == stored_gplus_id:

        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'

        return response

    # Store the access token in the session for later use.
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['email'] = data['email']

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(login_session['email'])

    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    flash("you are now logged in as %s" % login_session['username'])
    return output


# DISCONNET - Revoke a current user's token and reset their login_session.
@app.route("/gdisconnect")
def gdisconnect():

    # Only disconnect a connected user
    credentials = login_session.get('credentials')

    if credentials is None:

        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-type'] = 'application/json'

        return response

    # Execute HTTP GET request to revoke current token.
    access_token = credentials
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':

        # Reset the user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:

        # For whatever reason, the given token was invalid.
        response = make_response(json.dumps(
            'Failed to revoke token for given user.'), 400)
        response.headers['Content-type'] = 'applications/json'


# route to website homepage / category page
@app.route('/')
def showCategories():

    return redirect(url_for('showItems', category_id=1))


# route to categories page for a specific category of items
@app.route('/category/<int:category_id>')
def showItems(category_id):

    categories = session.query(Category).all()
    items = session.query(Item).filter_by(category_id=category_id).all()
    if 'username' not in login_session:

        return render_template(
            'publicCategories.html', items=items, categories=categories)
    else:
        return render_template(
            'categories.html', items=items, categories=categories)


# route to edit an item
@app.route('/edit/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
def editItem(item_id, category_id):

    editedItem = session.query(Item).filter_by(id=item_id).one()

    if 'username' not in login_session:

        return redirect('/login')

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

    if 'username' not in login_session:

        return redirect('/login')

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

    if 'username' not in login_session:

        return redirect('/login')

    if request.method == 'POST':

        newItem = Item(name=request.form['add_name'], description=request.form[
            'add_description'], category=category)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('addItem.html', category_id=category_id)


# JSON APIs to view all items
@app.route('/items/JSON')
def itemsJSON():

    items = session.query(Item).all()

    return jsonify(Items=[i.serialize for i in items])


# JSON APIs to view categories
@app.route('/categories/JSON')
def categoriesJSON():

    categories = session.query(Category).all()

    return jsonify(Categories=[i.serialize for i in categories])


# JSON APIs to view a category of items
@app.route('/category/<int:category_id>/JSON')
def categoryJSON(category_id):

    items = session.query(Item).filter_by(category_id=category_id).all()

    return jsonify(Items=[i.serialize for i in items])


# return a user id given their email
def getUserID(email):

    try:

        user = session.query(User).filter_by(email=email).one()

        return user.id

    except:

        return None


# return all info about a user given their ID
def getUserInfo(user_id):

    user = session.query(User).filter_by(id=user_id).one()
    return user


# create a user
def createUser(login_session):

    newUser = User(name=login_session['username'], email=login_session[
        'email'])
    session.add(newUser)
    session.commit
    user = session.query(User).filter_by(email=login_session['email']).one()

    return user.id


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
