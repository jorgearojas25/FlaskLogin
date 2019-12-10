from flask import render_template, request, session, make_response, g,Flask
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
    

    user = mT.existToken(request.cookies.get('token'))

    if None != user:  

        return render_template('home.html',user=user)

    if request.method == 'POST':
        
        tokenValue = generateToken()

        t = Token(tokenValue,datetime.datetime.now(),0)
        email = request.form['username']        
        user = m.getOne(email)
        
        if user != None:

            if user.password == request.form['password']:
                
                t.id=user.token
                mT.update(t)
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
    if request.method == 'POST':  
        
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        user = User(request.form['username'],request.form['password'],t,'0')
              
        m.create(user)       
        session['user'] = user.id                
        response = make_response(render_template('sign_in.html'))
        response.set_cookie("token",tokenValue)
        
                #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
        return response

        

    return render_template('register.html')

app = Flask(__name__, instance_relative_config=True)
@app.route('/home', methods=('GET', 'POST'))
def home(): 
    return render_template('home.html')