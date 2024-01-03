from flask import Flask, Blueprint, request, redirect, render_template, session, send_from_directory, jsonify
from database.Dbase import *
import os

account = Blueprint('account', __name__, url_prefix='/account')


# Render account page
@account.route("/settings")
def settings():
    print("dir" + os.getcwd())
    return render_template("/settings.html", user=session['email'])


# Attempt to update email or pin
@account.route("/update-user-info", methods=['POST'])
def updateUser():
    # Data type user wants to update, current password, new value
    newValueType = request.form['newValue']
    currentPass = request.form['current-password']
    newValue = request.form[newValueType]

    # Attempt update
    try:
        if newValueType == 'email':
            Dbase.changeEmail(session['email'], currentPass, newValue)
            session['email'] = newValue
        elif newValueType == 'password':
            Dbase.changePass(session['email'], currentPass, newValue)

    # Return error
    except Exception as e:
        return jsonify({'error': 'Incorrect password'}), 400

    # Return success
    return jsonify({'success': 'Success'}), 200


# Log out
@account.route("/logout") 
def logout():
    session.pop("email", None)
    return redirect("/")
