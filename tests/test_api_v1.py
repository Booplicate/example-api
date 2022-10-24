"""
Test cases for api endpoints
"""

import unittest
from unittest.mock import patch
import datetime
from contextlib import contextmanager

from fastapi.testclient import TestClient

from test_api.application import app_v1
from test_api import (
    database,
    models,
    auth
)


@contextmanager
def substitute_dependency(client, old, new):
    """
    Substitutes a dependency within client app
    """
    try:
        client.app.dependency_overrides[old] = new
        yield

    finally:
        client.app.dependency_overrides.pop(old, None)


def _generate_user_data():
    return {
        "identifier": 75,
        "name": "Mock User",
        "password": "Mock PW",
        "created_at": datetime.datetime(1970, 1, 1).isoformat()
    }

def _generate_db_user(from_data=None):
    if from_data is None:
        from_data = _generate_user_data()

    return database.User(**from_data)


async def create_db_user_mock(*args, **kwargs):
    return _generate_db_user()

async def update_db_user_valid_mock(*args, **kwargs):
    return _generate_db_user()

async def update_db_user_invalid_mock(*args, **kwargs):
    return None

async def get_db_user_valid_mock(*args, **kwargs):
    return _generate_db_user()

async def get_db_user_invalid_mock(*args, **kwargs):
    return None


async def verify_credentials_mock():
    return


class UsersEndpointTestCase(unittest.TestCase):
    """
    Test case for the users endpoint
    """
    ENDPOINT = "/users"

    def setUp(self):
        self.client = TestClient(app_v1)

    def tearDown(self):
        del self.client

    def test_create_user(self):
        with self.subTest("Test valid user"):
            with patch("test_api.services.create_user", create_db_user_mock):
                user_data = _generate_user_data()
                response = self.client.post(
                    self.ENDPOINT,
                    json=user_data
                )

                expected_user = models.UserModelOut.from_orm(_generate_db_user(user_data))
                returned_user = models.UserModelOut(**response.json())

                self.assertEqual(returned_user, expected_user)
                self.assertEqual(response.status_code, 201)

        with self.subTest("Test invalid user"):
            with patch("test_api.services.create_user", create_db_user_mock):
                response = self.client.post(
                    self.ENDPOINT,
                    json={}
                )

                self.assertEqual(response.status_code, 422)

    def test_update_user(self):
        with self.subTest("Test valid credentials"):
            with substitute_dependency(
                self.client,
                auth.verify_credentials,
                verify_credentials_mock
            ):
                with self.subTest("Test valid user"):
                    with patch("test_api.services.update_user", update_db_user_valid_mock):
                        user_data = _generate_user_data()
                        response = self.client.put(
                            self.ENDPOINT + "/75",
                            json=user_data
                        )

                        expected_user = models.UserModelOut.from_orm(_generate_db_user(user_data))
                        returned_user = models.UserModelOut(**response.json())

                        self.assertEqual(returned_user, expected_user)
                        self.assertEqual(response.status_code, 200)

                with self.subTest("Test invalid user"):
                    with patch("test_api.services.update_user", update_db_user_valid_mock):
                        response = self.client.put(
                            self.ENDPOINT + "/75",
                            json={}
                        )

                        self.assertEqual(response.status_code, 422)

                with self.subTest("Test non-existing user"):
                    with patch("test_api.services.update_user", update_db_user_invalid_mock):
                        response = self.client.put(
                            self.ENDPOINT + "/75",
                            json=_generate_user_data()
                        )

                        self.assertEqual(response.status_code, 404)

        with self.subTest("Test invalid credentials"):
            with patch("test_api.services.update_user", update_db_user_valid_mock):
                response = self.client.put(
                    self.ENDPOINT + "/75",
                    json=_generate_user_data()
                )

                self.assertEqual(response.status_code, 401)

    def test_get_user(self):
        with self.subTest("Test existing user"):
            with patch("test_api.services.get_user", get_db_user_valid_mock):
                response = self.client.get(
                    self.ENDPOINT + "/75"
                )
                expected_user = models.UserModelOut.from_orm(_generate_db_user())
                returned_user = models.UserModelOut(**response.json())

                self.assertEqual(returned_user, expected_user)
                self.assertEqual(response.status_code, 200)

        with self.subTest("Test non-existin user"):
            with patch("test_api.services.get_user", get_db_user_invalid_mock):
                response = self.client.get(
                    self.ENDPOINT + "/75"
                )

                self.assertEqual(response.status_code, 404)
