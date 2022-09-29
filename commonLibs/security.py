from models.user import UserModel

def authenticate(username, password):
    # user = username_mapping.get(username,None)
    user = UserModel.findByUsername(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.findById(user_id)