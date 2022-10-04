from app.user import User

# users = [
#     {
#         'id':1,
#         'username':'rushi',
#         'password':'rush1234'
#     }
# ]

users = [
    User(1,'rushi','rush1234')
    ]
username_mapping = {
    u.username: u for u in users
}
userid_mapping = {
    u.id: u for u in users
}

# username_mapping = {
#     'rushi': {
#         'id':1,
#         'username':'rushi',
#         'password':'rush1234'
#     }
# }

# userid_mapping = {
#     1: {
#         'id':1,
#         'username':'rushi',
#         'password':'rush1234'
#     }
# }

def authenticate(username, password):
    # user = username_mapping.get(username,None)
    user = User.findByUsername(username)
    if user and user.password == password:
        return user

def identity(payload):
    user_id = payload['identity']
    return User.findById(user_id)