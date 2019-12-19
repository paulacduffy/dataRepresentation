from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, session, flash
from stockDAO import stockDAO
from accountsDAO import accountsDAO
from functools import wraps


#from flask_cors import CORS
app = Flask(__name__, static_url_path='', static_folder='.')
#CORS(app)



#def login_required(f):
   # @wraps(f)
    #def wrap(*args, **kwargs):
     #   if 'logged_in' in session:
      #      return f(*args, **kwargs)
       # else:
        #    flash('You need to login first')
         #   return redirect(url_for('/'))
    #return wrap

@app.route('/')
#@login_required
def pageone():
    return render_template('pageone.html')


@app.route('/stafflogin/', methods=['GET', 'POST'])
#@login_required
def stafflogin():
    error = None
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        error = 'Invalid Credentials. Please try again.'
        account = accountsDAO.fetchone()
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            #session['id'] = account['id']
            session['username'] = account['username']
            session['password'] = account['password']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

           
    return render_template('stafflogin.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You have logged out!')
    return redirect(url_for('pageone'))

@app.route('/stock')
def getAll():
    #print("in getall")
    results = stockDAO.getAll()
    return jsonify(results)


@app.route('/stock/<int:id>')
def findById(id):
    foundStock = stockDAO.findByID(id)

    return jsonify(foundStock)


@app.route('/stock', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    stock = {
        "itemtype": request.json['itemtype'],
        "label": request.json['label'],
        "price": request.json['price'],
    }
    values =(stock['itemtype'],stock['label'],stock['price'])
    newId = stockDAO.create(values)
    stock['id'] = newId
    return jsonify(stock)


@app.route('/stock/<int:id>', methods=['PUT'])
def update(id):
    foundStock = stockDAO.findByID(id)
    if not foundStock:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'itemtype' in reqJson:
        foundStock['itemtype'] = reqJson['itemtype']
    if 'label' in reqJson:
        foundStock['label'] = reqJson['label']
    if 'price' in reqJson:
        foundStock['price'] = reqJson['price']
    values = (foundStock['itemtype'],foundStock['label'],foundStock['price'],foundStock['id'])
    stockDAO.update(values)
    return jsonify(foundStock)
        

    

@app.route('/stock/<int:id>' , methods=['DELETE'])
def delete(id):
    stockDAO.delete(id)
    return jsonify({"done":True})




if __name__ == '__main__' :
    app.run(debug= True)