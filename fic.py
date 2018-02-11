#!/usr/bin/env python3
import argparse
import os
import sys
import inspect
from stat import *
import logging
import shutil
import importlib

logging.basicConfig(level = logging.INFO)

class Logger:

    def __init__(self):
        pass

    def debug(self, message):
        logging.debug(message)

    def info(self, message):
        logging.info(message)

    def error(self, message):
        logging.error(message)

    def warning(self, message):
        logging.warning(message)

log = Logger()

class FileIntegrityCheck:

    def __init__(self, args):
        self.args = args
        self.filePlugins = []


        for module in os.listdir(os.path.dirname(__file__) + '/plugins'):
            if module != 'base.py' and module.endswith('.py'):
                importlib.import_module('plugins.' + module[:-3])

        for name, obj in inspect.getmembers(sys.modules['plugins']):
            for k, v in inspect.getmembers(obj):
                try:
                    bases = [b.__name__ for b in v.__bases__]

                    if 'Plugin' not in bases:
                        continue

                except AttributeError:
                    continue

                o = v({'log': log})

                if not hasattr(o, 'executable') or o.executable():
                    self.filePlugins.append(o)

    def run(self):
        files = self.args.files

        if files is None:
            log.error("Target was not specified")
            sys.exit(1)

        if os.path.isfile(files):
            self.testFile(files)
        elif os.path.isdir(files):
            self.testDirectory(files)
        else:
            log.error("Target can not be tested, not file or directory")

    def testDirectory(self, directory):
        for f in os.listdir(directory):
            pathname = os.path.join(directory, f)
            mode = os.stat(pathname)[ST_MODE]
            if S_ISDIR(mode):
                self.testDirectory(pathname)
            elif S_ISREG(mode):
                self.testFile(pathname)
            else:
                # Unknown file type, print a message
                log.info('Skipping "%s"' % pathname)

    def testFile(self, path):
        log.debug('Test: ' + path)
        tested = False
        for plugin in self.filePlugins:
            if plugin.usable(path):
                if not plugin.test(path) and self.args.alternatives:
                    # try to fix
                    altpath = self.args.alternatives + path[len(self.args.files):]
                    if os.path.isfile(altpath) and plugin.test(altpath):
                        if self.args.fix:
                            log.warning('File "%s" is available in alternatives, fixing ' % path)
                            shutil.copy(altpath, path)
                        else:
                            log.warning('File "%s" is available in alternatives ' % path)

                tested = True

        if not tested:
            log.info('File "' + path + '" skipped')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Check file or directory')
    parser.add_argument('--files', help='file or directory')
    parser.add_argument('--alternatives', help='file or directory for fixing')
    parser.add_argument('--fix', action='store_true', help='Fix files from alternatives')

    args = parser.parse_args()

    checker = FileIntegrityCheck(args)
    checker.run()
