from flask import Flask, render_template, url_for
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

data = """Time,Temperature
2019-05-23 13:22:57.266773,19.5
2019-05-23 13:23:57.266773,20.1
2019-05-23 13:24:57.266773,18.4
2019-05-23 13:25:57.266773,19.2
2019-05-23 13:26:57.266773,15.6
2019-05-23 13:27:57.266773,21.3
2019-05-23 13:28:57.266773,21.5
2019-05-23 13:29:57.266773,21.4
2019-05-23 13:30:57.266773,21.2
2019-05-23 13:31:57.266773,20.0
2019-05-23 13:32:57.266773,19.8
"""


@app.route("/data")
def getData():
    return data

if __name__ == "__main__":
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

    # TODO: Before running the app, generate a thread to manage the data

    app.run(host="0.0.0.0", port=8082, debug=True)
