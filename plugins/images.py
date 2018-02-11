from base import Plugin

class ImageTest(Plugin):
    extensions = ['jpg', 'thm', 'ppm', 'jpeg', 'tiff', 'bmp', 'eps', 'gif', 'im', 'msp', 'pcx', 'png']

    def executable(self):
        try:
            from PIL import Image
            return True
        except ImportError:
            pass

        self.log.info('Images will not be tested. Install PIL.');

        return False

    def test(self, file):
        try:
            im = Image.open(file)
            im.verify()
            return True
        except:
            pass

        self.log.warning('File ' + file + ' not valid image')

        return False
