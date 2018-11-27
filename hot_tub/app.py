from flask import Flask, jsonify, abort, make_response, request, render_template
from lib.

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/greenhouse/api/v1.0/tasks', methods=['POST'])
def create_task():
    request_task = request.json['task']
    tasks = {
        'random_number': RandomNumber().measure,
 #       'take_photo': Camera().take_photo,
        'soil_sensor': SoilSensor().measure,
        'sun_sensor': SunSensor().measure,
        'temp_humidity_sensor': TempHumiditySensor().measure,
        'toggle_valve': ToggleValve().toggle()
    }

    if not request.json or request_task not in tasks.keys():
        abort(400)

    result = tasks[request_task]()
    return jsonify({'task': result}), 201
if __name__ == '__main__':
    app.run(debug=True)
