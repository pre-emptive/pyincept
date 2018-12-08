import unittest
import logging

from incept import *

dictconfig = {
    'version': 1,
    'disable_existing_loggers': False,  # this fixes the problem
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level':'INFO',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

class TestInceptLogging(unittest.TestCase):

    def test_incept_logging(self):
        l = InceptLogging({ 'logging': dictconfig })
        self.assertIsInstance(l, InceptLogging)

