from datetime import datetime
from sqlite3 import IntegrityError
from flask import Flask, Blueprint, request, redirect, render_template, session, send_from_directory, jsonify
from database.Dbase import *
from services.DataService import *

data = Blueprint('data', __name__, url_prefix='/data')


@data.route("/sign-up")
def signup():
    # Check if user logged in before continuing
    if 'email' in session:
        return redirect("/data/view")
    
    return render_template('signup.html')


@data.route("/create-user", methods=['POST'])
def createUser():
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
    

@data.route("/view")
def loadData():
    # Session check
    if 'email' not in session:
        return render_template('login.html')
    
    # Fetch all drivers from the database
    drivers = DataService.driverData(session['email'])

    documents = DataService.docData(session['email'])

    return render_template("view.html", driverData=drivers, docData = documents, user=session['email'])


@data.route("/update", methods=['POST'])
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
        
    # Catch unique constraint
    except IntegrityError as e:
        errorMessage = 'Driver already exists!'
        return jsonify({'error': errorMessage}), 400
  

# Delete document
@data.route('/delete_document', methods=['POST'])
def delete_document():
    document_name = request.form['document_name']
    document_date = request.form['document_date']
    driver_id = request.form['driver_id']
    
    Dbase.deleteDoc(document_name, document_date, driver_id)
    
    return redirect("/data/view?driver_id=" + driver_id)


# Delete driver
@data.route('/delete_driver', methods=['POST'])
def delete_driver():
    driver_id = request.form['driver_id']
    
    Dbase.deleteDriver(driver_id)
    
    return redirect("/data/view")