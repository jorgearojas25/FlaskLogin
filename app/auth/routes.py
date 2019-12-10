from flask import render_template, request, session, make_response, g
import datetime


from app.db.dbMySQL import MySQLUser,MySQLToken
from app.models import User,Token
from app.utils.generate_token import generateToken
import threading

from . import auth_bp

from threading import Timer,Thread,Event






    


@auth_bp.route('/sign_in', methods=('GET', 'POST'))
def signIn():
    
    m = MySQLUser()
    mT = MySQLToken()

    

    user = g.db[1].existToken(request.cookies.get('token'))

    if None != user:  

        return render_template('home.html',user=user)

    if request.method == 'POST':
        
        tokenValue = generateToken()

        t = Token(tokenValue,datetime.datetime.now(),0)
        email = request.form['username']        
        user = g.db[0].getOne(email)
        
        if user != None:

            if user.password == request.form['password']:
                
                t.id=user.token
                g.db[1].update(t)
                session['user'] = user.id                
                response = make_response(render_template('home.html',user=user))
                response.set_cookie("token",tokenValue)
                
                #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
                return response

        return render_template('sign_in.html')        

    return render_template('sign_in.html')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register(): 
    m = MySQLUser()
    mT = MySQLToken()

    
    if request.method == 'POST':  
        
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        user = User(request.form['username'],request.form['password'],t,'0')
              
        g.db[0].create(user)
        print('sei tenrts...............................')  
        session['user'] = user.id                
        response = make_response(render_template('sign_in.html'))
        response.set_cookie("token",tokenValue)
        
                #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
        return response

        

    return render_template('register.html')
