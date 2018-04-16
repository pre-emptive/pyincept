#!/usr/bin/python

import incept
import sys
import argparse
import os
import imp

parser = argparse.ArgumentParser(description='Incept framework for non-UI Python applications')
parser.add_argument('-d','--directory', help='Directory to change into before running', required=False)
parser.add_argument('-b','--background', help='Daemonise into the background on startup', action="store_true")
parser.add_argument('-p','--pidfile', help='Location to write a PID file')
parser.add_argument('action', nargs='?', default='run', help='Action to take (run or init)')
parser.add_argument('appname', nargs='?', default='app', help='Application name to run')
args = parser.parse_args()

incept.prestart(args)

if args.action == 'run':
    incept.start(args)

    appname = "./app/%s.py" % (args.appname)

    try:
        import setproctitle
        setproctitle(appname)
    except:
        pass

    try:
        if incept.logging:
            incept.logging.debug("Loading Incept application '%s'" % (appname))
        app = imp.load_source('module_name', appname)
        app
    except Exception as e:
        if incept.logging:
            incept.logging.exception("Uncaught Exception: %s: %s" % (type(e), e))
        else:
            # TODO: Print out stacktrace here!
            print "Uncaught Exception: %s" % (e)
    incept.end()
elif args.action == 'init':
    incept.init()


