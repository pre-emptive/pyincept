import logging as logging_obj
import logging.config as l_c

class InceptLogging(object):
    logging = None

    def __init__(self, configdata):
        l_c.dictConfig(configdata['logging'])
        InceptLogging.logging = logging_obj
