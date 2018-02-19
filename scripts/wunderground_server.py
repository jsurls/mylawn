import os
import json
from flask import Flask

app = Flask(__name__)


@app.route("/weatherstation/WXDailyHistory.asp")
def get_history():
    with open("responses/sample_wunderground_history_response.html") as data_file:
        return data_file.read()


@app.route("/api/<apikey>/geolookup/q/<zipcode>.json")
def geolookup_zip(apikey, zipcode):
    with open("responses/sample_wunderground_zip_response.json") as data_file:
        data = json.load(data_file)
        return json.dumps(data)


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
