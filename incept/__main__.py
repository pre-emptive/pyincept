from __future__ import print_function

import sys
import argparse
import os
import imp
import incept
import traceback

def main():
    # We pass any arguments beyond "--" to the application we call (which can do its own command line
    # processing with it).
    incept_args = sys.argv[1:]
    app_args = [sys.argv[0]]
    try:
        x = sys.argv.index('--')
    except ValueError:
        pass
    else:
        incept_args = sys.argv[1:x]
        app_args = [sys.argv[0]] + sys.argv[x+1:]
    sys.argv = app_args

    parser = argparse.ArgumentParser(description='Incept framework for non-UI Python applications')
    parser.add_argument('-d','--directory', help='Directory to change into before running', required=False)
    parser.add_argument('-b','--background', help='Daemonise into the background on startup', action="store_true")
    parser.add_argument('-p','--pidfile', help='Location to write a PID file')
    parser.add_argument('action', nargs='?', default='run', help='Action to take (run or init)')
    parser.add_argument('appname', nargs='?', default='app', help='Application name to run')
    parser.add_argument('-n','--procname', help='Change the process name to this (requires setproctitle)', required=False)
    args = parser.parse_args(incept_args)

    incept.prestart(args)

    if args.action == 'run':
        incept.start(args)

        appname = "./app/%s.py" % (args.appname)

        if args.procname:
            try:
                import setproctitle
                setproctitle.setproctitle(args.procname)
            except Exception as e:
                if incept.logging:
                    incept.logging.debug("Couldn't set the process name: %s" % (e))
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
                print("Uncaught Exception: %s: %s" % (type(e), e))
                traceback.print_exc()
        incept.end()
    elif args.action == 'init':
        incept.init()


if __name__ == '__main__':
    main()
