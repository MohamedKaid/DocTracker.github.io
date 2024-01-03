from flask import Flask, request, redirect, render_template, session, send_from_directory, jsonify
from sqlite3 import IntegrityError
from werkzeug.exceptions import BadRequestKeyError
from database.Dbase import *
from services.DataService import *
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'mindFreak'  # Set a secret key for session security


#Paths are defined relative to flask application rather than the filesystem therefore function to retrieve a file is necessary
@app.route('/static/<path:filename>')
def serve_css(filename):
    return send_from_directory('static', filename, mimetype='text/css')


@app.route('/')
def index():
    return redirect('/loginPage')


@app.route("/loginPage")
def navLogin():
    # Check if email is already in session and exists in database
    if "email" in session:
        if Dbase.isEmailExist(session['email']):
            return redirect("/data")
    else:
        return render_template('newLogin.html')


@app.route("/login", methods=['POST'])
def logIn():
    # Login attempt
    email = request.form['email']
    pin = int(request.form['pin'])
    # Get stored pin
    returnPin = Dbase.logIn(email)

    # Validate login
    if pin == returnPin:
        # Set session email
        session['email'] = email

        # Return 'success' response
        return jsonify({'success': 'good'}), 200
    else:
        # Return 'bad request' response
        msg = 'Incorrect email or pin'
        return jsonify({'error': msg}), 400


@app.route("/forgot-pin")
def navForgotPin():
    return render_template('forgotPin.html')


@app.route("/data")
def loadData():
    # Fetch all drivers from the database
    drivers = DataService.driverData(session['email'])

    documents = DataService.docData(session['email'])

    return render_template("listPage.html", driverData=drivers, docData = documents, user=session['email'])


@app.route("/signUp.html")
def navSignup():
    return render_template('newSignup.html')


@app.route("/create-user", methods=['POST'])
def createUser():
    # Check if user logged in before continuing
    if 'email' in session:
        return redirect("/data")

    # New user data to be written
    # name = request.form['name']
    email = request.form['email']
    # username = request.form['username']
    pin = request.form['pin']

    # Write new user data and set session email
    try:
        Dbase.addDispatcher(email, pin)
        session['email'] = email

        return jsonify({'success': 'good'}), 200
    
    except sqlite3.IntegrityError as e:
        errorMessage = "Email already in use"
        return jsonify({'error': errorMessage}), 400


@app.route("/update", methods=['POST'])
def addData():
    # Get type of form (Add driver/Add document)
    form = request.form['form-type']
    email = session["email"]

    try:
        # Handle adding driver
        if form == 'driver':
            # Data to be written
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            name = first_name+" "+last_name

            # Writing data - throws exception if already exists
            driverId = Dbase.addDriver(name.title(),email)
            return jsonify({'success': driverId}), 200
    
        # Handle adding document
        elif form == 'document':
            # Request the data from the fontend
            driver_id = request.form['driver_id']
            doc_name = request.form['doc_name']
            exp_date = request.form['exp_date']
            
            # Convert the exp_date format from "%Y-%m-%d" to "%m-%d-%Y"
            temp = datetime.strptime(exp_date, "%Y-%m-%d")
            exp_date_format = temp.strftime("%m-%d-%Y")
            
            # Writing data TODO: throw exception
            Dbase.addDcoument(doc_name, exp_date_format, driver_id)
            return jsonify({'success': driver_id}), 200
        
        # Successful form submission being handled asynchronously by client-side AJAX logic
        # return statement below won't be reached
        return redirect("/data")
            
    except IntegrityError as e:
        errorMessage = 'Driver already exists!'
        return jsonify({'error': errorMessage}), 400
    
    
# Delete document
@app.route('/delete_document', methods=['POST'])
def delete_document():
    document_name = request.form['document_name']
    document_date = request.form['document_date']
    driver_id = request.form['driver_id']
    
    Dbase.deleteDoc(document_name, document_date, driver_id)
    
    return redirect("/data?driver_id=" + driver_id)


# Delete driver
@app.route('/delete_driver', methods=['POST'])
def delete_driver():
    driver_id = request.form['driver_id']
    
    Dbase.deleteDriver(driver_id)
    
    return redirect("/data")


# Render settings page
@app.route("/settings")
def settings():
    return render_template("/settings.html", user=session['email'])


# Attempt to update email or pin
@app.route("/update-user-info", methods=['POST'])
def updateUser():
    # Data type user wants to update, current password, new value
    newValueType = request.form['newValue']
    currentPass = request.form['current-password']
    newValue = request.form[newValueType]

    # Attempt update
    try:
        if newValueType == 'email':
            Dbase.changeEmail(session['email'], newValue)
            session['email'] = newValue
        elif newValueType == 'password':
            Dbase.changePass(session['email'], currentPass, newValue)

    # Return error
    except Exception as e:
        return jsonify({'error': 'Incorrect password'}), 400

    # Return success
    return jsonify({'success': 'Success'}), 200


# Log out
@app.route("/logout") 
def logout():
    session.pop("email", None)
    return redirect("/")
    
# forgot pin
@app.route("/forgotPin.html")
def navForgotPin():
    return render_template('forgotPin.html')

@app.route("/forgot-pin", methods=['POST'])
def forgotPin():
    email = request.form['email']
    pin = Dbase.getPin(email)
    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    
#---------------this function is used for debuging-----------------------#
# @app.route("/signup", methods=['POST'])
# def extractInfo():
#     try:
#         print(request.__dict__)  # Print the entire request object
#         print(request.form)       # Print the form data
#         name = request.form.get('name', '')
#         email = request.form.get('email', '')
#         username = request.form.get('username', '')
#         pin = request.form.get('pin', '')

#         print(f"Name: {name}, Email: {email}, Username: {username}, PIN: {pin}")

#         # Comment out the database operation for debugging
#         # Dbase.addDispatcher(name, username, email, pin)

#         return jsonify({'success': True, 'message': 'Data processed successfully'})
#     except BadRequestKeyError as e:
#         return jsonify({'success': False, 'message': f'Error: {e}'})
        





# app = Flask(__name__)
# makeFileObj = rwFiles()
# makeFolder = makeFolder()
# Dbase = Dbase()

# @app.route('/')
# def index():
#     Dbase.setUpDB()
#     return render_template('homePage.html')
 

# @app.route("/signup", methods=['POST'])
# def extractInfo():
#         name=request.form['name']
#         email=request.form['email']
#         username = request.form['username']
#         pin = request.form['pin']
#         Dbase.addDipatcher(name,username,email,pin)
        
        
# if __name__ == '__main__':
#     app.run(debug=True)
    
    
# from backEnd.auth import *

# driverList = [Driver(*driver) for driver in driverRecords]
# driverList = [{'name': driver.name, 'id': driver.driver_id} for driver in driverRecords]