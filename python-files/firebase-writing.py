import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# default_app = firebase_admin.initialize_app()

# Fetch the service account key JSON file contents
cred = credentials.Certificate('/Users/siddharthcherukupalli/Downloads/apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules

# replace the child value with the userID
ref = db.reference().child("3")

# replace the value for pie to the dictionary created
ref.set({
    'pie': [{'ticker': "AAPL", 'percentage': 0.06, 'sector': "Tech"}, {'ticker': "GS", 'percentage': 0.06, 'sector': "Banking"}]
})
print(ref.get())

