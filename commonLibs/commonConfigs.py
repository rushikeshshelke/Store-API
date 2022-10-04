import os
import json
from dotenv import load_dotenv
from flask_restful import reqparse

class CommonConfigs:

    def createDir(self,path):
        if os.path.isdir(path) == False:
            os.makedirs(path)
    
    def readJson(self,filename):
        with open(filename,'r') as f:
            data = json.load(f)
        return data
    
    def getEnvData(self):
        load_dotenv()
        secretKey = os.environ.get('SECRET_KEY')
        return secretKey

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