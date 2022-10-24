"""
Test cases for the encoder sub module
"""

import unittest

from example_api import encoder


class EncoderTestCase(unittest.TestCase):
    """
    Test case for the encoder sub module
    """
    def test_hash_string(self):
        test_string = "hello world"
        self.assertNotEqual(encoder.hash_string(test_string), test_string)

    def test_verify_string(self):
        test_string = "hello world"
        wrong_string = "goodbye world"
        hashed_string = encoder.hash_string(test_string)

        self.assertTrue(
            encoder.verify_string(test_string, hashed_string)
        )
        self.assertFalse(
            encoder.verify_string(wrong_string, hashed_string)
        )
