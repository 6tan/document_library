#!/usr/bin/env python3.8
# -*- coding: utf-8 -*-
import logging
import os
from typing import Tuple, Dict, List

import psycopg2
from psycopg2.extras import RealDictCursor
from utils.utils_exception import PostgresConnectorError

logger = logging.getLogger("search_logger")


class PostgresConnector(object):
    def __init__(self):
        self.connection = None
        self.create_connection()

    def create_connection(self):
        """
        This method is used to initialize the connection.
        """
        db_config = {
            'database': os.environ["PG_DATABASE"],
            'host': os.environ["PG_HOST"],
            'password': os.environ["PG_PASSWORD"],
            'port': os.environ["PG_PORT"],
            'user': os.environ["PG_USER"],
            'cursor_factory': RealDictCursor,
            'sslmode': 'disable'
        }
        self.connection = psycopg2.connect(**db_config)

    def fetchone(self, query: str, args: Tuple = None) -> Dict:
        """
        Fetch the next row of a query result set, returning a single tuple, or None when no more data is available
        :param query: Query the has to be fired.
        :param args: Arguments required to execute query
        :return: Dict
        """

        conn = self.connection
        curr = conn.cursor()

        try:
            curr.execute(query, vars=(args or ()))
            result = curr.fetchone()
        except psycopg2.OperationalError:
            logger.error(f"[Debug] psycopg2 Operational Error", exc_info=1)
            if self.connection is not None:
                self.connection.close()
            self.create_connection()
            result = self.fetchone(query, args)
        except psycopg2.ProgrammingError as error:
            conn.rollback()
            raise PostgresConnectorError(error)

        return result

    def fetchall(self, query, args=None) -> List[Dict]:
        """
        Fetch all (remaining) rows of a query result, returning them as a list of tuples. An empty list is
        returned if there is no more record to fetch.

        :param query: Query the has to be fired.
        :param args: Arguments required to execute query
        """
        conn = self.connection
        curr = conn.cursor()

        try:
            curr.execute(query, vars=(args or ()))
            result = curr.fetchall()
        except psycopg2.OperationalError:
            logger.error(f"[Debug] psycopg2 Operational Error", exc_info=1)
            if self.connection is not None:
                self.connection.close()
            self.create_connection()
            result = self.fetchall(query, args)
        except psycopg2.ProgrammingError as error:
            conn.rollback()
            raise PostgresConnectorError(error)

        return result

    def execute(self, query: str, args=None):
        """
        Execute a database operation (query or command).

        :param return_fields:
        :param query: Query the has to be fired.
        :param args: Arguments required to execute query
        """
        conn = self.connection
        curr = conn.cursor()

        try:
            curr.execute(query, vars=(args or ()))
            conn.commit()
        except psycopg2.OperationalError:
            logger.error(f"[Debug] psycopg2 Operational Error", exc_info=1)
            if self.connection is not None:
                self.connection.close()
            self.create_connection()
            self.execute(query, args)
        except psycopg2.ProgrammingError as error:
            conn.rollback()
            raise PostgresConnectorError(error)


connector = PostgresConnector()
