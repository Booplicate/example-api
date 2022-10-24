"""
Test cases for the services sub module
"""

import unittest
import datetime

from example_api import services


class ServicesTestCase(unittest.TestCase):
    """
    Test case for the services sub module
    TODO: create_user and get_user could be tested using a mock sqlite db,
        but update_user utilises RETURNING which only works in postgre
    """
    def test_preprocess_user_data(self):
        og_password = "secret!"
        data = {"password": og_password}
        services._preprocess_user_data(data)

        self.assertNotEqual(data["password"], og_password)

    def test_preprocess_new_user_data(self):
        password = "secret!"
        date = datetime.datetime(1999, 9, 22)
        data = {"password": password}
        services._preprocess_new_user_data(data, now_utc_dt=date)

        self.assertNotEqual(data["password"], password)
        self.assertEqual(data["created_at"], date)
