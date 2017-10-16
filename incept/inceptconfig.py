import yaml
import os
import sys

class InceptConfig(object):
    def __init__(self):
        self.config_loaded = False
        self.config_data = {}
        self.load()

    def load(self, configpath = "./config", force = False, failonerror = False):
        if self.config_loaded and not force:
            return True
        try:
            files = os.listdir(configpath)
        except OSError as e:
            print "Could not load config: %s" % (e)
            if failonerror:
                sys.exit(1)
            else:
                return False

        for fname in os.listdir(configpath):
            if not fname.endswith(".yml"):
                continue
            path = os.path.join(configpath, fname)
            if not os.path.isfile(path):
                continue
            try:
                lump = yaml.safe_load(open(path))
                # Put the lump of config into a key with the same
                # name as the file we got it from
                key = os.path.splitext(fname)[0]
                if lump != None:
                    self.config_data.update({ key: lump })
            except Exception as e:
                print "Error reading %s: %s" % (path, e)
                if failonerror:
                    sys.exit(1)
        self.config_loaded = True
        return True

    def get(self):
        try:
            return self.config_data
        except:
            return None

