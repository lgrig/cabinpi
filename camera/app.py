from flask import Flask
import os
os.environ['FLASK_APP'] = 'camera.py'

app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True)
