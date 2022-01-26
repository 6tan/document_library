#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import logging
from abc import abstractmethod
from flask.views import MethodView
from flask import Flask
from flask import request, jsonify, send_file
from utils.utils_constant import ValidationTypes, Status
import traceback

logger = logging.getLogger("logger")


class ApiBase(MethodView):
    def __init__(self):
        self._request = None
        self.is_file = False
        self._request_headers = None

    @property
    def request_data(self):
        return self._request
    
    @property
    def request_headers(self):
        # using for token validation
        return self._request_headers

    def validate_parameters(self, *args, **kwargs):
        """
            This function can be overridden by the inherited class to validate API specific parameters

            :rtype (str, srt|None, str)
        """
        return Status.SUCCESS, None, None
    
    def validate_request(self):
        """
            This function can be overridden by the inherited class to validate request json
            :rtype (str, srt|None, str)
        """
        return Status.SUCCESS, None, None

    def post(self) -> Flask.make_response:

        self._request = request
        self._request_headers = request.headers

        try:
            status, _type, msg = self.validate_request()
            if status == Status.FAILURE and _type == ValidationTypes.VALIDATION:
                return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400)

            data = self.process_post()
        except Exception as e:
            message = "Has encountered a situation it doesn't know how to handle."
            logger.error(message, extra={"error": e}, exc_info=True)
            return ApiResponse.get(_type=ValidationTypes.INTERNAL_SERVER_ERROR, message=message,
                                   error_code=500, status_code=500)

        return ApiResponse.get(response_data=data)

    @abstractmethod
    def process_post(self):
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Flask.make_response:

        self._request_headers = request.headers
        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.VALIDATION:
                return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400)

            response, message, status_code, _type = self.process_get(**request.args, **kwargs)
        except Exception as e:
            print(traceback.format_exc())
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)
        if self.is_file:
            return send_file(response)
        else:
            return ApiResponse.get(response_data=response, status_code=status_code, _type=_type,
                                           message=message)

    @abstractmethod
    def process_get(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs) -> Flask.make_response:

        self._request = request
        self._request_headers = request.headers

        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.VALIDATION:
                return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400)

            response, message, status_code, _type = self.process_put(*args, **kwargs)
        except Exception as e:
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)

        return ApiResponse.get(response_data=response, status_code=status_code, _type=_type,
                                           message=message)

    @abstractmethod
    def process_put(self, *args, **kwargs):
        raise NotImplementedError()

    def delete(self, *args, **kwargs) -> Flask.make_response:
        self._request_headers = request.headers
        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.VALIDATION:
                return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400)

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
