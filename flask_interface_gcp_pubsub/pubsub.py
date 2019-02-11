import json
from mementos import MementoMetaclass
from .publisher import Publisher


class PubSub(metaclass=MementoMetaclass):
    """
        Base class that uses the multiton design pattern, to publish
        messages on using a publisher class at a specific topic. An
        instance of this class returns the same memory address when
        the parameters in the constructor are equals.

        Args:
            topic_name (:obj: `string`, required): The name of the topic to
            publish messages to.

            publisher (:obj:`Publisher`, optional): Instance of the Publisher.
            This object uses the concept of Duck typing. In duck typing, an
            object's suitability is determined by the presence of certain
            methods and properties, rather than the type of the object itself.
            In this case, we need to the presence of the method 'publish'.
    """

    def __init__(self, topic_name, publisher=None):
        self.topic_name = topic_name
        self.publisher = publisher or Publisher()

    def publish(self, data):
        """
            Publish a single message.

            Args:
                data (:obj: `dict`, required): A dictionary representing the
                message body.
        """
        data = json.dumps(data).encode('utf-8')
        self.publisher.publish(self.topic_name, data=data)
