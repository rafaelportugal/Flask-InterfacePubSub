import os
from google.cloud import pubsub_v1
from mementos import MementoMetaclass


class Publisher(metaclass=MementoMetaclass):
    """
        Base class that uses the multiton design pattern, to help publishing
        messages on Google's Pub/Sub. An instance of this class returns the
        same memory address when the parameters in the constructor are equals.

        When this class receives at least one of the batch configuration
        parameters, its message submission feature occour in batch.

        Args:
            project_id (:obj: `str`, optioanl): The name of the project
            at GCP. Can also be provided by defining a value for the
            system environment variable 'GCP_PROJECT_ID' with the name
            of your cloud project.

            max_bytes (:obj: `int`, optional): Max bytes per batch. Batch
            configuration parameter, if there is any batch parameter being
            sent and this field is not passed, default value is: 1048576.

            max_latency (:obj:`int`, optional): Max latency in seconds. Batch
            configuration parameter, if there is any batch parameter being sent
            and this field is not passed, default value is: 15.

            max_messages (:obj:`int`, optional): Max messages per batch. Batch
            configuration parameter, if there is any batch parameter being sent
            and this field is not passed, default value is: 1000.
    """

    def __init__(self,
                 project_id=None,
                 max_bytes=None,
                 max_latency=None,
                 max_messages=None,
                 *args,
                 **kwargs):
        self.project_id = project_id or os.environ["GCP_PROJECT_ID"]

        if max_bytes or max_latency or max_messages:
            settings = {
                "max_bytes": max_bytes or 1048576,
                "max_latency": max_latency or 15,
                "max_messages": max_messages or 1000,
            }
            batch_settings = pubsub_v1.types.BatchSettings(**settings)
            self.__publisher = pubsub_v1.PublisherClient(batch_settings)
        else:
            self.__publisher = pubsub_v1.PublisherClient()

        return super().__init__(*args, **kwargs)

    def _topic_path(self, topic_name):
        """This method returns the full path of the topic name

        Args:
            topic_name (:obj: `string`, required): The name of the topic to
            publish messages to.

        Returns:
            Full path name of the topic required

        Return type:
            String
        """
        return self.__publisher.topic_path(self.project_id, topic_name)

    def publish(self, topic_name, data):
        """This method returns the full path of the topic name

        Args:
            topic_name (:obj: `string`, required): The name of the topic to
            publish messages to.
            data: A bytestring representing the message body. This must be a
            bytestring.

        Returns:
            An object conforming to the concurrent.futures.Future interface.

        Return type:
            Future
        """
        topic_path = self._topic_path(topic_name)
        return self.__publisher.publish(topic_path, data=data)
