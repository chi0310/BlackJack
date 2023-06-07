import os
import time
import unittest
from datetime import timedelta


class TestMiddlewareJwt(unittest.TestCase):

    def setUp(self) -> None:
        # set env and import
        os.environ['JWT_SECRET_KEY'] = 'test'
        from blackjack.controller.middleware.jwt import JWT
        self.jwt = JWT()

    def test_jwt(self):
        encoded_data = {
            'username': 'test_username',
            'email': 'test_email',
        }
        # test1
        # jwt timeout
        token = self.jwt.create_access_token(encoded_data,
                                             timedelta(seconds=1))
        time.sleep(1)
        payload = self.jwt.verify_jwt(token)
        self.assertEqual(payload, None)

        # test2
        # test incorrect token
        payload = self.jwt.verify_jwt('error')
        self.assertEqual(payload, None)

        # test3
        # test correct token
        token = self.jwt.create_access_token(encoded_data)
        payload = self.jwt.verify_jwt(token)
        self.assertEqual(payload['username'], 'test_username')
        self.assertEqual(payload['email'], 'test_email')
        self.assertIsNotNone(payload['exp'])
