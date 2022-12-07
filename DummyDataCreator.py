import random
import requests

import time

starttime = time.time()

while True:
    print("tick")

    soundVal = random.randint(0, 2000)
    motionVal = random.randint(0, 60)

    response = requests.post("http://127.0.0.1:5000/api/sound",
                             headers={"Content-Type": "application/json"},
                             json={'value': soundVal,
                                   'sensorId': 'SoundTest'})

    print(response.text)

    response2 = requests.post("http://127.0.0.1:5000/api/motion",
                              headers={"Content-Type": "application/json"},
                              json={'value': motionVal,
                                    'sensorId': 'MotionTest'})

    print(response2.text)

    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
