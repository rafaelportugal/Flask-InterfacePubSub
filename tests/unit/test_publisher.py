from unittest import mock
from unittest import TestCase
from google.cloud import pubsub_v1
from flask_interface_gcp_pubsub.pubsub import Publisher


ENV_MOCK = {
    'GCP_PROJECT_ID': 'test'
}
TOPIC_NAME = 'my_topic'
MOCK_DATA = 'my_test_data'


@mock.patch.dict('os.environ', values=ENV_MOCK)
class TestPublisher(TestCase):
    def setUp(self):
        self._topic_path = Publisher._topic_path

    def tearDown(self):
        Publisher._topic_path = self._topic_path

    def test_project_id(self):
        pub = Publisher()
        self.assertEqual(pub.project_id, ENV_MOCK['GCP_PROJECT_ID'])

    @mock.patch('google.cloud.pubsub_v1.PublisherClient')
    @mock.patch('google.cloud.pubsub_v1.types.BatchSettings')
    def test_settings(self, mock_settings, mock_client):
        Publisher(max_bytes=1,
                  max_latency=2,
                  max_messages=3)

        expected_settings_calls = [
            mock.call(max_bytes=1, max_latency=2, max_messages=3),
            mock.call(max_bytes=1, max_latency=2, max_messages=3)
        ]
        expected_client_calls = [
            mock.call(pubsub_v1.types.BatchSettings(
                max_bytes=1, max_latency=2, max_messages=3
            ))
        ]

        self.assertEquals(mock_settings.mock_calls, expected_settings_calls)
        self.assertEquals(mock_client.mock_calls, expected_client_calls)

    @mock.patch('google.cloud.pubsub_v1.PublisherClient')
    def test_default_client(self, mock_client):
        Publisher()
        expected = [mock.call()]
        self.assertEquals(mock_client.mock_calls, expected)

    @mock.patch('google.cloud.pubsub_v1.PublisherClient')
    def test_topic_path(self, mock_client):
        pub = Publisher()
        pub._Publisher__publisher = mock.MagicMock()
        pub._topic_path(TOPIC_NAME)

        expected = [
            mock.call.topic_path(
                ENV_MOCK['GCP_PROJECT_ID'],
                TOPIC_NAME
            )
        ]
        self.assertEquals(pub._Publisher__publisher.mock_calls, expected)

    @mock.patch('google.cloud.pubsub_v1.PublisherClient')
    def test_publish(self, mock_client):
        pub = Publisher()
        Publisher._topic_path = mock.MagicMock(return_value=TOPIC_NAME)
        pub.publish(TOPIC_NAME, MOCK_DATA)

        expected = [mock.call.publish(TOPIC_NAME, data=MOCK_DATA)]

        pub._topic_path.assert_called_once()
        self.assertEquals(pub._Publisher__publisher.mock_calls, expected)
