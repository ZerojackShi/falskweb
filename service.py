import win32serviceutil
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all()
import ssl
import threading
from web import app
import os
class Service(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyFlaskService"
    _svc_display_name_ = "FlaskService"
    _svc_description_ = "flask gevent service test description"

    def __init__(self, *args):
        super().__init__(*args)
        self.http_server = WSGIServer(('127.0.0.1', 5173), app)

    def SvcDoRun(self):
        os.chdir("D:\ProjackSpace\cracktest")
        thread = threading.Thread(target=self.http_server.serve_forever)
        thread.start()
        thread.join()

    def SvcStop(self):
        self.http_server.stop()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(Service)
