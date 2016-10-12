import sys, os
import uuid
import traceback

class HttpResponse():
    def __init__(self, code, header):
        self.code = code
        self.header = header
    def addHeader(self, head):
        self.header.append(head)
    def setCode(self, code):
        self.code = code

def application(environ, start_response):

    new_environ = environ

    # default return
    hr = HttpResponse('200 OK', [('Content-Type', 'text/html; charset=UTF-8')])

    # give minimal function
    new_environ['http_header'] = hr.addHeader
    new_environ['http_response'] = hr.setCode

    file = environ['SCRIPT_FILENAME']
    try:
        f = open(file,'r')
        data = f.read()
        f.close()
    except FileNotFoundError:
        start_response('404 not found', [('Content-Type', 'text/html')])
        content = 'File not found: ' + os.path.basename(file)
        return [content.encode('utf-8')]

    sid = uuid.uuid4().hex
    logout = open('/tmp/'+sid+'.out.log', 'w')
    sys.stdout = logout # hop, on hijack la sortie standard
    os.chdir(os.path.dirname(file))
    try:
        exec(data, new_environ)
    except Exception as e:
        res = str(e)
    else:
        logout.close()
        logout = open('/tmp/'+sid+'.out.log', 'r')
        res = logout.read()
        logout.close()
    finally:
        pass

    os.remove('/tmp/'+sid+'.out.log')
    start_response(hr.code, hr.header)
    return [res.encode('utf-8')]

