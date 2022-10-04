import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from app.globalVariables import GlobalVariables

class Item(Resource):

    def parseReqBody(self):
        reqParser = reqparse.RequestParser()
        reqParser.add_argument('price',
        type=float,
        required=True,
        help="This field can not be left blank!")

        return reqParser.parse_args()
    
    def select(self,itemName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        result = cursor.execute(GlobalVariables.SELECT_ITEM_BY_NAME,(itemName,))
        row = result.fetchone()
        connection.close()
        return row
    
    def insert(self,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(GlobalVariables.INSERT_INTO_ITEMS,(item['name'],item['price']))
        connection.commit()
        connection.close()
    
    def update(self,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(GlobalVariables.UPDATE_IETM,(item['price'],item['name']))
        connection.commit()
        connection.close()

    def delete(self,itemName):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        cursor.execute(GlobalVariables.DELETE_ITEM,(itemName,))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self,itemName):
        row = self.select(itemName)
        if row:
            return {'item':{'name':row[0],'price':row[1]}}, 200
        GlobalVariables.LOGGER.info("Item not found.")
        return {'message':'Item not found.'}, 404

    @jwt_required()
    def post(self,itemName):
        try:
            row = self.select(itemName)
        except:
            GlobalVariables.LOGGER.info("An error occured while fetching the item.")
            return {"message":"An error occured while fetching the item."}, 500
        if row:
            GlobalVariables.LOGGER.info("Item '{}' already exists".format(itemName))
            return {'message':"Item '{}' already exists".format(itemName)}, 400
        reqData = self.parseReqBody()
        GlobalVariables.LOGGER.info("POST method request body : {}".format(reqData))
        item = {'name':itemName,'price':reqData['price']}
        try:
            self.insert(item)
        except:
            GlobalVariables.LOGGER.info("An error occured while inserting the item.")
            return {"message":"An error occured while inserting the item."}, 500
        return item, 201
        
    @jwt_required()
    def delete(self,itemName):
        try:
            row = self.select(itemName)
        except:
            GlobalVariables.LOGGER.info("An error occured while fetching the item.")
            return {"message":"An error occured while fetching the item."}, 500
        if row:
            try:
                self.delete(itemName)
            except:
                GlobalVariables.LOGGER.info("An error occured while deleting the item.")
                return {"message":"An error occured while deleting the item."}, 500
            GlobalVariables.LOGGER.info("Item '{}' deleted successfully".format(itemName))
            return {'message':"Item '{}' deleted successfully".format(itemName)}, 200
        GlobalVariables.LOGGER.info("Item not found.")
        return {'message':'Item not found.'}, 404

    @jwt_required()
    def put(self,itemName):
        reqData = self.parseReqBody()
        GlobalVariables.LOGGER.info("PUT method request body : {}".format(reqData))
        try:
            row = self.select(itemName)
        except:
            GlobalVariables.LOGGER.info("An error occured while fetching the item.")
            return {"message":"An error occured while fetching the item."}, 500
        item = {'name':itemName,'price':reqData['price']}
        if row:
            try:
                self.update(item)
            except:
                GlobalVariables.LOGGER.info("An error occured while updating the item.")
                return {"message":"An error occured while updating the item."}, 500
            return item, 201
        try:
            self.insert(item)
        except:
            GlobalVariables.LOGGER.info("An error occured while inserting the item.")
            return {"message":"An error occured while inserting the item."}, 500
        return item, 201

class ItemList(Resource):
    @jwt_required()
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        result = cursor.execute(GlobalVariables.SELECT_ITEMS)
        rows = result.fetchall()
        connection.close()
        responsePayload = []
        if rows:
            for row in rows:
                dataDict = {}
                dataDict['name'] = row[0]
                dataDict['price'] = row[1]
                responsePayload.append(dataDict)
                GlobalVariables.LOGGER.info("items : {}".format(responsePayload))
            return {'items':responsePayload}, 200
        GlobalVariables.LOGGER.info("Items not found")
        return {'message':'Items not found'}, 400