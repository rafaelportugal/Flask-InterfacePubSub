import json
from jsonschema import validate, FormatChecker
from jsonschema.exceptions import ValidationError
from flask import request


def process_message(schema, publisher, data):
    """
        Method to process messsages for all the bases that uses
        Google's Pub/Sub.

        Args:
            schema (:obj:`dict`, required): A JSON schema for contract
            validation. JSON Schema is a vocabulary that allows you
            to annotate and validate JSON documents.
            publisher (:obj:`PubSub`, optional): Instance of the
            '.manager.PubSub'. data (:obj: `dict`, required):
            A dictionary representing the message body.
    """
    try:
        data = json.loads(request.data)
        validate(data, schema, format_checker=FormatChecker())
        publisher.publish(data)
        return data, 202
    except ValidationError as validate_error:
        return str(validate_error), 400
