#필요한 함수 및 클래스를 임포트합니다.
import os
from http.client import HTTPConnection
from urllib.parse import urljoin, urlunparse
from urllib.request import urlretrieve
from html.parser import HTMLParser

#HTMLParser 클래스를 사용할 떄는 상속받는 클래스를 정의하고 필요한 내용을 오버라이드합니다.
class ImageParser(HTMLParser):
    #<img> 태그를 찾기 위하여 handle_starttag() 함수를 오버라이드합니다.
    def handle_starttag(self, tag, attrs):
        #<img src> 속성을 찾으면 속성값을 self.result 리스트에 추가합니다.
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)

#HTML 문장이 주어지면 ImageParser 클래스를 사용해서 이미지를 찾고, 그 이미지들을 DOWNLOAD 디렉토리에 다운로드.
def download_image(url, data):
    if not os.path.exists('DOWNLOAD'):
        os.makedirs('DOWNLOAD')

    #HTML 문장을 feed() 함수에 주면, 바로 파싱하고 그 결과를 parser.result 리스트에 추가합니다.
    parser = ImageParser()
    parser.feed(data)
    dataSet = set(x for x in parser.result) #파싱 결과를 set 타입의 dataSet으로 모아줍니다.

    #dataSet으로 모은 파싱 결과를 정렬한 후에 하나씩 처리합니다.
    for x in sorted(dataSet):
        #다운로드하기 위해 소스 URL과 타깃 파일명을 지정합니다.
        #소스 URL을 지정할 때 urljoin() 함수를 사용합니다.
        #urljoin()함수는 baseURL과 파일명을 합쳐서 완전한 URL을 리턴하는 함수입니다.
        imageUrl = urljoin(url, x)
        basename = os.path.basename(imageUrl)
        #이미지 파일을 다운로드하기 위해 urlretrieve() 함수를 사용합니다.
        #urlretrieve()함수는 src로부터 파일을 가져와서 targetFile 파일로 생성해줍니다.
        targetFile = os.path.join('DOWNLOAD',basename)

        print("Downloading...", imageUrl)
        urlretrieve(imageUrl, targetFile)

#프로그램의 시작점인 메인 함수로, www.google.co.kr 사이트를 검색해 이미지를 찾고 다운로드해주는 함수.
def main():
    host = "www.google.co.kr"

    #http.client 모듈을 사용해 구글 사이트에 접속한 후 첫 페이지 내용을 가져옵니다.
    #HTTPConnection() 함수의 인자는 host:post 형식.
    #port는 생략하면 디폴트로 80번 포트.
    conn = HTTPConnection(host)
    conn.request("GET",'')
    resp = conn.getresponse()

    #사이트에서 가져오는 데이터는 인코딩된 데이터이므로, 인코딩 방식을 알아내 디코딩해줍니다.
    charset = resp.msg.get_param('charset')
    data = resp.read().decode(charset)
    conn.close()

    print("\>>>>>>>>>>>>>> Download Images from", host)
    #다운로드 소스 URL을 지정하기 위해 urlunparse() 함수를 사용합니다.
    #urlunparse()함수는 urlparse()함수와 반대 기능으로 URL 요소 6개를 튜플로 받아 이를 조립해 완성된 URL을 리턴하는 함수.
    url = urlunparse(('http', host, '', '', '', ''))
    #이미지를 다운로드하기 위해 download_image() 함수를 호출
    download_image(url, data)

#프로그램을 시작하기 위해 main() 함수를 호출
if __name__ == '__main__':
    main()