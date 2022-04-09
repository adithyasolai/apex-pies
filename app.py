from flask import Flask;
from flask_cors import CORS
from flask import jsonify
from flask import request

import pandas as pd
import numpy as pd
import logging

####
# `pip install flask` and `pip install flask_cors` before running this server.
# Run `python app.py` to start the server. Don't use `flask run`!
####

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

CORS(app)

data = ""

@app.route('/', methods = ['GET', 'POST'])
def calculatePies():

  if request.method == 'POST':
    age = request.json['age']
    risk = request.json['risk']
    sector = request.json['sector']
    app.logger.info("Age {age} Risk {risk} Sector {sector}".format(age=age, risk=risk, sector=sector))

    # TODO: Pie Calculation Algorithm goes here!

    return jsonify({"message": "POST Reply Message"})
  elif request.method == 'GET':
    # Don't worry about this GET case. It's only here if we need it in the future.

    app.logger.info("GET message received")
    return jsonify("GET Reply Message")

if __name__ == '__main__':
  app.run(debug=True)