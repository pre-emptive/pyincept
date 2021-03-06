from __future__ import print_function

from .inceptconfig import InceptConfig
from .inceptlogging import InceptLogging

import os
import shutil, errno
import site

logging = None
pidfile = None
config = None
config_data = None
daemon_context = None
database_engine = None
database = None
redis = None
rabbitmq = None

# This mostly from https://stackoverflow.com/a/13696380
def _get_filenos_from_logging(logging):
    filenos = []
    for handler in logging.root.handlers:
        try:
            filenos.append(handler.stream.fileno())
        except:
            try:
                filenos.append(handler.socket.fileno())
            except:
                pass
    return filenos

def prestart(args):
    if args.directory:
        os.chdir(args.directory)

# I can't beleive there's not a library to do this easily
def _rcopy(src, dest):
    for item in os.listdir(src):
        if item == '.exists':
            continue
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            try:
                os.makedirs(d)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            _rcopy(s, d)
        else:
            if os.path.isfile(d):
                print("Warning: Not overwriting existing file %s" % (d))
            else:
                shutil.copy(s, d)


def init():
    module_path = os.path.dirname(__file__)
    _rcopy("%s/skel" % (module_path), ".")
    print("Incept project initialised")

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

# get going...
def start(args, **todo_options):

    todo = {
        'directory': True,
        'logging': True,
        'daemonise': True,
        'redis': True,
        'database': True,
        'rabbitmq': True,
    }

    for item in todo_options.keys():
        if item in todo:
            todo[item] = todo_options[item]

    if isinstance(args, dict):
        args = AttrDict(args)

    config_obj = InceptConfig()
    global config_data
    config_data = config_obj.get()

    if todo['directory']:
        if args.directory:
            working_directory = args.directory
        else:
            working_directory = os.getcwd()

        site.addsitedir(working_directory)

    if todo['logging']:
        if 'logging' in config_data:
            global logging
            logging_obj = InceptLogging(config_data)
            logging = logging_obj.logging

            _get_filenos_from_logging(logging)

    if todo['daemonise']:
        # daemonise if required to do so
        if args.background:
            import daemon
            import daemon.pidfile
            daemon_args = {}
            daemon_args['working_directory'] = working_directory
            if args.pidfile:
                daemon_args['pidfile'] = daemon.pidfile.PIDLockFile(args.pidfile)

            if 'logging' in config_data:
                # preserve any files opened by logging
                # this won't preserve STDOUT/STDERR, even if
                # logging said to use them.
                daemon_args['files_preserve'] = _get_filenos_from_logging(Incept.logging)

            global daemon_context
            daemon_context = daemon.DaemonContext(**daemon_args)
            daemon_context.open()

    if todo['redis']:
        if 'redis' in config_data:
            import redis
            global redis
            redis = redis.Redis(**config_data['redis'])
            redis.ping()

    if todo['database']:
        if 'database' in config_data:
            from sqlalchemy import create_engine
            db_config = {}
            for key, value in config_data['database'].items():
                if key not in ['url']:
                    db_config[key] = value
            global database_engine
            global database
            database_engine = create_engine(config_data['database']['url'], **db_config)
            database = database_engine.connect()

    if todo['rabbitmq']:
        if 'rabbitmq' in config_data:
            import pika
            for required in ['username', 'password', 'host']:
                if required not in config_data['rabbitmq']:
                    raise KeyError('%s not in RabbitMQ config' % (required))
            credentials = pika.PlainCredentials(config_data['rabbitmq']['username'],
                                                config_data['rabbitmq']['password'])
            try:
                vhost = config_data['rabbitmq']['vhost']
            except KeyError:
                vhost = '/'
            parameters = pika.ConnectionParameters(
                host=config_data['rabbitmq']['host'],
                credentials=credentials,
                virtual_host=vhost
            )
            global rabbitmq
            rabbitmq = pika.BlockingConnection(parameters)


def end():
    global daemon_context
    if daemon_context:
        daemon_context.close()

