from unittest import mock
from unittest import TestCase
from flask_interface_gcp_pubsub.pubsub import PubSub, Publisher

MOCK_DATA = {
    'my_data': {
        'key': 'value'
    }
}


class TestPubSub(TestCase):
    @mock.patch.object(Publisher, '__init__', return_value=None)
    def test_multiton_with_the_same_parameter(self, mock_pub):
        first_client = PubSub('test_with_the_same_parameter')
        second_client = PubSub('test_with_the_same_parameter')
        self.assertEqual(first_client, second_client)

    @mock.patch.object(Publisher, '__init__', return_value=None)
    def test_multiton_with_a_different_parameter(self, mock_pub):
        first_client = PubSub('test')
        second_client = PubSub('test2')
        self.assertNotEquals(first_client, second_client)

    def test_publish(self):
        publisher = mock.MagicMock()
        client = PubSub('test_publish', publisher)
        client.publish(MOCK_DATA)
        expected = [
            mock.call.publish(
                'test_publish', data=b'{"my_data": {"key": "value"}}'
            )
        ]
        self.assertEqual(publisher.method_calls, expected)