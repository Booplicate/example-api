"""
Test cases for the auth module
"""

import unittest
from unittest.mock import patch, MagicMock, AsyncMock

from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from example_api.auth import verify_credentials


class AsyncAuthTestCase(unittest.IsolatedAsyncioTestCase):
    """
    Test case for the auth module
    """
    async def test_verify_credentials(self):
        identifier = 5
        name = "Mock Name"
        password = "Mock Password"
        wrong_str = "wrong"

        def print_and_return(txt, rv):
            def inner():
                print(txt)
                return rv

            return inner

        mock_db_user = MagicMock()
        mock_db_user.identifier = identifier
        mock_db_user.name = name
        mock_db_user.password = password

        crdn = HTTPBasicCredentials(username=name, password=password)

        with patch("example_api.auth.new_session") as mock_sesh_factory:
            mock_sesh = MagicMock()
            mock_sesh.get = AsyncMock(return_value=None)# None means not found in the db
            mock_sesh_ctx_manager = AsyncMock(__aenter__=AsyncMock(return_value=mock_sesh))
            mock_sesh_factory.return_value = mock_sesh_ctx_manager

            with self.subTest("Test non-exiting user"):
                with self.assertRaises(HTTPException) as e:
                    await verify_credentials(identifier, crdn)

                self.assertEqual(e.exception.status_code, 404)

            mock_sesh.get.return_value = mock_db_user# Non-None means found in the db

            # This is so we don't need to actually compare string and hash
            verify_string_mock = lambda a, b: a==b

            with self.subTest("Test exiting user"):
                with patch("example_api.encoder.verify_string", verify_string_mock):
                    with self.subTest("Test full credentials match"):
                        await verify_credentials(identifier, crdn)

                    with self.subTest("Test wrong password"):
                        with patch.object(mock_db_user, "password", wrong_str):
                            with self.assertRaises(HTTPException) as e:
                                await verify_credentials(identifier, crdn)

                            self.assertEqual(e.exception.status_code, 401)

                    with self.subTest("Test wrong username"):
                        with patch.object(mock_db_user, "name", wrong_str):
                            with self.assertRaises(HTTPException) as e:
                                await verify_credentials(identifier, crdn)

                            self.assertEqual(e.exception.status_code, 401)
