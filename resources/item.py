from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from commonLibs.globalVariables import GlobalVariables
from models.item import ItemModel

class Item(Resource):

    def parseReqBody(self):
        reqParser = reqparse.RequestParser()
        reqParser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank!")

        reqParser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id.")

        return reqParser.parse_args()

    @jwt_required()
    def get(self,itemName):
        try:
            item = ItemModel.select(itemName)
        except Exception as e:
            GlobalVariables.LOGGER.info("An error occured while fetching the item : {}".format(e))
            return {"message":"An error occured while fetching the item."}, 500
        if item:
            return item.json(), 200
        GlobalVariables.LOGGER.info("Item not found.")
        return {'message':'Item not found.'}, 404

    @jwt_required(fresh=True)
    def post(self,itemName):
        try:
            item = ItemModel.select(itemName)
        except Exception as e:
            GlobalVariables.LOGGER.info("An error occured while fetching the item : {}".format(e))
            return {"message":"An error occured while fetching the item."}, 500
        if item:
            GlobalVariables.LOGGER.info("Item '{}' already exists".format(itemName))
            return {'message':"Item '{}' already exists".format(itemName)}, 400
        reqData = self.parseReqBody()
        GlobalVariables.LOGGER.info("POST method request body : {}".format(reqData))
        item = ItemModel(itemName,reqData['price'],reqData['store_id'])
        try:
            item.saveToDB()
        except:
            GlobalVariables.LOGGER.info("An error occured while inserting the item.")
            return {"message":"An error occured while inserting the item."}, 500
        return item.json(), 201
        
    @jwt_required(fresh=True)
    def delete(self,itemName):
        claim = get_jwt()
        if not claim['is_admin']:
            return {"message":"Admin privilege required"}, 401

        try:
            item = ItemModel.select(itemName)
        except:
            GlobalVariables.LOGGER.info("An error occured while fetching the item.")
            return {"message":"An error occured while fetching the item."}, 500
        if item:
            try:
                item.deleteFromDB()
            except Exception as e:
                GlobalVariables.LOGGER.info("An error occured while deleting the item : {}".format(e))
                return {"message":"An error occured while deleting the item."}, 500
            GlobalVariables.LOGGER.info("Item '{}' deleted successfully".format(itemName))
            return {'message':"Item '{}' deleted successfully".format(itemName)}, 200
        GlobalVariables.LOGGER.info("Item not found.")
        return {'message':'Item not found.'}, 404

    @jwt_required(fresh=True)
    def put(self,itemName):
        reqData = self.parseReqBody()
        GlobalVariables.LOGGER.info("PUT method request body : {}".format(reqData))
        try:
            item = ItemModel.select(itemName)
        except Exception as e:
            GlobalVariables.LOGGER.info("An error occured while fetching the item : {}".format(e))
            return {"message":"An error occured while fetching the item."}, 500
        if item:
            item.price = reqData['price']
        else:
            item = ItemModel(itemName,reqData['price'],reqData['store_id'])
        try:
            item.saveToDB()
        except Exception as e:
            GlobalVariables.LOGGER.info("An error occured while inserting/updating the item : {}".format(e))
            return {"message":"An error occured while inserting/updating the item."}, 500
        return item.json(), 201


class ItemList(Resource):
    @jwt_required()
    def get(self):
        rows = ItemModel.findAll()
        responsePayload = []
        if rows:
            for row in rows:
                responsePayload.append(row.json())
                GlobalVariables.LOGGER.info("items : {}".format(responsePayload))
            return {'items':responsePayload}, 200
        GlobalVariables.LOGGER.info("Items not found")
        return {'message':'Items not found'}, 404