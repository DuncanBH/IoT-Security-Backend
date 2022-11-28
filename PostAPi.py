from flask import Flask, request

app = Flask(__name__)


@app.route("/api/sound", methods=["POST"])
def createSound():
    body = request.json




app.run()
