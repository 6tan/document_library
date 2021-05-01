#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import inspect
import json
import logging
from abc import abstractmethod
from json import JSONDecodeError

from fastjsonschema import JsonSchemaException
from flask.views import MethodView
from flask import Flask
from flask import request, jsonify

from utils.utils_constant import ValidationTypes, Status
from utils.utils_postgres_connector import connector

logger = logging.getLogger("search_logger")


class ApiBase(MethodView):
    def __init__(self):
        self._request = None
        self._json_error_information_dict = dict()
        self.__json_schema = []
        self.pg_connector = connector

    @property
    def request_data(self):
        return self._request

    @property
    @abstractmethod
    def json_schema(self):
        return self.__json_schema

    @property
    @abstractmethod
    def validator(self):
        return self.__validator

    def validate_schema(self, *args, **kwargs):
        if inspect.ismethod(self.request_data):
            raise Exception(f"Should define '{self.json_schema.__name__}' as property")
        try:
            self.validator(self.request_data)
            return Status.SUCCESS, None, None
        except JsonSchemaException as error:
            error_message = f'Schema Validation Failed for {self.json_schema.get("title", "Unknown")}'
            error_info_list = []
            error_dict = {
                'message': error.message,
            }
            try:
                error_dict.update({'instance': error.value})
            except AttributeError:
                error_dict.update({'instance': None})

            error_info_list.append(error_dict)
            self._json_error_information_dict = {'error': error_info_list}
            validation_type = ValidationTypes.INVALID_JSON_SCHEMA
            return Status.FAILURE, validation_type, error_message

    def validate_parameters(self, *args, **kwargs):
        """
            This function can be overridden by the inherited class to validate API specific parameters

            :rtype (str, srt|None, str)
        """
        return Status.SUCCESS, None, None

    def post(self) -> Flask.make_response:

        try:
            self._request = json.loads(request.data)
        except JSONDecodeError as e:
            message = "The server will not process the request due to something that is perceived to be an error."
            logger.error(message, extra={"error": e})
            return ApiResponse.get(_type=ValidationTypes.CLIENT_ERROR, message=message,
                                   error_code=400, status_code=400)

        status, _type, msg = self.validate_schema()
        if status == Status.FAILURE and _type == ValidationTypes.INVALID_JSON_SCHEMA:
            return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400,
                                   schema_error_information=self._json_error_information_dict)

        try:
            data = self.process_post()
        except Exception as e:
            message = "Has encountered a situation it doesn't know how to handle."
            logger.error(message, extra={"error": e}, exc_info=True)
            return ApiResponse.get(_type=ValidationTypes.INTERNAL_SERVER_ERROR, message=message,
                                   error_code=500, status_code=500)

        response_message = ApiResponse.get(response_data=data)
        return response_message

    @abstractmethod
    def process_post(self):
        raise NotImplementedError()

    def get(self, *args, **kwargs) -> Flask.make_response:

        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.URL_ERROR:
                return ApiResponse.get(_type=_type, message=msg, error_code=404, status_code=404)

            data = self.process_get(**request.args, **kwargs)
        except Exception as e:
            return ApiResponse.get(_type="Exception handler", message=f'{e}', status_code=500)

        response_message = ApiResponse.get(response_data=data)
        return response_message

    @abstractmethod
    def process_get(self, *args, **kwargs):
        raise NotImplementedError()

    def put(self, *args, **kwargs) -> Flask.make_response:

        try:
            status, _type, msg = self.validate_parameters(**request.args, **kwargs)
            if status == Status.FAILURE and _type == ValidationTypes.URL_ERROR:
                return ApiResponse.get(_type=_type, message=msg, error_code=404, status_code=404)

            self._request = json.loads(request.data)

        except JSONDecodeError as e:
            message = "The server will not process the request due to something that is perceived to be an error."
            logger.error(message, extra={"error": e})
            return ApiResponse.get(_type=ValidationTypes.CLIENT_ERROR, message=message,
                                   error_code=400, status_code=400)

        status, _type, msg = self.validate_schema(*args, **kwargs)
        if status == Status.FAILURE and _type == ValidationTypes.INVALID_JSON_SCHEMA:
            return ApiResponse.get(_type=_type, message=msg, error_code=400, status_code=400,
                                   schema_error_information=self._json_error_information_dict)

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
