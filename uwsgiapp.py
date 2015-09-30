import sys, os
import uuid
import traceback

def application(environ, start_response):

    """
    yield '<h1>FastCGI Environment</h1>'
    yield '<table>'
    for k, v in sorted(environ.items()):
         yield '<tr><th>{0}</th><td>{1}</td></tr>'.format(k,v)
    yield '</table>'
    """

    file = environ['SCRIPT_FILENAME']
    try:
        f = open(file,'r')
        data = f.read()
        f.close()
    except FileNotFoundError:
        start_response('404 not found', [('Content-Type', 'text/html')])
        content = 'file not found: ' + file
        return [content.encode('utf-8')]

    sid = uuid.uuid4().hex
    logout = open('/tmp/'+sid+'.out.log', 'w')
    sys.stdout = logout # hop, on hijack la sortie standard
    try:
        exec(data, environ, {})
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
    start_response('200 OK', [('Content-Type', 'text/html; charset=UTF-8')])
    return [res.encode('utf-8')]



def oldapplication(environ, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    dis = '<h1>FastCGI Environment</h1>'
    dis +=  '<table>'
    for k, v in sorted(environ.items()):
         dis += '<tr><th>{0}</th><td>{1}</td></tr>'.format(k,v)
    dis += '</table>'
    return [dis.encode('utf-8')]

