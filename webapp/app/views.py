#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import json
from inspect import getframeinfo, currentframe
from pathlib import Path

from utils.utils_constant import AudioType, Status, ValidationTypes
from .api_base import ApiBase
from db.models import User, db
filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent
ROOT_PATH = Path(current_module_path).parents[1].as_posix()


class CreateUser(ApiBase):

    def __init__(self):
        super().__init__()

    def process_post(self):
        request_data = json.loads(self.request_data.data)
        email = request_data["email"]
        user = User.query.filter_by(email=email).first()
        if user:
            return {}, 400, "User Already Exist", ValidationTypes.VALIDATION
        else:
            user_obj = User(email=email)
            db.session.add(user_obj)
            db.session.commit()
            return 200, {"message": "User Created Successfully"}


class DocumentGet(ApiBase):

    def __init__(self):
        super().__init__()

    def validate_parameters(self, *args, **kwargs):


        return Status.SUCCESS, None, None

        # msg = "The requested URL was not found on the server. " \
        #       "If you entered the URL manually please check your spelling and try again."
        # return Status.FAILURE, ValidationTypes.URL_ERROR, msg

    def process_get(self, *args, **kwargs):
        document_id = kwargs.get("documentID")

        return f"{ROOT_PATH}/sample.txt"


class DocumentCreate(ApiBase):

    def __init__(self):
        super().__init__()

    def process_post(self):
        obj = self.request_data.files["file"]
        obj.save(f"{ROOT_PATH}/sample.txt")
        print(self.request_data.files["file"])

        # if audio_file_type == AudioType.SONG:
        #     query = "INSERT INTO song (name, duration) VALUES (%s,%s)"
        #     self.pg_connector.execute(query, (audio_file_metadata["name"], audio_file_metadata["duration"]))
        # elif audio_file_type == AudioType.PODCAST:
        #     query = "INSERT INTO podcast (name, duration, host, participants) VALUES (%s,%s,%s,%s)"
        #     self.pg_connector.execute(query, (audio_file_metadata["name"], audio_file_metadata["duration"],
        #                                       audio_file_metadata["host"], audio_file_metadata["participants"]))
        # else:
        #     query = "INSERT INTO audiobook (title, author, narrator, duration) VALUES (%s,%s,%s,%s)"
        #     self.pg_connector.execute(query, (audio_file_metadata["title"], audio_file_metadata["author"],
        #                                       audio_file_metadata["narrator"], audio_file_metadata["duration"]))
        return {"message": "Data Inserted Successfully"}


class DocumentDelete(ApiBase):

    def __init__(self):
        super().__init__()

    def validate_parameters(self, *args, **kwargs):
        document_id = kwargs['audioFileType']
        # if audio_file_type in [AudioType.SONG, AudioType.PODCAST, AudioType.AUDIO_BOOK]:
        return Status.SUCCESS, None, None

        # msg = "The requested URL was not found on the server. " \
        #       "If you entered the URL manually please check your spelling and try again."
        # return Status.FAILURE, ValidationTypes.URL_ERROR, msg

    def process_delete(self, *args, **kwargs):
        document_id = int(kwargs["documentID"])
        check_query = f"SELECT 1 FROM document WHERE id=%s"
        if not self.pg_connector.fetchone(check_query, (document_id,)):
            return {"message": f"Document with ID {document_id} Does Not Exists"}
        query = f"DELETE FROM document WHERE id=%s"
        self.pg_connector.execute(query, (document_id,))
        return {"message": f"Deleted document with ID {document_id} Successfully"}


class DocumentUpdate(ApiBase):

    def __init__(self):
        super().__init__()

    def validate_parameters(self, *args, **kwargs):
        audio_file_type = kwargs['audioFileType']
        if audio_file_type in [AudioType.SONG, AudioType.PODCAST, AudioType.AUDIO_BOOK]:
            return Status.SUCCESS, None, None

        msg = "The requested URL was not found on the server. " \
              "If you entered the URL manually please check your spelling and try again."
        return Status.FAILURE, ValidationTypes.URL_ERROR, msg

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
