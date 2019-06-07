#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database2_setup import Base, EffectAnswer, Cause, User
from flask import session as login_session
from oauth2client import client
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from apiclient import discovery
import random
import string
import httplib2
import requests
import json

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('clients_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "threads-1557767301046"

engine = create_engine('sqlite:///causeandeffectwithusers.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('clients_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
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
        return response

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
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')

    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    # Or just access_token
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # # Add provider to Login session
    login_session['provider'] = 'google'

    # See if user exists, if it doesn't make a new one
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print('Access Token is None')
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print('In gdisconnect access token is %s', access_token)
    print('User name is: ')
    print(login_session['username'])
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print('result is ')
    print(result)
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        response = redirect(url_for('showHomePage'))
        flash("You are now logged out.")
        return response
    else:
        response = make_response(json.dumps(
            'Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/threads/JSON/')
def showCausesJSON():
    causes = session.query(Cause).order_by(Cause.name)
    return jsonify(causes=[i.serialize for i in causes])


@app.route('/threads/<int:cause_id>/answers/JSON/')
def showAnswersJSON(cause_id):
    answers = session.query(EffectAnswer).filter_by(cause_id=cause_id).all()
    return jsonify(EffectAnswer=[i.serialize for i in answers])


@app.route('/threads/<int:cause_id>/answers/<int:answer_id>/JSON/')
def showAnswerJSON(cause_id, answer_id):
    cause = session.query(Cause).filter_by(id=cause_id).one()
    answer = session.query(EffectAnswer).filter_by(id=answer_id).one()
    return jsonify(cause=cause.serialize, answer=answer.serialize)


@app.route('/')
@app.route('/threads/')
def showHomePage():
    causes = session.query(Cause).order_by(Cause.name)
    return render_template('threads.html', causes=causes)


@app.route('/threads/new/', methods=['GET', 'POST'])
def newCause():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newcause = Cause(
            name=request.form['cause'], user_id=login_session['user_id'])
        session.add(newcause)
        session.commit()
        flash("New Post Created!")
        return redirect(url_for('showHomePage'))
    else:
        return render_template('newCause.html')


@app.route('/threads/<int:cause_id>/')
@app.route('/threads/<int:cause_id>/edit/', methods=['GET', 'POST'])
def editCause(cause_id):
    editedcause = session.query(
        Cause).filter_by(id=cause_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedcause.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this cause. Please create your own post.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedcause.name = request.form['cause']
            flash('Post successfully Edited %s' % editedcause.name)
            return redirect(url_for('showHomePage'))
    else:
        return render_template('editCause.html', cause=editedcause)


@app.route('/threads/<int:cause_id>/delete/', methods=['GET', 'POST'])
def deleteCause(cause_id):
    causeToDelete = session.query(
        Cause).filter_by(id=cause_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if causeToDelete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to delete this cause. Please create your own post.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(causeToDelete)
        flash('%s Successfully Deleted' % causeToDelete.name)
        session.commit()
        return redirect(url_for('showHomePage'))
    else:
        return render_template('deleteCause.html', cause=causeToDelete)


@app.route('/threads/<int:cause_id>/answers/')
def showCause(cause_id):
    cause = session.query(Cause).filter_by(id=cause_id).one()
    creator = getUserInfo(cause.user_id)
    answers = session.query(EffectAnswer).filter_by(
        cause_id=cause_id).all()
    return render_template('list.html', cause=cause, answers=answers, cause_id=cause.id, creator=creator)


@app.route('/threads/<int:cause_id>/answers/new/', methods=['GET', 'POST'])
def newEffectAnswer(cause_id):
    if 'username' not in login_session:
        return redirect('/login')
    cause = session.query(Cause).filter_by(id=cause_id).one()
    if request.method == 'POST':
        newAnswer = EffectAnswer(name=request.form['name'], solution=request.form['solution'],
                                 importance=request.form['importance'], area=request.form['area'], cause_id=cause_id, user_id=cause.user_id)
        session.add(newAnswer)
        session.commit()
        flash("New Solution Created!")
        return redirect(url_for('showCause', cause_id=cause_id))
    else:
        return render_template('newEffectAnswer.html', cause_id=cause_id)


@app.route('/threads/<int:cause_id>/answers/<int:answer_id>/edit', methods=['GET', 'POST'])
def editEffectAnswer(cause_id, answer_id):
    if 'username' not in login_session:
        return redirect('/login')
    cause = session.query(Cause).filter_by(id=cause_id).one()
    editedAnswer = session.query(EffectAnswer).filter_by(id=answer_id).one()
    if login_session['user_id'] != cause.user_id:
        return "<script>function myFunction() {alert('You are not authorized to edit this idea. Please write your own idea.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedAnswer.name = request.form['name']
        if request.form['solution']:
            editedAnswer.solution = request.form['solution']
        if request.form['importance']:
            editedAnswer.importance = request.form['importance']
        if request.form['area']:
            editedAnswer.area = request.form['area']
        session.add(editedAnswer)
        session.commit()
        flash("solution has been changed.")
        return redirect(url_for('showCause', cause_id=cause_id))
    else:
        return render_template('editEffectAnswer.html', cause_id=cause_id, answer_id=answer_id, item=editedAnswer)


@app.route('/threads/<int:cause_id>/answers/<int:answer_id>/delete', methods=['GET', 'POST'])
def deleteEffectAnswer(cause_id, answer_id):
    if 'username' not in login_session:
        return redirect('/login')
    answerToDelete = session.query(EffectAnswer).filter_by(id=answer_id).one()
    cause = session.query(Cause).filter_by(id=cause_id).one()
    if login_session['user_id'] != cause.user_id:
        return "<script>function myFunction() {alert('You are not authorized to delete this idea. Please write your own idea.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        session.delete(answerToDelete)
        session.commit()
        flash("answer has been deleted.")
        return redirect(url_for('showCause', cause_id=cause_id))
    else:
        return render_template('deleteEffectAnswer.html', item=answerToDelete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
