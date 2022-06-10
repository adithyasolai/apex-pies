import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

'''
Some utility functions that programmatically impact the Firebase RTDB
'''

#Firebase setup
# Fetch the service account key JSON file contents
# Service accounts will always bypass any read/write rules
cred = credentials.Certificate('../../apex-pies.json')

# Initialize the app with a service account, granting admin privileges
app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

def deleteAllUsers():
  "Deleting all user data from Authentication..."
  for authUser in auth.list_users().users:
    auth.delete_user(authUser.uid)

  "Deleting all user data from Realtime Database..."
  userRTDBData = db.reference().child("users")
  if userRTDBData is not None:
    for userId in userRTDBData.get():
      childRef = userRTDBData.child(userId)
      childRef.delete()

def printAllUserIds():
  "Printing all userIds..."
  ref = db.reference()
  for userId in ref.get():
    print(userId)

# printAllUserIds()
deleteAllUsers()