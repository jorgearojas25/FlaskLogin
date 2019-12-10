import datetime


def generateToken():
    return str(hash(datetime.datetime.now()))

