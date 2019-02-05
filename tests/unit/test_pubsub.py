from unittest import TestCase
from flask_interface_gcp_pubsub.pubsub import PubSub


class TestManager(TestCase):
    def test_multiton_with_the_same_parameter(self):
        first_client = PubSub('test')
        second_client = PubSub('test')
        self.assertEqual(first_client, second_client)

    def test_multiton_with_a_different_parameter(self):
        first_client = PubSub('test')
        second_client = PubSub('test2')
        self.assertNotEquals(first_client, second_client)
