import os

from flask import Flask, redirect,g
from app.db.dbMySQL import MySQLUser,MySQLToken
from app.utils.temp_toke import perpetualTimer


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True,static_url_path='/static')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )   

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)    
    

    

    @app.before_request
    def before_request():
        # valor de 10 segundos cambio de token de usuario
        tempToken = perpetualTimer(10)
        g.user = tempToken

    @app.route('/')
    def hello():
        
        return redirect('/auth/sign_in')
    
    # register blueprint

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    return app