import os
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from ichingshifa.ichingshifa import Iching

TRIGRAM_SYMBOLS = {
    '乾': '☰',
    '兌': '☱',
    '離': '☲',
    '震': '☳',
    '巽': '☴',
    '坎': '☵',
    '艮': '☶',
    '坤': '☷'
}

def map_trigram(digits):
    """Map a 3-digit sequence to a trigram name."""
    # Convert each digit to yin (0) or yang (1):
    # 6 = old yin, 7 = young yang, 8 = young yin, 9 = old yang
    # For trigram identification, we care about yin/yang regardless of age
    binary = ''.join(['1' if d in '79' else '0' for d in digits])

    # Map binary representation to trigram names
    trigram_map = {
        '111': '乾',  # Heaven
        '110': '兌',  # Lake
        '101': '離',  # Fire
        '100': '震',  # Thunder
        '011': '巽',  # Wind
        '010': '坎',  # Water
        '001': '艮',  # Mountain
        '000': '坤'   # Earth
    }
    return trigram_map.get(binary, '未知')

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

                # Split hexagram into upper and lower trigrams
                lower_digits = hexagram_number[0:3]
                upper_digits = hexagram_number[3:6]
                lower_trigram_name = map_trigram(lower_digits)
                upper_trigram_name = map_trigram(upper_digits)

                # Get symbols for trigrams
                lower_trigram_symbol = TRIGRAM_SYMBOLS.get(
                    lower_trigram_name, '')
                upper_trigram_symbol = TRIGRAM_SYMBOLS.get(
                    upper_trigram_name, '')

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
                    lower_trigram_name=lower_trigram_name,
                    lower_trigram_symbol=lower_trigram_symbol,
                    upper_trigram_name=upper_trigram_name,
                    upper_trigram_symbol=upper_trigram_symbol,
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
