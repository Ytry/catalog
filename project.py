# import flask dependencies
from flask import Flask, render_template

# import sqlalchemy dependencies
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import database classes
from database_setup import Base, Category, Item


app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# route to website homepage / category page
@app.route('/')
@app.route('/category')
@app.route('/categories')
def showCategories():

    return render_template('categories.html')


@app.route('/item/<int:category_id>/<int:item_id>')
def showItem(category_id, item_id):

    return render_template('item.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
