#http.server 모듈을 임포트합니다.
from http.server import HTTPServer, BaseHTTPRequestHandler

#BaseHTTPRequestHandler를 상속받아, 원하는 로직으로 핸들러 클래스를 정의합니다.
class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response_only(200, 'OK')
        self.send_header('Content_Type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"Hello World")

if __name__ == '__main__':
    #서버의 IP, PORT 및 핸들러 클래스를 인자로 하여 HTTPServer 객체를 생성합니다.
    server = HTTPServer(('', 8888), MyHandler)
    print("Started WebServer on port 8888...")
    print("Press ^C to quit WebServer.")
    #HTTPServer 객체의 serve_forever() 메소드를 호출합니다.
    server.serve_forever()
