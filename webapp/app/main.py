#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import os
import sys
from inspect import getframeinfo, currentframe
from pathlib import Path

filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent
ROOT_PATH = Path(current_module_path).parents[1].as_posix()
module_path = [
    f'{ROOT_PATH}/webapp/'
]

for index, path in enumerate(module_path):
    sys.path.insert(index, os.path.realpath(os.path.join(os.path.dirname(__file__), path)))

from app import url, flask_app
from db.models import  db

db.create_all()  # loading database


def app_run():
    debug = False
    flask_app.run('0.0.0.0', 9876, debug)


url.register_urls(flask_app)

if __name__ == '__main__':
    app_run()
