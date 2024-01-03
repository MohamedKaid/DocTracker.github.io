from flask import flash, Blueprint, request, redirect, render_template, session, current_app, jsonify, url_for
from database.Dbase import *
from itsdangerous import URLSafeTimedSerializer
from services.EmailService import *
from services.TokenHandler import *

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route("/")
def logInPage():
    # Check if email is already in session and exists in database
    if "email" in session:
        if Dbase.isEmailExist(session['email']):
            return redirect("/data/view")
        
        # Email in session but doesn't exist
        return redirect(url_for("account.logout"))
    
    return render_template('login.html')


@auth.route("/log-in", methods=['POST'])
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


@auth.route("/forgot-pin", methods=['GET', 'POST'])
def forgotPin():
    em = EmailService()
    
    if request.method == 'POST':
        # Retrieve email
        email = request.form['email']

        # Generate token
        token = TokenHandler.generateToken(email)

        # Create and send reset url
        reset_url = url_for('auth.resetPin', token=token, _external=True)
        em.sendEmail(email, reset_url, 'reset')

        #TODO: Display page with 'check email' message
        return redirect(url_for('index'))
    
    # Render forgot pin page on GET request
    return render_template('forgotPin.html')


@auth.route("/reset-pin/<token>", methods=['GET', 'POST'])
def resetPin(token):
    if request.method == 'POST':
        # Retrieve email and new pin
        email = TokenHandler.retrieveEmail(token)
        new_pin = request.form['new_pin']
        old_pin = Dbase.getPin(email)

        #Updating the password to the database
        Dbase.changePass(email,old_pin,new_pin)

        # Redirect to login upon successful pin reset
        flash('Your password has been reset successfully')
        return redirect(url_for('auth.logInPage'))
    
    # Render reset pin page on GET request
    return render_template('resetPin.html', token=token)
    