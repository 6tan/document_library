#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
from utils.utils_constant import Method
from . import views


def register_url(app, view, url, endpoint, method):
    url = f"/api/v1/{url}"
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, view_func=view_func, methods=[method.upper()])


def register_urls(app):
    register_url(app=app, view=views.CreateUser, endpoint='create_user', url='user/create', method=Method.POST)
    register_url(app=app, view=views.DocumentGet, endpoint='get_documents', url='documents', method=Method.GET)
    register_url(app=app, view=views.DocumentGet, endpoint='get_document_file', url='document/<documentID>', method=Method.GET)
    register_url(app=app, view=views.DocumentCreate, endpoint='create_document', url='document/create', method=Method.POST)
    register_url(app=app, view=views.DocumentUpdate, endpoint='update_document', url='document/<documentID>',
                 method=Method.PUT)
    register_url(app=app, view=views.DocumentDelete, endpoint='delete_document', url='document/<documentID>',
                 method=Method.DELETE)
