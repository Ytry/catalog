# import flask dependencies
from flask import Flask, render_template, url_for, redirect
from flask import Flask, render_template, url_for, redirect, request

# import sqlalchemy dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database classes
from database_setup import Base, Category, Item


app = Flask(__name__)

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

            editItem.description = request.form['description']

        session.add(editedItem)
        session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
            'edit.html', category_id=category_id, item_id=item_id, item=editedItem)  # noqa


@app.route('/delete/<int:category_id>/<int:item_id>', methods=['GET', 'POST'])
def deleteItem(item_id, category_id):

    deletedItem = session.query(Item).filter_by(id=item_id).one()

    if request.method == 'POST':

        if request.form['name'] == deletedItem.name:

            session.delete(deleteItem)
            session.commit()

        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template('deleteItem.html', category_id=category_id, item_id=item_id, item=deletedItem)  # noqa


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
