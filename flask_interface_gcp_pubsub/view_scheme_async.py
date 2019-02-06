from flask_restful import Resource as BaseRestfulResource
from flask import request
from .pubsub import PubSub
from .utils import process_message


class ViewSchemeAsync(BaseRestfulResource):
    """
        Base class to send messages to Google's Pub/Sub asynchronously.

        properties:
            topic_name (:obj: `string`, required): The name of the topic to
            publish messages to.
            schema (:obj:`dict`, required): A JSON schema for contract
            validation. JSON Schema is a vocabulary that allows you to annotate
            and validate JSON documents.
    """

    def __init__(self, *args, **kwargs):
        topic_name = getattr(self, "topic_name")

        self.schema = getattr(self, "schema")
        self.publisher = PubSub(topic_name)
        return super().__init__(*args, **kwargs)

    def get(self):
        """
            Returns information with schema for request.
        """
        return self.schema, 200

    def post(self):
        """
            If json body message is valid, create on google pub sub this
            data.
        """
        return process_message(self.schema, self.publisher, request.data)