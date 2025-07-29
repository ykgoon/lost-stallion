import os
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from ichingshifa.ichingshifa import Iching

class IChingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        iching = Iching()

        if path == '/':
            # Generate a random hexagram (6-digit number)
            hexagram = iching.bookgua()
            self.send_response(302)
            self.send_header('Location', f'/{hexagram}')
            self.end_headers()

        elif path.startswith('/') and len(path) == 7 and path[1:].isdigit():
            # Display hexagram details
            hexagram_number = path[1:]
            try:
                result = iching.mget_bookgua_details(hexagram_number)
                explanation = result[4]
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open('templates/hexagram.html',
                          'r', encoding='utf-8') as f:
                    template = f.read()
                judgment = ''.join(f'<p>{item}</p>' for item in explanation)
                self.wfile.write(template.format(
                    hexagram=result[1],
                    judgment=judgment,
                ).encode('utf-8'))

            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write('無效的卦號'.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('頁面未找到'.encode('utf-8'))

def run(server_class=HTTPServer, handler_class=IChingHandler, port=4732):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Server running on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
