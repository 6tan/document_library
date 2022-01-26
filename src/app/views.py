#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import json
from inspect import getframeinfo, currentframe
from pathlib import Path
from werkzeug.security import check_password_hash, generate_password_hash
from utils.utils_constant import AudioType, Status, ValidationTypes
from .api_base import ApiBase
from db.models import User, db, Document, DocMap, History
import uuid
from datetime import datetime
filename = getframeinfo(currentframe()).filename
current_module_path = Path(filename).resolve().parent
ROOT_PATH = Path(current_module_path).parents[1].as_posix()


def token_required(f):
    def proc(self, *args, **kwargs):
        token = self.request_headers.get("token")
        if not token:
            return Status.FAILURE, ValidationTypes.VALIDATION, "No Token Provided"
        user = User.query.filter_by(token=token).first()
        if not user:
            return Status.FAILURE, ValidationTypes.VALIDATION, "Invalid Token Provided"
        return f(self, *args, **kwargs)
    return  proc


class CreateUser(ApiBase):

    def __init__(self):
        super().__init__()
    
    def validate_request(self):
        request_data = self.request_data.json
        email = request_data.get("email")
        password = request_data.get("password")
        if email and password:
            user = User.query.filter_by(email=email).first()
            if not user:
                 return Status.SUCCESS, None, None
            else:
                message = "Email Already Exist"
        else:
            message = "Missing email or document_id in request json"

        return Status.FAILURE, ValidationTypes.VALIDATION, message

    def process_post(self):
        request_data = self.request_data.json
        email = request_data["email"]
        password = request_data["password"]
        user_obj = User(email=email, password=generate_password_hash(password), token=str(uuid.uuid4()))
        db.session.add(user_obj)
        db.session.commit()
        return {"message": "User Created Successfully"}

