import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

cred = credentials.Certificate('../apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

def createUser(userEmail, userPassword):
    user = auth.create_user(
        email= userEmail,
        password = userPassword
        )
    print('Sucessfully created new user: {0}'.format(user.uid))

createUser("winner@bloomberg.com", "bloomberg")
