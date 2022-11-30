import pymongo as pymongo
from flask import Flask, request, jsonify
from pymongo.server_api import ServerApi
from Schemas import SoundSchema
from dotenv import load_dotenv
import datetime as dt
import os

load_dotenv()

MONGODB_LINK = os.environ.get("MONGODB_LINK")
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASS = os.environ.get("MONGODB_PASS")


app = Flask(__name__)
app.config['DEBUG'] = True

# connecting to mongodb
client = pymongo.MongoClient(
    f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_LINK}/?retryWrites=true&w=majority",
    server_api=ServerApi('1'))

# name of database
db = client.SecurityApp

if 'Motion' not in db.list_collection_names():
    db.create_collection("Motion",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})
if 'Sound' not in db.list_collection_names():
    db.create_collection("Sound",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})

# Testing
db.Sound.insert_one(
    {"timestamp": dt.datetime.today().replace(microsecond=0), "sensorId": "test", "value": {"$numberInt": "1010"}}
)
print(list(db.Motion.find()))


@app.route("/api/sound", methods=["POST"])
def createSound():
    body = request.json
    error = SoundSchema().validate(data=body)

    if error:
        return {"message": "Invalid body"}, 401

    if body["soundAvg"] >= 650:
        body["detected"] = True
    else:
        body["detected"] = False

    return jsonify(body), 200


app.run()
