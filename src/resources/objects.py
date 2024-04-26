import os
import pika
import pymongo
import logging
from dataclasses import dataclass

from fastapi.security import OAuth2PasswordBearer

from resources.broker_constants import (
    BROKER_IP,
    BROKER_PORT,
    BROKER_USERNAME,
    BROKER_PASSWORD,
)
# from resources.secrets import TOKEN_URL

# from utilities.session_utils import get_session_data, set_session_paths_to_constants

logger = logging.getLogger("Objects")
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl=TOKEN_URL)


@dataclass
class AppResources:
    database: any = None
    channel: any = None
    connection: any = None
    paho: any = None
    celery_broker: any = None
    celery_backend: any = None

    @classmethod
    def initialize(cls):
        resources = cls()

        # MongoDB setup
        try:
            resources.database = pymongo.MongoClient("mongodb://localhost:27017/")["hotel_users"]
            logger.info("MongoDB Connected!")
        except pymongo.errors.ConnectionFailure as e:
            logger.error(f"MongoDB Connection Failed: {e}")

        # RabbitMQ setup
        try:
            credentials = pika.PlainCredentials(BROKER_USERNAME, BROKER_PASSWORD)
            parameters = pika.ConnectionParameters(BROKER_IP, BROKER_PORT, '/', credentials)
            resources.connection = pika.BlockingConnection(parameters)
            resources.channel = resources.connection.channel()
            logger.info("RabbitMQ Connected!")
        except Exception as e:
            logger.error(f"RabbitMQ Connection Failed: {e}")

        return resources

    def destroy(self):
        # Closing MongoDB connection
        self.database.client.close()
        logger.info("MongoDB Connection Closed!")

        # Closing RabbitMQ connection if it exists
        if self.connection is not None:
            self.connection.close()
            logger.info("RabbitMQ Connection Closed!")
        else:
            logger.warning("RabbitMQ Connection object is None, skipping closing.")


app_resources = AppResources
