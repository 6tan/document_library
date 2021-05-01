#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import psycopg2


class PostgresConnectorError(psycopg2.ProgrammingError):
    def __init__(self, *args, **kwargs):
        pass


class ValueExists(Exception):
    pass
