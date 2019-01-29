import json
import os
class Config:
    config_path = os.path.dirname(os.path.realpath(__file__))
    config = json.load(open(config_path + '/.config.json'))
