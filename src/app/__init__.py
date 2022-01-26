#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from flask import Flask
flask_app = Flask(__name__)
flask_app.config.from_object(__name__)
