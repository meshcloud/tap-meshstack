from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/api/meshobjects/<path:path>')
def send_report(path):
    return send_from_directory('meshobjects', path + ".json")


if __name__ == '__main__':
    app.run(host='localhost', port=8000)