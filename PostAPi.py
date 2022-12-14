import pymongo as pymongo
from flask import Flask, request, jsonify
from pymongo.server_api import ServerApi

from Pipelines import sound_for_period, average_for_period, count_for_period, motion_for_period
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
client = pymongo.MongoClient(f"mongodb+srv://{MONGODB_USER}:{MONGODB_PASS}@{MONGODB_LINK}/?retryWrites=true&w=majority",
                             server_api=ServerApi('1'))

# name of database
db = client.SecurityApp

# Collections
if 'Motion' not in db.list_collection_names():
    db.create_collection("Motion",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})
if 'Sound' not in db.list_collection_names():
    db.create_collection("Sound",
                         timeseries={'timeField': 'timestamp', 'metaField': 'sensorId', 'granularity': 'minutes'})


# DB populator
# import random
# for x in range(0, 20):
#     motionSeenCount = random.randint(0, 60)
#     motionSeen = motionSeenCount >= 40
#     db.Motion.insert_one(
#         {"timestamp": dt.datetime.today().replace(microsecond=0), "sensorId": "test",
#          "value": motionSeenCount, "motionSeen": motionSeen}
#     )

@app.route("/api/sound", methods=["POST"])
def createSound():
    body = request.json
    error = SoundSchema().validate(data=body)

    if error:
        return {"message": "Invalid body"}, 401

    if body["value"] >= 650:
        body["soundHeard"] = True
    else:
        body["soundHeard"] = False

    body["timestamp"] = dt.datetime.today().replace(microsecond=0)

    db.Sound.insert_one(body)

    body["_id"] = str(body["_id"])

    return jsonify(body), 200


@app.route("/api/sound")
def getDailySoundAverage():
    average = request.args.get("average", False)
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    day = request.args.get("day", None)

    if average:
        data = db.Sound.aggregate(average_for_period(year, month, day))
    else:
        data = db.Sound.aggregate(sound_for_period(year, month, day))

    return jsonify(list(data))


@app.route("/api/motion", methods=['POST'])
def crateMotion():
    body = request.json
    error = SoundSchema().validate(data=body)

    if error:
        return {"message": "Invalid body"}, 401

    if body["value"] >= 40:
        body["motionSeen"] = True
    else:
        body["motionSeen"] = False

    body["timestamp"] = dt.datetime.today().replace(microsecond=0)

    db.Motion.insert_one(body)

    body["_id"] = str(body["_id"])

    return jsonify(body), 200


@app.route("/api/motion")
def getDailyMotionCount():
    count = request.args.get("count", False)
    year = request.args.get("year", None)
    month = request.args.get("month", None)
    day = request.args.get("day", None)

    if count:
        data = db.Motion.aggregate(count_for_period(year, month, day))
    else:
        data = db.Motion.aggregate(motion_for_period(year, month, day))

    return jsonify(list(data))


app.run(debug=True, port=5000, host="0.0.0.0")
