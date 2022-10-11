import os

from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from commonLibs.initialiseLogging import InitialiseLogging
from commonLibs.globalVariables import GlobalVariables
from resources.userRegister import UserRegister, User, UserLogin, UserLogout, TokenRefresh
from commonLibs.commonConfigs import CommonConfigs
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
plugin = os.environ.get("DATABASE_URL","sqlite:///data.db")
if plugin.startswith('postgres://'):
    plugin = plugin.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = plugin
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disables flask sqlalchemy tracker not underlying sqlalchemy tracker
app.config['PROPAGATE_EXCEPTIONS'] = True #Flask jwt will return proper error response
app.config['JWT_BLOCKLIST_TOKEN_CHECKS'] = ["access","refresh"]
secretKey, jwtAlgorithm = CommonConfigs().getEnvData()
app.secret_key = secretKey
app.config["JWT_SECRET_KEY"] = secretKey
app.config["JWT_ALGORITHM"] = jwtAlgorithm
api = Api(app)

# @app.before_first_request
# def createTables():
#     db.create_all()

jwt = JWTManager(app)

@jwt.additional_claims_loader
def addClaimsToJWT(identity):
    if identity == GlobalVariables.ADMIN_USER:
        return {"is_admin":True}
    return {"is_admin":False}

@jwt.token_in_blocklist_loader
def checkIfTokenInBlackList(jwt_header,jwt_payload):
    return jwt_payload['jti'] in GlobalVariables.BLACK_LIST

@jwt.expired_token_loader
def expiredTokenCallback(jwt_headers,jwt_payload):
    return {
                "description": "The token has expired.",
                "error": "token_expired"
            }, 401

@jwt.invalid_token_loader
def invalidTokenLoader(jwt_headers,jwt_payload):
    return {
                "description": "Signature verification failed.",
                "error": "invalid_token"
    }, 401

@jwt.unauthorized_loader
def missingTokenCallback():
    return {
                "description": "Request does not contain valid token.",
                "error": "authorization_required"
    }, 401

@jwt.needs_fresh_token_loader
def tokenNotRefreshCallback(jwt_headers,jwt_payload):
    return {
                "description": "The token not fresh.",
                "error": "fresh_token_required"
    }, 401

@jwt.revoked_token_loader
def revokedTokenCallback(jwt_headers,jwt_payload):
    return {
                'description': "The token has been revoked.",
                "error": "token_revoked"
    }
    
InitialiseLogging().setupLogging()
GlobalVariables.LOGGER.info("App Started...")
GlobalVariables.LOGGER.info("Logging initialised...")

api.add_resource(Item,'/item/<string:itemName>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:storeName>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:userID>')
api.add_resource(UserLogin,'/auth')
api.add_resource(TokenRefresh,'/refresh')
api.add_resource(UserLogout,'/logout')

if __name__ == "__main__":
    # from commonLibs.database import db
    # db.init_app(app)
    port = os.environ.get('PORT',5000)
    app.run(host="0.0.0.0",port=port,debug=True)