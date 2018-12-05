import json

from flask_restful import Resource as BaseRestfulResource
from flask import request
from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError

from mementos import MementoMetaclass

from .manager import PubSub
from .gcp import Publisher


def process_message(schema, publisher, data):
    """
        Method to reuse the message processing for all the bases of the
        gogole pub sub.

        Args:
            schema (:obj:`dict`, required): A JSON schema for border validation. 
            JSON Schema is a vocabulary that allows you to annotate and validate
            JSON documents.
            publisher (:obj:`PubSub`, optional): Instance of the '.manager.PubSub'.
            data (:obj: `dict`, required): A dictionary representing the
                message body.
    """
    try:
        data = json.loads(request.data)
        validate(data, schema, format_checker=FormatChecker())
        publisher.publish(data)
        return data, 202
    except ValidationError as validate_error:
        return str(validate_error), 400


class ViewSchemeAsync(BaseRestfulResource):
    """
        Base class for sending messages to google pub sub in asynchronous way.

        properties:
            topic_name (:obj: `string`, required): The name of the topic to publish
            messages to.
            schema (:obj:`dict`, required): A JSON schema for border validation. 
            JSON Schema is a vocabulary that allows you to annotate and validate
            JSON documents.
    """

    def __init__(self, *args, **kwargs):
        topic_name = getattr(self, "topic_name")

        self.schema = getattr(self, "schema")
        self.publisher = PubSub(topic_name)
        return super().__init__(*args, **kwargs)

    def get(self):
        """
            Return information with schema for request.
        """
        return self.schema, 200

    def post(self):
        """
            If json body message is valid, create on google pub sub this
            data.
        """
        return process_message(self.schema, self.publisher, request.data)


class ViewSchemeBatch(BaseRestfulResource):
    """
        Base class for sending messages to google pub sub in asynchronous way in batch.

        properties:
            topic_name (:obj: `string`, required): The name of the topic to publish
            messages to.
            schema (:obj:`dict`, required): A JSON schema for border validation. 
            JSON Schema is a vocabulary that allows you to annotate and validate
            JSON documents.
    """

    def __init__(self, *args, **kwargs):
        topic_name = getattr(self, "topic_name")
        self.schema = getattr(self, "schema")

        batch_settings = {"max_bytes": 1048576, "max_latency": 15}

        publisher = Publisher(**batch_settings)
        self.publisher = PubSub(topic_name, publisher)

        return super().__init__(*args, **kwargs)

    def get(self):
        """
            Return information with schema for request.
        """
        return self.schema, 200

    def post(self):
        """
            If json body message is valid, create on google pub sub this
            data.
        """
        return process_message(self.schema, self.publisher, request.data)
