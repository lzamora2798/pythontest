#! -*- coding: utf-8 -*-
import logging
from contextlib import ContextDecorator

from environs import Env
from mongoengine import connect, disconnect, connection
import mongomock

logger = logging.getLogger()

env = Env()

# noinspection PyUnresolvedReferences
env.read_env()


# noinspection PyUnresolvedReferences
def acquire_db_client():
    """
    :return: The client connection to the specified database.
    """

    db_name = env.str("MONGO_FTF_DB")

    if env.bool("USE_MONGO_MOCK", False):
        client_db = connect(db_name, mongo_client_class=mongomock.MongoClient)
        return client_db, db_name

    if env.bool("MONGO_USE_LOCAL", False):
        try:
            client_db = connect(db_name)
        except connection.MongoEngineConnectionError as connection_err:
            logger.warning(
                f"Connection failed, trying disconnect and connect again: {connection_err}"
            )
            try:
                disconnect()
            except Exception as err:
                logger.error(f"Trying to disconnect after connection error: {err}")
                raise
            else:
                client_db = connect(db_name)
    else:
        host = env.str("MONGO_FTF_URL")
        port = env.int("MONGO_PORT", None)
        username = env.str("MONGO_USERNAME", None)
        password = env.str("MONGO_PASSWORD", None)

        settings = {
            "host": host,
            "port": port,
            "username": username,
            "password": password,
            "compressors": "zlib",
        }
        try:
            client_db = connect(db_name, **settings)
        except connection.ConnectionFailure as connection_err:
            logger.warning(
                f"Connection failed, trying disconnect and connect again: {connection_err}"
            )
            try:
                disconnect()
            except Exception as err:
                logger.error(f"Trying to disconnect after connection error: {err}")
                raise
            else:
                client_db = connect(db_name, **settings)

    return client_db, db_name


class db_connection(ContextDecorator):
    """
    Use this for decorate a function that require access to the
    database. This will open the connection and close the same connection
    after the function finish its work.

    Ex:
        @db_connection(tenant)
        def foo():
            pass

    Ex:

        with db_connection(tenant):
            ...
    """

    def __init__(
        self,
    ):
        self.db_name = None

    def __enter__(self):
        self.db_client, self.db_name = acquire_db_client()

        return self.db_client, self.db_name

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Exiting context nothing to do here, connections are managed by the garbage collector.
        pass