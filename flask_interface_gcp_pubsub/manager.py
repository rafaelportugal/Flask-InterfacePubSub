import json
from mementos import MementoMetaclass
from .gcp import Publisher


class PubSub(metaclass=MementoMetaclass):
    """
        Base class that uses the partner multiton, for manager the publish message
        on using a publisher class on specific topic. This instance return same
        memory address when parameters are equals.

        Args:
            topic_name (:obj: `string`, required): The name of the topic to publish
            messages to.

            publisher (:obj:`Publisher`, optional): Instance of the Publisher.
            This object using of the concept Duck typing. In duck typing, an object's
            suitability is determined by the presence of certain methods and properties,
            rather than the type of the object itself. This case, need to the presence
            of the method 'publish'.
    """

    def __init__(self, topic_name, publisher=Publisher()):
        self.topic_name = topic_name
        self.publisher = publisher

    def publish(self, data):
        """
            Publish a single message.

            Args:
                data (:obj: `dict`, required): A dictionary representing the
                message body.
        """
        data = json.dumps(data).encode('utf-8')
        self.publisher.publish(self.topic_name, data=data)
