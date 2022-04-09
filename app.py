from flask import Flask;
from flask_cors import CORS
from flask import jsonify
from flask import request
import logging

####
# `pip install flask` and `pip install flask_cors` before running this server.
# Run `python app.py` to start the server. Don't use `flask run`!
####

app = Flask(__name__)

# logging.basicConfig(level=logging.DEBUG)

CORS(app)

data = ""

@app.route('/', methods = ['GET', 'POST'])
def calculatePies():
  if request.method == 'POST':
    age = request.json['age']
    risk = request.json['risk']
    sector = request.json['sector']
    userId = request.json['userId']
    app.logger.error("Age {age} Risk {risk} Sector {sector} UserId {userId}".format(age=age, risk=risk, sector=sector, userId=userId))

    # TODO: Pie Calculation Algorithm goes here!

    return jsonify({"message": "POST Reply Message", "age":age, "risk":risk,"sector": sector,"userId": userId})
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")


app.run(debug=True)