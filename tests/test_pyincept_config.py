import unittest

from pyincept import *

class TestInceptConfig(unittest.TestCase):

    def test_incept_config_instantion(self):
        obj = InceptConfig()
        self.assertIsInstance(obj, InceptConfig)

    def test_incept_config_load(self):
        obj = InceptConfig()
        self.assertNotEqual(obj.get(), {})
