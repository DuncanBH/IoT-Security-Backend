from flask import Flask, request, jsonify
from Schemas import SoundSchema

app = Flask(__name__)


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
