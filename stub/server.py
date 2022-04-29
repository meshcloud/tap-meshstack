from flask import send_from_directory

@app.route('/reports/<path:path>')
def send_report(path):
    return send_from_directory('reports', path)