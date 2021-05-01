#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import inspect

from fastjsonschema import JsonSchemaException

from utils.utils_api_json_schema import CREATE_SCHEMA_DICT_VALIDATOR, CREATE_SCHEMA_DICT
from utils.utils_constant import AudioType, Status, ValidationTypes
from app.api_base import ApiBase


class AudioGet(ApiBase):

    def __init__(self):
        super().__init__()

    def validate_parameters(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        if audio_file_type in [AudioType.SONG, AudioType.PODCAST, AudioType.AUDIO_BOOK]:
            return Status.SUCCESS, None, None

        msg = "The requested URL was not found on the server. " \
              "If you entered the URL manually please check your spelling and try again."
        return Status.FAILURE, ValidationTypes.URL_ERROR, msg

    def process_get(self, *args, **kwargs):

        audio_file_type = kwargs['audioFileType']
        audio_file_id = kwargs.get("audioFileID")

        query = f"SELECT * FROM {audio_file_type}"
        if audio_file_id:
            query = query + " WHERE id=%s"
            return self.pg_connector.fetchone(query, (int(audio_file_id),))
        return self.pg_connector.fetchall(query)


class AudioCreate(ApiBase):

    def __init__(self):
        super().__init__()

    @property
    def json_schema(self):
        return CREATE_SCHEMA_DICT

    @property
    def validator(self):
        return CREATE_SCHEMA_DICT_VALIDATOR

    def process_post(self):
        audio_file_type = self.request_data["audioFileType"]
        audio_file_metadata = self.request_data["audioFileMetadata"]

        if audio_file_type == AudioType.SONG:
            query = "INSERT INTO song (name, duration) VALUES (%s,%s)"
            self.pg_connector.execute(query, (audio_file_metadata["name"], audio_file_metadata["duration"]))
        elif audio_file_type == AudioType.PODCAST:
            query = "INSERT INTO podcast (name, duration, host, participants) VALUES (%s,%s,%s,%s)"
            self.pg_connector.execute(query, (audio_file_metadata["name"], audio_file_metadata["duration"],
                                              audio_file_metadata["host"], audio_file_metadata["participants"]))
        else:
            query = "INSERT INTO audiobook (title, author, narrator, duration) VALUES (%s,%s,%s,%s)"
            self.pg_connector.execute(query, (audio_file_metadata["title"], audio_file_metadata["author"],
                                              audio_file_metadata["narrator"], audio_file_metadata["duration"]))
        return {"message": "Data Inserted Successfully"}


class AudioDelete(ApiBase):

    def __init__(self):
        super().__init__()

    def validate_parameters(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        if audio_file_type in [AudioType.SONG, AudioType.PODCAST, AudioType.AUDIO_BOOK]:
            return Status.SUCCESS, None, None

        msg = "The requested URL was not found on the server. " \
              "If you entered the URL manually please check your spelling and try again."
        return Status.FAILURE, ValidationTypes.URL_ERROR, msg

    def process_delete(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        audio_file_id = int(kwargs["audioFileID"])
        check_query = f"SELECT 1 FROM {audio_file_type} WHERE id=%s"
        if not self.pg_connector.fetchone(check_query, (audio_file_id,)):
            return {"message": f"Data For {audio_file_type} with ID {audio_file_id} Does Not Exists"}
        query = f"DELETE FROM {audio_file_type} WHERE id=%s"
        self.pg_connector.execute(query, (audio_file_id,))
        return {"message": f"Deleted {audio_file_type} with ID {audio_file_id} Successfully"}


class AudioUpdate(ApiBase):

    def __init__(self):
        super().__init__()

    @property
    def json_schema(self):
        return CREATE_SCHEMA_DICT

    @property
    def validator(self):
        return CREATE_SCHEMA_DICT_VALIDATOR

    def validate_parameters(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        if audio_file_type in [AudioType.SONG, AudioType.PODCAST, AudioType.AUDIO_BOOK]:
            return Status.SUCCESS, None, None

        msg = "The requested URL was not found on the server. " \
              "If you entered the URL manually please check your spelling and try again."
        return Status.FAILURE, ValidationTypes.URL_ERROR, msg

    def validate_schema(self, *args, **kwargs):
        if inspect.ismethod(self.request_data):
            raise Exception(f"Should define '{self.json_schema.__name__}' as property")

        data_dict = {
            "audioFileType": kwargs["audioFileType"],
            "audioFileMetadata": self.request_data
        }

        try:
            self.validator(data_dict)
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

    def process_put(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        audio_file_id = int(kwargs["audioFileID"])
        check_query = f"SELECT 1 FROM {audio_file_type} WHERE id=%s"
        if not self.pg_connector.fetchone(check_query, (audio_file_id,)):
            return {"message": f"Data For {audio_file_type} with ID {audio_file_id} Does Not Exists"}

        if audio_file_type == AudioType.SONG:
            query = "UPDATE song SET name=%s, duration=%s WHERE id=%s"
            self.pg_connector.execute(query, (self.request_data["name"], self.request_data["duration"], audio_file_id))
        elif audio_file_type == AudioType.PODCAST:
            query = "UPDATE podcast SET name=%s, duration=%s, host=%s, participants=%s WHERE id=%s"
            self.pg_connector.execute(query, (self.request_data["name"], self.request_data["duration"],
                                              self.request_data["host"], self.request_data["participants"],
                                              audio_file_id))
        else:
            query = "UPDATE audiobook SET title=%s, author=%s, narrator=%s, duration=%s WHERE id=%s"
            self.pg_connector.execute(query, (self.request_data["title"], self.request_data["author"],
                                              self.request_data["narrator"], self.request_data["duration"],
                                              audio_file_id))
        return {"message": f"Updated Data For {audio_file_type} with ID {audio_file_id} Successfully"}


