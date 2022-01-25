#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import logging
from abc import abstractmethod
from flask.views import MethodView
from flask import Flask
from flask import request, jsonify, send_file
from utils.utils_constant import ValidationTypes, Status

logger = logging.getLogger("logger")


class ApiBase(MethodView):
    def __init__(self):
        self._request = None

    @property
    def request_data(self):
        return self._request

    def validate_parameters(self, *args, **kwargs):
        """
            This function can be overridden by the inherited class to validate API specific parameters

            :rtype (str, srt|None, str)
        """
        return Status.SUCCESS, None, None

    def post(self) -> Flask.make_response:

        self._request = request

        try:
            data, status_code, message, _type = self.process_post()
        except Exception as e:
            message = "Has encountered a situation it doesn't know how to handle."
            logger.error(message, extra={"error": e}, exc_info=True)
            return ApiResponse.get(_type=ValidationTypes.INTERNAL_SERVER_ERROR, message=message,
                                   error_code=500, status_code=500)

        response_message = ApiResponse.get(response_data=data, status_code=status_code, _type=_type,
                                           message=message)
        return response_message

    @abstractmethod
    def process_post(self):
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Flask.make_response:

        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.URL_ERROR:
                return ApiResponse.get(_type=_type, message=msg, error_code=404, status_code=404)

            file_path = self.process_get(**request.args, **kwargs)
        except Exception as e:
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)

        return send_file(file_path)

    @abstractmethod
    def process_get(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs) -> Flask.make_response:

        self._request = request

        try:
            data = self.process_put(*args, **kwargs)
        except Exception as e:
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)

        response_message = ApiResponse.get(response_data=data)
        return response_message

    @abstractmethod
    def process_put(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs) -> Flask.make_response:
        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.URL_ERROR:
                return ApiResponse.get(_type=_type, message=msg, error_code=404, status_code=404)

            data = self.process_delete(**request.args, **kwargs)
        except Exception as e:
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)

        response_message = ApiResponse.get(response_data=data)
        return response_message

    @abstractmethod
    def process_delete(self, *args, **kwargs):
        raise NotImplementedError()


class ApiResponse(object):
    SUCCESS_STATUS_CODE: int = 200
    NO_CONTENT_STATUS_CODE: int = 204

    @classmethod
    def get(cls, _type=None, message=None, error_code=None, response_data=None,
            status_code=200, **kwargs) -> Flask.make_response:

        if status_code == ApiResponse.SUCCESS_STATUS_CODE:
            data = response_data
            if not response_data:
                status_code = ApiResponse.NO_CONTENT_STATUS_CODE
        else:
            data = {"type": _type, "message": message, "code": error_code}
        if kwargs:
            data['additional_data'] = kwargs
        content = jsonify(data)
        response = Flask(__name__).make_response((content, status_code))

        return response
