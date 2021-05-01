#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import os
import sys
from inspect import getframeinfo, currentframe
from pathlib import Path

from flask import Flask

filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent
ROOT_PATH = Path(current_module_path).parents[1].as_posix()
module_path = [
    f'{ROOT_PATH}/webapp/'
]
print(module_path)
for index, path in enumerate(module_path):
    sys.path.insert(index, os.path.realpath(os.path.join(os.path.dirname(__file__), path)))

from app.url import register_urls

flask_app = Flask(__name__)
flask_app.config.from_object(__name__)


def app_run():
    debug = False
    flask_app.run('0.0.0.0', 9876, debug)


register_urls(flask_app)

if __name__ == '__main__':
    app_run()
