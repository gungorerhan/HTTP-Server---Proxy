import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse
from SocketServer import ThreadingMixIn


class Handler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(400)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse.urlparse(self.path)
        # information about client
        message_parts = [
            'Thread Name=%s' % threading.current_thread().getName(),  # thread name
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
            'HEADERS RECEIVED:',
        ]
        for name, value in sorted(self.headers.items()):
            message_parts.append('%s=%s' % (name, value.rstrip()))
        message_parts.append('')
        message = '\r\n'.join(message_parts)
        print message

        try:
            temp = int(self.path[1:])  # remove '/'
            if temp < 100 or temp > 20000:
                self.respond({'status': 400})  # path is not between 100 - 20.000
        except:
            self.respond({'status': 400})  # path is not an integer
        else:
            self.respond({'status': 200})  # path is correct

    def handle_http(self, status_code, path):
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = ""
        if status_code == 400:  # return error
            content = "Bad Request"
        elif status_code == 200:  # return html file
            temp = ""
            for i in range(int(path[1:])):  # create body
                temp += "a"
            # create html file - 207 bytes except body
            content = '''   
                    <html>
                    <head>
                    <title>{}</title>
                    </head>
                    <body>{}</body>
                    </html>
                    '''.format(path[1:], temp)
        return content

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


if __name__ == '__main__':
    server = ThreadedHTTPServer(('localhost', 2000), Handler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
