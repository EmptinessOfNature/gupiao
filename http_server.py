from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 解析请求的URL
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        # 读取数据长度
        content_length = int(self.headers['Content-Length'])
        # 读取POST数据
        post_data = self.rfile.read(content_length)

        # 假设POST数据是JSON，尝试解析它
        try:
            input = json.loads(post_data)

            if path == "/":
                self.handle_root()
            elif path == "/duanxian":
                pass
        except json.JSONDecodeError:
            self.to_response("Bad Request:" + post_data, 400)
            return

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run(handler_class=SimpleHTTPRequestHandler)