class Login(ApiBase):

    def __init__(self):
        super().__init__()
    
    def validate_parameters(self, *args, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        if email and password:
            return Status.SUCCESS, None, None

        msg = "Check if Email and password are provided"
        return Status.FAILURE, ValidationTypes.VALIDATION, msg

    def process_get(self, *args, **kwargs):
        email = kwargs.get("email")
        password = kwargs.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                return {"token": user.token}, "success", 200, ""
        return {}, "Invalid Credentials", 400, ValidationTypes.VALIDATION


class DocumentGet(ApiBase):

    def __init__(self):
        super().__init__()

    @token_required
    def validate_parameters(self, *args, **kwargs):
        return Status.SUCCESS, None, None

    def process_get(self, *args, **kwargs):
        document_id = kwargs.get("documentID")
        user = User.query.filter_by(token=self.request_headers["token"]).first()
        if document_id:
            # fetch given document id
            document = Document.query.get(document_id)
            if not document:
                return {}, f"Document with id {document_id} doesnot exist.", 400, ValidationTypes.VALIDATION
            
            #check if document is available for user
            docmap = DocMap.query.filter_by(user_id=user.id,document_id=document_id).first()
            if not docmap:
                return {}, "Document Unavailable For Requested User", 400, ValidationTypes.VALIDATION

            if document.user_id == user.id:
                document.lock = True # lock if owner downloads document
                db.session.commit()
            elif document.lock == True:
                return {}, f"Document with id {document_id} is beign edited by Owner", 400, ValidationTypes.VALIDATION
                
            self.is_file = True
            response = f"{ROOT_PATH}/src/documents/document_{document_id}.txt"
            history = History(user_id=user.id, document_id=document_id, action="download")
            db.session.add(history)
            db.session.commit()
        else:
            # list all documents for the user
            docmap = DocMap.query.filter_by(user_id=user.id).all()
            response = {"documents": [doc.document_id for doc in docmap]}
        return response, "success", 200, ""

class DocumentShare(ApiBase):

    def __init__(self):
        super().__init__()
    
    @token_required
    def validate_request(self):
        request_data = self.request_data.json
        email = request_data.get("email")
        document_id = request_data.get("document_id")
        owner = User.query.filter_by(token=self.request_headers["token"]).first()
        if email and document_id:
            shared_user = User.query.filter_by(email=email).first()
            if shared_user:
                if shared_user.id != owner.id:
                    document = Document.query.filter_by(id=document_id).first()
                    if document:
                        if document.user_id == owner.id:
                            return Status.SUCCESS, None, None
                        else:
                            message = f"Access Denied: Only Owner of Document has access to share."
                    else:
                        message = f"Document with id {document_id} doesnot exist."
                else:
                    message = f"Cannot Share with owner."
            else:
                message = "Invalid Email."
        else:
            message = "Missing email or document_id in request json."

        return Status.FAILURE, ValidationTypes.VALIDATION, message

    def process_post(self):
        request_data = self.request_data.json
        email = request_data["email"]
        document_id = request_data["document_id"]
        user = User.query.filter_by(email=email).first()
        docmap = DocMap.query.filter_by(document_id=document_id, user_id=user.id).first()
        if not docmap: # do not create map if its already present
            docmap = DocMap(user_id=user.id, document_id=document_id)
            db.session.add(docmap)
            db.session.commit()
 
        return {"message": "Document Shared Successfully"}

class DocumentCreate(ApiBase):

    def __init__(self):
        super().__init__()
    
    @token_required
    def validate_request(self):
        if self.request_data.files.get("file"):
            return Status.SUCCESS, None, None
        else:
            return Status.FAILURE, ValidationTypes.VALIDATION, "Invalid Request: Please Upload document"

    def process_post(self):
        user = User.query.filter_by(token=self.request_headers["token"]).first()
        document = Document(user_id=user.id,version=1,)
        db.session.add(document)
        db.session.flush()
        db.session.commit()
        file_obj = self.request_data.files["file"]
        file_obj.save(f"{ROOT_PATH}/src/documents/document_{document.id}.txt") # save file 
        docmap = DocMap(user_id=user.id, document_id=document.id) # map file to user
        db.session.add(docmap)
        db.session.commit()
        return {"message": f"Document Saved Successfully with id {document.id}"}


class DocumentDelete(ApiBase):

    def __init__(self):
        super().__init__()

    @token_required
    def validate_parameters(self, *args, **kwargs):
        document_id = kwargs["documentID"]
        user = User.query.filter_by(token=self.request_headers["token"]).first()
        document = Document.query.filter_by(id=int(document_id)).first()
        if document:
            if document.user_id == user.id:
                return Status.SUCCESS, None, None
            else:
                message = "Permssion Denied: Shared User cannot delete document"
        else:
            message = f"Document with id {document_id} Doesnot Exist."
        return Status.FAILURE, ValidationTypes.VALIDATION, message

    def process_delete(self, *args, **kwargs):
        document_id = int(kwargs["documentID"])
        Document.query.filter_by(id=document_id).delete() # delete document
        DocMap.query.filter_by(document_id=document_id).delete() # delete mapping 
        db.session.commit()
        return {"message": f"Deleted document with ID {document_id} Successfully"}


class DocumentUpdate(ApiBase):

    def __init__(self):
        super().__init__()
    
    @token_required
    def validate_parameters(self, *args, **kwargs):
        document_id = int(kwargs['documentID'])
        document = Document.query.get(document_id)
        user = User.query.filter_by(token=self.request_headers["token"]).first()
        if document:
            docmap = DocMap.query.filter_by(user_id=user.id,document_id=document_id).first()
            if not docmap:
                return Status.FAILURE, ValidationTypes.VALIDATION,"Document Unavailable For Requested User"
            if self.request_data.files.get("file"):
                return Status.SUCCESS, None, None
            else:
                return Status.FAILURE, ValidationTypes.VALIDATION, "Invalid Request: Please Upload document"
        else:
            message = f"Document with id {document_id} Doesnot Exist."
        return Status.FAILURE, ValidationTypes.VALIDATION, message

    def process_put(self, *args, **kwargs):
        document_id = int(kwargs['documentID'])
        user = User.query.filter_by(token=self.request_headers["token"]).first()
        document = Document.query.get(document_id)
        if user.id == document.user_id:
            document.lock = False # unlock if owner uploads document
            document.last_update_date = datetime.now()
            db.session.commit()
            history = History(user_id=user.id, document_id=document_id, action="upload")
            db.session.add(history)
            db.session.commit()
        elif document.lock == True:
            return {}, f"Document with id {document_id} is beign edited by Owner", 400, ValidationTypes.VALIDATION
        else:
            history = History.query.filter_by(user_id=user.id, document_id=document_id, 
                        action='download').order_by(History.last_update_date.desc()).first()
            if history and history.last_update_date < document.last_update_date: # check if shared user is uploading wth latest version of doc
                return {}, f"Document with id {document_id} is updated by Owner, \
                    please download latest document for further edits.", 400, ValidationTypes.VALIDATION

        file_obj = self.request_data.files["file"]
        file_obj.save(f"{ROOT_PATH}/src/documents/document_{document_id}.txt")
        return {"message": f"Document with id {document_id} Updated Successfully."}, "Success", 200, ""

        
