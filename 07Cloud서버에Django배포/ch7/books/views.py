#클래스형 제네릭 뷰를 사용하기 위해 임포트.
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
#테이블 조회를 위해 모델 클래스들을 임포트.
from books.models import Book, Author, Publisher

# Create your views here.

# TemplateView
#BooksModelView는 books 애플리케이션의 첫 화면을 보여주기 위한 뷰. 특별한 로직이 없고 템플릿 파일만을 렌더링하는 경우에는
#TemplateView 제네릭 뷰를 상속받아 사용하면 간단.
#TemplateView를 사용하는 경우에는 필수적으로 template_name 클래스 변수를 오버라이딩해서 지정해줘야 합니다.
#템플릿 시스템으로 넘겨줄 컨텍스트 변수가 있는 경우에는 get_context_data() 메소드를 오버라이딩해서 정의.
class BooksModelView(TemplateView):
    #books 애플리케이션의 첫 화면을 보여주기 위한 템플릿 파일을 books/index.html로 지정.
    template_name = 'books/index.html'

    def get_context_data(self, **kwargs):
        #get_context_data() 메소드를 정의할 때는 반드시 첫 줄에 super() 메소드를 호출해야 합니다.
        context = super().get_context_data(**kwargs)
        #books 애플리케이션의 첫 화면에 테이블 리스트를 보여주기 위해 컨텍스트 변수 model_list에 담아 템플릿 시스템에 넘겨줌.
        context['model_list'] = ['Book', 'Author', 'Publisher']
        #return도 필수.
        return context

# ListView
#ListView를 상속받는 경우는 객체가 들어있는 리스트를 구성해서 이를 컨텍스트 변수로 템플릿 시스템에 넘겨주면 된다.
#만일 이런 리스트를 테이블에 들어있는 모든 레코드를 가져와 구성하는 경우 모델 클래스명(테이블 명)만 지정해주면 된다.
#명시적으로 지정하지 않아도 장고에서 디폴트로 지정해주는 2가지 속성.
#첫번째는 컨텍스트 변수로 object_list를 사용하는 것이고, 두번째는 템플릿 파일을 모델명 소문자_list.html 형식의 이름으로 지정.
class BookList(ListView):
    #Book 테이블로부터 모든 레코드를 가져와 object_list라는 컨텍스트 변수를 구성.
    #템플릿 파일은 디폴트로 books/book_list.html 파일이 됩니다.
    model = Book

class AuthorList(ListView):
    #Author 테이블로부터 모든 레코드를 가져와 object_list라는 컨텍스트 변수를 구성합니다.
    #템플릿 파일은 디폴트로 books/author_list.html파일이 됩니다.
    model = Author

class PublisherList(ListView):
    #Publisher 테이블로부터 모든 레코드를 가져와 object_list라는 컨텍스트 변수를 구성합니다.
    #템플릿 파일은 디폴트로 books/publisher_list.html파일이 됩니다.
    model = Publisher

# DetailView
#DetailView를 상속받는 경우는 특정 객체 하나를 컨텍스트 변수에 담아 템플릿 시스템에 넘겨주면 됩니다.
#만일 테이블에서 Primary Key로 조회해서 특정 객체를 가져오는 경우에는 모델 클래스명만 지정해주면 됩니다.
#조회 시 사용할 Primary Key값은 URLconf에서 추출하여 뷰로 넘어온 파라미터를 사용.
#명시적으로 지정하지 않아도 장고에서 디폴트로 2가지 속성.
#첫 번째는 컨텍스트 변수로 object를 사용하는 것이고, 두 번째는 템플릿 파일을 모델명 소문자_detail.html형식의 이름으로 지정.
class BookDetail(DetailView):
    #Book 테이블로부터 특정 레코드를 가져와 object라는 컨텍스트 변수를 구성.
    #템플릿 파일은 디폴트로 books/book_detail.html 파일이 됩니다.
    #테이블 조회 조건에 사용되는 Primary Key값은 URLconf에서 넘겨받는데, 이에 대한 처리는 DetailView제네릭 뷰에서 자동으로.
    model = Book

class AuthorDetail(DetailView):
    #Author 테이블로부터 특정레코드를 가져와 object라는 컨텍스트 변수를 구성합니다.
    #템플릿 파일은 디폴트로 books/author_detail.html 파일이 됩니다.
    model = Author

class PublisherDetail(DetailView):
    #Publisher 테이블로부터 특정레코드를 가져와 object라는 컨텍스트 변수를 구성합니다.
    #템플릿 파일은 디폴트로 books/publisher_detail.html 파일이 됩니다.
    model = Publisher
