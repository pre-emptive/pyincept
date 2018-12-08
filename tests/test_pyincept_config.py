import unittest

from incept import *

class TestInceptConfig(unittest.TestCase):

    def test_incept_config_instantion(self):
        obj = InceptConfig('./tests/config_fixtures')
        self.assertIsInstance(obj, InceptConfig)

    def test_incept_config_load(self):
        obj = InceptConfig('./tests/config_fixtures')
        self.assertNotEqual(obj.get(), {})
