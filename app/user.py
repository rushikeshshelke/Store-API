import sqlite3
from flask_restful import Resource, reqparse
from app.globalVariables import GlobalVariables

class User:

    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password
    
    @classmethod
    def findByUsername(cls,username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        SELECT_QUERY = GlobalVariables.SELECT_USERS_BY_UNAME
        result = cursor.execute(SELECT_QUERY,(username,))
        row = result.fetchone()
        GlobalVariables.LOGGER.info("Find by username : {}".format(row))
        if row:
            user =  cls(row[0],row[1],row[2])
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def findById(cls,_id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        SELECT_QUERY = GlobalVariables.SELECT_USERS_BY_UID
        result = cursor.execute(SELECT_QUERY,(_id,))
        row = result.fetchone()
        GlobalVariables.LOGGER.info("Find by id : {}".format(row))
        if row:
            user =  cls(row[0],row[1],row[2])
        else:
            user = None
        connection.close()
        return user

class UserRegister(Resource):

    def parseReqBody(self):
        reqParser = reqparse.RequestParser()
        reqParser.add_argument('username',
        type=str,
        required=True,
        help="This field can not be left blank!")

        reqParser.add_argument('password',
        type=str,
        required=True,
        help="This field can not be left blank!")
        return reqParser.parse_args()

    def post(self):
        reqData = self.parseReqBody()        
        user = User.findByUsername(reqData['username'])
        if user:
            GlobalVariables.LOGGER.info("User '{}' already exists.".format(reqData['username']))
            return {"message":"User '{}' already exists.".format(reqData['username'])}, 409

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        cursor.execute(GlobalVariables.INSERT_INTO_USERS,(reqData['username'],reqData['password']))
        
        connection.commit()
        connection.close()
        GlobalVariables.LOGGER.info("User '{}' created successfully.".format(reqData['username']))
        return {"message":"User '{}' created successfully.".format(reqData['username'])}, 201