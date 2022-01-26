#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-

class Status(object):
    SUCCESS = 'success'
    FAILURE = 'failure'


class Method(object):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class ValidationTypes(object):
    INVALID_JSON_SCHEMA = 'INVALID_JSON_SCHEMA'
    VALIDATION = 'VALIDATION'
    CLIENT_ERROR = 'CLIENT_ERROR'
    INTERNAL_SERVER_ERROR = 'INTERNAL_SERVER_ERROR'
    CONFLICT = "CONFLICT"
    URL_ERROR = 'URL_NOT_FOUND'


class AudioType(object):
    SONG = "song"
    PODCAST = "podcast"
    AUDIO_BOOK = "audiobook"
