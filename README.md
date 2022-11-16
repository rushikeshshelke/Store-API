# Store-API

## Install dependancies
```
pip3 install -r requirements.txt
```

## Description

This project is implemented using Flask-Restful, and it is REST API for store.

### Usage

Following are the resources offered by Store-API

```
    1. Resource - Store
        - get /stores : Lists down all available stores
        - get /store/storeName : List down specific store by name
        - post /store/storeName : Creates store by name if not exists
        - delete /store/storeName : Delete store by name

    2. Resource - Item
        - get /items : Lists down all available items
        - get /item/itemName : List down specific item by name
        - post /item/itemName : Creates item by name if not exists
        - put /item/itemName : Creates/Updates item by name
        - delete /item/itemName : Delete item by name
    
    3. Resource - User
        - get /user/userID : List down user by userID
        - delete /user/userID : Delete user by userID
    
    4. Resource - UserRegister
        - post /register : Registers user by username and password
    
    5. Resource - UserLogin
        - post /auth : Authenticates user by username and password
    
    6. Resource - UserLogout
        - post /logout : Helps to user logged out.
    
    7. Resource - TokenRefresh
        - post /refresh : Creates access_token from refresh_token
```
```
API DOC : https://store-item-rest-api-v1.herokuapp.com/api/docs/
```