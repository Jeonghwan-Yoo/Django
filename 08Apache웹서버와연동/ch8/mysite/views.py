#클래스형 제네릭 뷰를 사용하기 위해 TemplateView 클래스를 임포트.
from django.views.generic.base import TemplateView
from django.apps import apps #추가

# Template
#Template 제네릭 뷰를 상속. TemplateView를 사용하면 필수적으로 template_name 클래스 변수를 오버라이딩해야 합니다.
#템플릿 시스템으로 넘겨줄 컨텍스트 변수가 있는 경우에는 get_context_data() 메소드를 오버라이딩해서 정의.
class HomeView(TemplateView):
    #mysite 프로젝트의 첫 화면을 보여주기 위한 템플릿 파일.
    #템플릿 파일이 위치하는 디렉토리는 settings.py 파일의 TEMAPLATES 항목에 리스트 요소로 추가되어 있다.
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        #get_context_data() 메소드를 정의할 때는 반드시 첫 줄에 super() 메소드 호출.
        context = super().get_context_data(**kwargs) 
        #mysite 프로젝트 하위에 있는 애플리케이션들의 리스트를 보여주기 위해 컨텍스트 변수 app_list에 담아 템플릿 시스템에 전달.
        #context['app_list'] = ['polls', 'books'] #이 라인 대신 아래 5라인 추가
        dictVerbose = {}
        #장고가 제공하는 apps 객체의 get_app_configs() 메소드를 호출하면 settings.py 파일의 INSTALLED_APPS에 등록된
        #각 앱의 설정 클래스들을 담은 리스트를 반환합니다. for 문장으로 각 설정 클래스들을 순회.
        for app in apps.get_app_configs():
            #app은 각 앱의 설정 클래스를 의미하므로, app.path는 각 설정 클래스의 path 속성으로, 애플리케이션 디렉토리의
            #물리적 경로를 뜻함. 예를 들어 books 앱의 물리적 경로는 ~ch5\books.
            #물리적 경로에 site-packages 문자열이 들어있으면 외부 라이브러리 앱을 의미하므로, if문장에서 제외.
            if 'site-packages' not in app.path:
                #설정 클래스의 label속성값을 키로 verbose_name 속성값을 값으로해서, dictVerbose 사전에 담습니다.
                #books 앱의 경우, label은 books이고 verbose_name은 Book-Author-Publisher App입니다.
                dictVerbose[app.label] = app.verbose_name
        #for 문장이 완료된 후에, verbose_dict 컨텍스트 변수에 dictVerbose 사전을 대입.
        context['verbose_dict'] = dictVerbose
        #return 문장 필수.
        return context
