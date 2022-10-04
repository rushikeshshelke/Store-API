import os
import json
from dotenv import load_dotenv

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