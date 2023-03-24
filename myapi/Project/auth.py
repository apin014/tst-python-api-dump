from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify
from flask_jwt_extended import (
    get_csrf_token, create_access_token,
    get_jwt_identity, set_access_cookies, get_jwt, 
    unset_jwt_cookies
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, main
from datetime import timedelta, datetime

auth = Blueprint('auth', __name__)

""" @auth.route('/login')
def login():
    return render_template('login.html') """

@auth.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        """ flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page """
        return jsonify({"login":False, 'msg':'user not found, check login details and try again'})
    
    # if the above check passes, then we know the user has the right credentials
    access_token = create_access_token(identity=user.name)
    
    resp = jsonify({
        'access_csrf': get_csrf_token(access_token)
    })
    
    set_access_cookies(resp, access_token)
    
    return resp, 200

#implicit token refreshing
@main.main.after_request
def refresh_expiring_jwts(resp):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now()
        target_timestamp = datetime.timestamp(now + timedelta(minutes=1))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(resp, access_token)
        return resp
    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return resp
    
""" @auth.route('/signup')
def signup():
    return render_template('signup.html') """

@auth.route('/signup', methods=['POST'])
def signup_post():
    # code to validate and add user to database goes here
    username = request.json.get('username')
    name = request.json.get('name')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first() # if this returns a user, then the username already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        """ flash('username already exists')
        return redirect(url_for('auth.signup')) """
        return jsonify({'signup':False, 'msg':'User with same username already exists'})

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'signup':True})

@auth.route('/logout', methods=['POST'])
def logout():
    resp = jsonify({'logout':True})
    unset_jwt_cookies(resp)
    return resp, 200