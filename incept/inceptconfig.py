from __future__ import print_function

import yaml
import os
import sys

class InceptConfig(object):
    def __init__(self, configpath = "./config", force = False, failonerror = False):
        self.config_loaded = False
        self.config_data = {}
        self.load(configpath, force, failonerror)

    def load(self, configpath = "./config", force = False, failonerror = False):
        if self.config_loaded and not force:
            return True
        try:
            files = os.listdir(configpath)
        except OSError as e:
            print("Could not load config: %s" % (e))
            if failonerror:
                sys.exit(1)
            else:
                return False

        for fname in os.listdir(configpath):
            if not fname.endswith(".yml"):
                continue
            path = os.path.join(configpath, fname)
            if not os.path.isfile(path):
                print("Not a file: %s" % (path))
                continue
            with open(path) as stream:
                try:
                    lump = yaml.safe_load(stream)
                    # skip if the yaml was empty (or all comments)
                    if not lump:
                        continue
                    # Put the lump of config into a key with the same
                    # name as the file we got it from
                    key = os.path.splitext(fname)[0]
                    self.config_data.update({ key: lump })
                except yaml.YAMLError as e:
                    print("Error reading %s: %s" % (path, e))
                    if failonerror:
                        sys.exit(1)
        self.config_loaded = True
        return True

    def get(self):
        try:
            return self.config_data
        except:
            return None

