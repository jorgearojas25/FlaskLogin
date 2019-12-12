import mysql.connector
from app.models import User,Token
import datetime

class ConnectionMySQL:
    
    def connect(self):
        config = {
            'host' :'localhost',
            'user' :'root',
            'password' : 'rootmysql2019',
            'database' : 'db_login',
            'port' : "3306"
        }
        
        self.db = mysql.connector.connect(**config)        
        return self.db.cursor() 
        


class MySQLUser:

    connectionMySQL = ConnectionMySQL()

    def __init__(self):
        self.cursor = self.connectionMySQL.connect()    
        

    def create(self, user):

        mT = MySQLToken()
        mT.create(user.token)
        idToken = mT.getLastIdToken()
               
        sql ="INSERT INTO users (email, password, idtoken) VALUES (%s, %s, %s)"
        val = (user.email, user.password, idToken,) 
        try:
            self.cursor.execute(sql,val)            
        except:
            return False       
        
        self.connectionMySQL.db.commit()
        return True

        
        

    def getOne(self, email):

        sql = "SELECT * FROM users WHERE email='{}'".format(email)
        self.cursor.execute(sql)
        query = self.cursor.fetchone()
        if query == None:
            return None
        return self.queryToUser(query)

    def getOneByToken(self, idToken):

        sql = "SELECT * FROM users WHERE idtoken='{}'".format(idToken)
        
        self.cursor.execute(sql)
        query = self.cursor.fetchone()
        if query == None:
            return None
        return self.queryToUser(query)
        

    def update(self, user):
        pass

    def delete(self, idObject):
        pass

    def getAll(self):
        pass

    def queryToUser(self, query):

        return User(query[1],query[2],query[3],query[0])


class MySQLToken:

    connectionMySQL = ConnectionMySQL()

    def __init__(self):
        self.cursor = self.connectionMySQL.connect()
   
        

    def create(self, token):
        sql ="INSERT INTO tokens (value, date) VALUES (%s, %s)"
        val = (token.value, token.date)
        self.cursor.execute(sql,val) 
        self.connectionMySQL.db.commit()


    def getOne(self, idToken):
        sql = "SELECT * FROM tokens WHERE idtokens='{}'".format(idToken)
        self.cursor.execute(sql)
        return self.queryToToken(self.cursor.fetchone())

    def update(self, token):
        sql ="UPDATE tokens SET value = %s, date = %s WHERE idtokens = '{}'".format(token.id)
        val = (token.value, token.date)
        self.cursor.execute(sql,val) 
        self.connectionMySQL.db.commit()

    def delete(self, idObject):
        pass

    def getAll(self):
        pass

    def getLastIdToken(self):
        return self.cursor.lastrowid

    def queryToToken(self,query):
        return Token(query[1],query[2],query[0])

    def existToken(self, token):
        sql = "SELECT * FROM tokens WHERE value = '{}'".format(token)
        self.cursor.execute(sql)
        query = self.cursor.fetchone()
        if query == None:
            return None
        m = MySQLUser()
        user = m.getOneByToken(query[0])
        return user