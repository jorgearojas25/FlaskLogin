class User:

    def __init__(self, email, password, token, idUser):
        self.email = email
        self.password = password
        self.token = token
        self.id = idUser
    
    def validatePassword(self,password2):
        if self.password == password2:
            return True
        return False

class Token:

    def __init__(self, value, date, idToken):
        self.value = value
        self.date = date
        self.id = idToken
        