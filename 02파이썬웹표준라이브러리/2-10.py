from http.client import HTTPConnection
from urllib.parse import urlencode

host = '127.0.0.1:8000'
#POST 요청으로 보낼 파라미터에 대해 URL 인코딩을 합니다.
params = urlencode({
    'language':'python',
    'name':'김석훈',
    'email':'shkim@naver.com',
})
#POST 요청으로 보낼 헤더를 사전 타입으로 지정합니다.
headers = {
    'Content-Type':'application/x-www-form-urlencoded',
    'Accept':'text/plain',
}
#127.0.0.1 사이트의 8000번 포트에 접속을 준비합니다.
#HTTPConnection() 클래스 생성 시, 첫 번째 인자는 url이 아니라 host입니다. http://는 쓰지 않습니다.
conn = HTTPConnection(host)
#POST 방식임을 명시적으로 표현하고, 파라미터와 헤더를 같이 보냅니다.
#request(method, url, body, headers) 형식이며, method, url 인자는 필수고, body, headers 인자는 옵션.
conn.request('POST','',params,headers)
resp = conn.getresponse()
print(resp.status, resp.reason)

data = resp.read()
#서버로부터의 응답 결과를 확인합니다.
print(data.decode('utf-8'))

conn.close()
