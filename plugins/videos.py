from base import Plugin

import os
import re

class VideoTest(Plugin):
    extensions = ['mp4', 'avi', 'mov', 'mts', '3gp']

    def executable(self):
        t = os.popen('ffmpeg 2>&1').read()

        if t.startswith('ffmpeg version'):
            return True

        self.log.info('ffmpeg is not in path, video files will not be tested.')
        return False

    def test(self, file):
        try:
            t = os.popen('ffmpeg -v error -i "%s" -f null - 2>&1' % file).read()
            t = re.sub(r"frame=.+?\r", "", t)
            t = re.sub(r"\[(.+?) @ 0x.+?\]", "[\\1]", t)

            if len(t) > 0:
                self.log.debug(t)
                raise "error"

            return True
        except:
            self.log.warning('File ' + file + ' not valid video')

        return False
