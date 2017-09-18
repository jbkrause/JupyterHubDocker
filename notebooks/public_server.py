#!/usr/bin/python3
import tornado.ioloop
import tornado.web
import re
import os
import sys
#import glob
import mimetypes
#import shutil

if len(sys.argv)==1:
    served_folder = '/persistent/Share'
else:
    served_folder = sys.argv[1] # give absolute path

class MainHandler(tornado.web.RequestHandler):
    def get(self, path):
        fspath = '%s/%s' % (served_folder, path)
        print(fspath)
        if os.path.isfile(fspath):
            if fspath.endswith(".ipynb"):
                self.download(fspath, mime_type="text/plain")
            else:
                self.download(fspath, mime_type=None)
        elif os.path.isdir(fspath):
            self.write("%s is a directory" % (fspath,))
        else: # not a file, but a directory, FIXME : zip it
            self.write("%s does not exist" % (fspath,))

    def download(self, fspath, mime_type=None):

        if os.path.exists(fspath):
            if mime_type is None:
                mime_type, encoding = mimetypes.guess_type(fspath)
            if mime_type is None:
                mime_type = "text/plain"
            base_filename = os.path.basename(fspath)
            self.set_header('Content-Type', mime_type)
            self.set_header('Content-Disposition', 'attachment; filename="%s"' % base_filename)
            fp = open(fspath, "rb")
            try:
                self.write(fp.read())
            except:
                print("IO error reading: " + fspath)
            finally:
                fp.close()
        else:
            raise web.HTTPError(404)

def make_app():
    return tornado.web.Application([
        (r"/(.*)", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(80)
    print('starting tornado :)')
    tornado.ioloop.IOLoop.current().start()
