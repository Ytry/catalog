from flask import Flask, render_template

app = Flask(__name__)


# route to website homepage / category page
@app.route('/')
@app.route('/category')
@app.route('/categories')
def showCategories():

    return render_template('categories.html')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
