from unittest import mock
from unittest import TestCase
from flask_interface_gcp_pubsub.pubsub import PubSub, Publisher


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
        mock_pub.assert_called_once()
        self.assertNotEquals(first_client, second_client)
