import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from commonLibs.initialiseLogging import InitialiseLogging
from commonLibs.globalVariables import GlobalVariables
from commonLibs.security import authenticate,identity
from resources.userRegister import UserRegister
from commonLibs.commonConfigs import CommonConfigs
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
plugin = os.environ.get("DATABASE_URL","sqlite:///data.db")
if plugin.startswith('postgres://'):
    plugin = plugin.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = plugin
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # disables flask sqlalchemy tracker not underlying sqlalchemy tracker
app.secret_key = CommonConfigs().getEnvData()
api = Api(app)

jwt = JWT(app,authenticate,identity)  #/auth

InitialiseLogging().setupLogging()
GlobalVariables.LOGGER.info("App Started...")
GlobalVariables.LOGGER.info("Logging initialised...")

api.add_resource(Item,'/item/<string:itemName>')
api.add_resource(ItemList,'/items')
api.add_resource(UserRegister,'/register')
api.add_resource(Store,'/store/<string:storeName>')
api.add_resource(StoreList,'/stores')

if __name__ == "__main__":
    from commonLibs.database import db
    db.init_app(app)
    app.run(port=5000,debug=True)