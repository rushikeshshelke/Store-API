from flask_restful import Resource, reqparse
from models.store import StoreModel
from flask_jwt_extended import jwt_required, get_jwt
from commonLibs.globalVariables import GlobalVariables

class Store(Resource):

    def get(self,storeName):
        store = StoreModel.select(storeName)
        if store:
            GlobalVariables.LOGGER.info("Store : {}".format(store.json()))
            return store.json(), 200
        GlobalVariables.LOGGER.info("Store not found")
        return {"message":"Store not found"}, 404
    
    @jwt_required(fresh=True)
    def post(self,storeName):
        store = StoreModel.select(storeName)
        if store:
            GlobalVariables.LOGGER.info("Store '{}' already exists".format(storeName))
            return {"message":"Store '{}' already exists".format(storeName)}, 400
        store = StoreModel(storeName)
        try:
            store.saveToDB()
        except Exception as e:
            GlobalVariables.LOGGER.info("An error occured while creating the store : {}".format(e))
            return {"message":"An error occured while creating the store."}, 500
        return store.json(), 201

    @jwt_required(fresh=True)
    def delete(self,storeName):
        claim = get_jwt()
        if not claim['is_admin']:
            return {"message":"Admin privilege required"}, 401
        store = StoreModel.select(storeName)
        if store:
            try:
                store.deleteFromDB()
            except Exception as e:
                GlobalVariables.LOGGER.info("An error occured while deleting the store : {}".format(e))
                return {"message":"An error occured while deleting the store ."}, 500
            GlobalVariables.LOGGER.info("Store '{}' has been deleted successfully.".format(storeName))
            return {"message":"Store '{}' has been deleted successfully.".format(storeName)}, 200
        GlobalVariables.LOGGER.info("Store '{}' not found.".format(storeName))
        return {"message":"Store '{}' not found.".format(storeName)}, 404        


class StoreList(Resource):
    
    def get(self):
        rows = StoreModel.findAll()
        responsePayload = []
        if rows:
            for row in rows:
                responsePayload.append(row.json())
                GlobalVariables.LOGGER.info("stores : {}".format(responsePayload))
            return {'stores':responsePayload}, 200
        GlobalVariables.LOGGER.info("Stores not found")
        return {'message':'Stores not found'}, 400