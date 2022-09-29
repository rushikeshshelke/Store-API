import sqlite3
from flask_restful import Resource, reqparse
from commonLibs.globalVariables import GlobalVariables
from models.user import UserModel

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
        user = UserModel.findByUsername(reqData['username'])
        if user:
            GlobalVariables.LOGGER.info("User '{}' already exists.".format(reqData['username']))
            return {"message":"User '{}' already exists.".format(reqData['username'])}, 409
        user = UserModel(reqData['username'],reqData['password'])
        user.saveToDB()
        
        GlobalVariables.LOGGER.info("User '{}' created successfully.".format(reqData['username']))
        return {"message":"User '{}' created successfully.".format(reqData['username'])}, 201