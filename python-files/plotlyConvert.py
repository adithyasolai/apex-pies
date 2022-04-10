import plotly.express as px
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from prettyprinter import pprint
import pandas as pd
import plotly
from bs4 import BeautifulSoup


#Firebase setup
# Fetch the service account key JSON file contents
cred = credentials.Certificate('./apex-pies.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://apex-pies-default-rtdb.firebaseio.com'
})

ref2 = db.reference().child("DummyUser223").child("pie")


df = ref2.get()
pprint(df)
tickers = {}
for dictionary in df:
    tickers[(dictionary['Ticker'])] = "5.0%"

tickers_list = list(tickers.keys())

vals = [0.0] * len(tickers_list)
for i in range(len(tickers_list)):
    vals[i] = 100/len(tickers_list)

print(tickers_list)

df = pd.DataFrame({"Ticker": tickers_list, "Percentages": vals})
print(df)

fig = px.pie(df,values="Percentages", names="Ticker")
fig.show()      
plotly.offline.plot(fig, filename='file.html')

soup = BeautifulSoup('../file.html')
htmlString = soup.get_text()
print(htmlString)
