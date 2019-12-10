from flask import render_template, request, session, make_response, g,copy_current_request_context,redirect


from app.db.dbMySQL import MySQLUser,MySQLToken
from app.models import User,Token
from app.utils.generate_token import generateToken
import threading

from . import auth_bp
import datetime

from threading import Timer,Thread,Event


@auth_bp.route('/sign_in', methods=('GET', 'POST'))
def signIn():   
    
    m = MySQLUser()
    mT = MySQLToken()
    
    # verficia si el toquen que se tiene en las cookies esta registrado en la bd y devulve el usuario corresponidente
    user = mT.existToken(request.cookies.get('token'))

    if None != user:  

        # cambio de token de usuario cada cierto tiempo
        @copy_current_request_context
        def verificate():
            mT = MySQLToken()
            tokenValue = generateToken()
            t = Token(tokenValue,datetime.datetime.now(),user.token)
            #actualiza el valro del token en la bd
            mT.update(t)                       
        # inicio de ciclo infinito cambio de token
        g.user.setFunction(verificate) 
        g.user.start()        

        return render_template('home.html',user=user)

    if request.method == 'POST':
        
        # generacion de token
        tokenValue = generateToken()

        t = Token(tokenValue,datetime.datetime.now(),0)
        email = request.form['username']

        # busqueda de usario por gmail (ingresado anteriormente)       
        user = m.getOne(email)
        
        if user != None:
            
            # verificacion de password
            if user.password == request.form['password']:
                
                t.id=user.token
                mT.update(t)
                session['user'] = user.id                
                response = make_response(render_template('home.html',user=user))

                # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
                expireDate = t.date + datetime.timedelta(days=0.3)
                response.set_cookie("token",tokenValue,expires = expireDate) 

                # cambio de token de usario cada 
                @copy_current_request_context
                def verificate():
                    mT = MySQLToken()
                    tokenValue = generateToken()
                    t = Token(tokenValue,datetime.datetime.now(),user.token)
                    mT.update(t)                       
                    
                g.user.setFunction(verificate) 
                g.user.start()                                             
                
                
                return response

        return render_template('sign_in.html')        

    return render_template('sign_in.html')


@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    
    m = MySQLUser()
    if request.method == 'POST':  
        
        # generacion de token
        tokenValue = generateToken()
        t = Token(tokenValue,datetime.datetime.now(),0)
        # creacion de usario
        user = User(request.form['username'],request.form['password'],t,'0')              
        m.create(user)      
        session['user'] = user.id

        response = make_response(render_template('sign_in.html'))
        # expiracion de cookie (no es posble ponerl una espiracion menor a 0.3 dias)
        expireDate = t.date + datetime.timedelta(days=0.3)
        response.set_cookie("token",tokenValue, expires=expireDate)
        
                #return 'Email: {} \nPassword: {}'.format(user.email,user.password)
        return response
        

    return render_template('register.html')




    