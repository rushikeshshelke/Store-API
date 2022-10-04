import sqlite3
from flask_restful import Resource, reqparse
from commonLibs.globalVariables import GlobalVariables
from models.user import UserModel
from commonLibs.commonConfigs import CommonConfigs
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
    )

class UserRegister(Resource):

    def post(self):
        reqData = CommonConfigs().parseReqBody()        
        user = UserModel.findByUsername(reqData['username'])
        if user:
            GlobalVariables.LOGGER.info("User '{}' already exists.".format(reqData['username']))
            return {"message":"User '{}' already exists.".format(reqData['username'])}, 409
        user = UserModel(reqData['username'],reqData['password'])
        user.saveToDB()
        
        GlobalVariables.LOGGER.info("User '{}' created successfully.".format(reqData['username']))
        return {"message":"User '{}' created successfully.".format(reqData['username'])}, 201


class User(Resource):
    
    @classmethod
    def get(cls,userID):
        user = UserModel.findById(userID)
        if user:
            GlobalVariables.LOGGER.info("User details : {}".format(user.json()))
            return user.json(), 200
        GlobalVariables.LOGGER.info("User not found : {}".format(userID))
        return {"message":"User not found"}, 404

    @classmethod
    def delete(clsif,userID):
        user = UserModel.findById(userID)
        if user:
            GlobalVariables.LOGGER.info("User details : {}".format(user.json()))
            try:
                user.deleteFromDB()
            except Exception as e:
                GlobalVariables.LOGGER.info("An error occured while deleting the user : {}".format(e))
                return {"message":"An error occured while deleting the user."}, 500
            GlobalVariables.LOGGER.info("User '{}' has been deleted successfully.".format(userID))
            return {"message":"User '{}' has been deleted successfully.".format(userID)}, 200
        GlobalVariables.LOGGER.info("User '{}' not found.".format(userID))
        return {"message":"User '{}' not found.".format(userID)}, 404        


class UserLogin(Resource):
    
    @classmethod
    def post(cls):
        reqData = CommonConfigs().parseReqBody() 
        user = UserModel.findByUsername(reqData['username'])
        if user and user.password == reqData['password']:
            accessToken = create_access_token(identity=user.id,fresh=True)
            refreshToken = create_refresh_token(user.id)
            return {
                "access_token":accessToken,
                "refresh_token":refreshToken
            }, 201
        return {"message":"Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']      # jti is "JWT ID" , a unique identifier for jwt
        GlobalVariables.BLACK_LIST.add(jti)
        return {"message":"Successfully logged out..."}, 201


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        currentUser = get_jwt_identity()
        accessToken = create_access_token(currentUser,fresh=False)
        return {"access_token":accessToken}, 201