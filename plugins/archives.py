from base import Plugin

class ZipTest(Plugin):
    extensions = ['zip']

    def executable(self):
        try:
            import zipfile
            return True
        except ImportError:
            pass

        self.log.info('ZIP files will not be tested. Install zipfile module.');
        return False

    def test(self, file):
        try:
            z = zipfile.ZipFile(file)

            if z.testzip() is not None:
                raise "Error"

            return True

        except:
            self.log.warning('File ' + file + ' not valid video')

        return False
