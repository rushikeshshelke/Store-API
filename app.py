from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from app.initialiseLogging import InitialiseLogging
from app.globalVariables import GlobalVariables
from app.security import authenticate,identity
from app.user import UserRegister
from app.commonConfigs import CommonConfigs
from app.item import Item, ItemList

app = Flask(__name__)
app.secret_key = CommonConfigs().getEnvData()
api = Api(app)

jwt = JWT(app,authenticate,identity)  #/auth

InitialiseLogging().setupLogging()
GlobalVariables.LOGGER.info("App Started...")
GlobalVariables.LOGGER.info("Logging initialised...")



api.add_resource(Item,'/item/<string:itemName>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')

if __name__ == "__main__":
    app.run(port=5000,debug=True)