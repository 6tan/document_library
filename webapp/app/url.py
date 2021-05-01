#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from utils.utils_constant import Method
from app.views import AudioGet, AudioCreate, AudioDelete, AudioUpdate


def register_url(app, view, url, endpoint, method):
    url = f"/api/v1/{url}"
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=[method.upper()])


def register_urls(app):
    register_url(app=app, view=AudioGet, endpoint='get_audio_type', url='audioFile/<audioFileType>', method=Method.GET)
    register_url(app=app, view=AudioGet, endpoint='get_audio_file', url='audioFile/<audioFileType>/<audioFileID>',
                 method=Method.GET)
    register_url(app=app, view=AudioCreate, endpoint='create_audio_file', url='audioFile/create',
                 method=Method.POST)
    register_url(app=app, view=AudioUpdate, endpoint='update_audio_file', url='audioFile/<audioFileType>/<audioFileID>',
                 method=Method.PUT)
    register_url(app=app, view=AudioDelete, endpoint='delete_audio_file', url='audioFile/<audioFileType>/<audioFileID>',
                 method=Method.DELETE)
