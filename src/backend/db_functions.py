import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

#Firebase setup
# Fetch the service account key JSON file contents
cred = credentials.Certificate('../../apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

def deleteAllUsers():
  "Deleting all userIds..."
  ref = db.reference()

  for userId in ref.get():
    childRef = db.reference().child(userId)
    childRef.delete()

def printAllUserIds():
  "Printing all userIds..."
  ref = db.reference()
  for userId in ref.get():
    print(userId)

# printAllUserIds()
deleteAllUsers()
