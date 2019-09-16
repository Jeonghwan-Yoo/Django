#필요한 함수 및 클래스를 임포트합니다.
from urllib.request import urlopen
from html.parser import HTMLParser

#HTMLParser 클래스를 사용할 때는 상속받는 클래스를 정의하고, 필요한 내용을 오버라이드합니다.
class ImageParser(HTMLParser):
    #<img>태그를 찾기 위해 handle_starttag() 함수를 오버라이딩 합니다.
    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        if not hasattr(self, 'result'):
            self.result = []
        #<img src>속성을 찾으면 속성값을 self.result 리스트에 추가합니다.
        for name, value in attrs:
            if name == 'src':
                self.result.append(value)

#HTML 문장이 주어지면 HTMLParser 클래스를 사용해 이미지를 찾고, 그 리스트를 출력해주는 함수.
def parse_image(data):
    parser = ImageParser()
    parser.feed(data) #HTML문장을 feed()함수에 주면 바로 파싱하고 그 결과를 parser.result 리스트에 추가합니다.
    dataSet = set(x for x in parser.result) #파싱 결과를 set타입의 dataSet으로 모아줍니다.
    return dataSet #dataSet으로 모은 파싱 결과를 리턴합니다.

#프로그램의 시작점인 메인 함수로, www.google.co.kr 사이트를 검색해 이미지를 찾는 함수.
def main():
    url = "http://www.google.co.kr"

    #urllib.request모듈의 urlopen()함수를 사용해 구글 사이트에 접속한 후 첫 페이지 내용을 가져옵니다.
    with urlopen(url) as f:
        #사이트에서 가져오는 데이터는 인코딩된 데이터이므로, 인코딩 방식(charset)을 알아내 디코딩해줍니다.
        charset = f.info().get_param('charset')
        data = f.read().decode(charset)
    
    #이미지를 찾기 위해 parse_image()함수를 호출합니다.
    dataSet = parse_image(data)
    print("\>>>>>>>> Fetch Images from", url)
    print('\n'.join(sorted(dataSet))) #찾은 이미지들을 정렬하여 라인별로 출력합니다.

if __name__ == '__main__':
    main() #프로그램을 시작하기 위해 main()함수를 호출합니다.