import os
import time
import unittest
from datetime import timedelta


class TestMiddlewareJwt(unittest.TestCase):

    def setUp(self) -> None:
        os.environ['JWT_SECRET_KEY'] = 'test'
        from blackjack.controller.middleware.jwt import JWT
        self.jwt = JWT()

    def test_jwt(self):
        encoded_data = {
            'username': 'test_username',
            'email': 'test_email',
        }
        token = self.jwt.create_access_token(encoded_data,
                                             timedelta(seconds=1))
        time.sleep(1)
        print(time.time())
        payload = self.jwt.verify_jwt(token)
        self.assertEqual(payload, None)

        # TODO
        # test incorrect token
