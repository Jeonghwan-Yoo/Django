#장고의 단축함수인 render() 함수를 임포트합니다.
#장고의 단축함수인 get_object_or_404() 함수를 임포트.
from django.shortcuts import get_object_or_404, render
#리다이렉트 기능이 필요해, HttpResponseRedirect 클래스를 임포트.
from django.http import HttpResponseRedirect, HttpResponse
#url 처리를 위해 reverse() 함수를 임포트.
#from django.core.urlresolvers import reverse 이전 버전
from django.urls import reverse
#Question테이블에 액세스하기 위해 polls.models.Question 클래스를 임포트.

#클래스형 제네릭 뷰를 사용하기 위해 generic 모듈을 임포트.
from django.views import generic

from polls.models import Choice, Question

# logging 추가
#로깅을 위하여 파이썬의 logging 모듈을 임포트.
import logging
#getLogger(__name__)메소드를 호출해 polls.views 로거 객체를 취득합니다.
#__name__은 모듈 경로를 담고 있는 파이썬 내장 변수.
#views.py 파일의 모듈 경로는 polls.views이고, 사용하고자 하는 로거 객체의 이름.
#이 로거에서 생상한 로그 레코드는 상위 polls 로거에게 전파되고, polls로거에서 메시지를 기록합니다.
#이 동작을 위해 settings.py 파일에 polls 로거를 설정했다.
logger = logging.getLogger(__name__)

# Class-based GenericView
#IndexView 클래스는 ListView 제네릭 뷰를 사용.
#ListView를 상속받는 경우는 객체가 들어있는 리스트를 구성해서 이를 컨텍스트 변수로 템플릿 시스템에 넘겨주면 됩니다.
#만일 리스트를 테이블에 들어있는 모든 레코드를 가져와 구성하는 경우에는 모델 클래스명만 지정해주면 된다.
#그렇지 않은 경우는 get_queryset()메소드를 오버라이딩으로 정의해 원하는 리스트를 구성.
#템플릿 파일명과 컨텍스트 변수명은 디폴트 값을 사용할 수 있고, 명시적으로 지정해줄 수도 있다.
class IndexView(generic.ListView):
    #템플릿 파일명을 디폴트로 사용하지 않고, polls/index.html로 지정.
    template_name = 'polls/index.html'
    #컨텍스트 변수명을 디폴트로 사용하지 않고, latest_question_list로 지정.
    #ListView 사용 시 디폴트 컨텍스트 변수명은 object_list와 모델명 소준자를 사용한 question_list 둘다 가능.
    context_object_name = 'latest_question_list'

    #처리 대상 객체 리스트를 구성하기 위해 get_queryset() 메소드를 오버라이딩해서 정의.
    #Question 테이블에서 pub_date 칼럼 기준으로 최신 5개를 조회하여 리스트를 구성.
    def get_queryset(self):
        #최근 생성된 질문 5개를 반환함
        return Question.objects.order_by('-pub_date')[:5]

#DetailView 클래스는 DetailView 제네릭 뷰를 사용하고 있습니다.
#DetailView를 상속받는 경우는 특정 객체 하나를 컨텍스트 변수에 담아 템플릿 시스템에 넘겨주면 됩니다.
#만일 특정 객체를 테이블에서 Primary Key로 조회해서 가져오는 경우에는 모델 클래스명만 지정.
#테이블 조회 조건에 사용되는 Primary Key 값은 URLconf에서 pk라는 파라미터 이름으로 넘겨받는데, 제네릭 뷰에서 알아서 처리.
#컨텍스트 변수명과 템플릿 파일명은 디폴트 값을 사용할 수도 있고, 명시적으로 지정해줄 수도 있다.
class DetailView(generic.DetailView):
    #Question 테이블로부터 특정 레코드를 가져와 컨텍스트 변수를 구성.
    #컨텍스트 변수명은 디폴트 값을 사용하며, object와 모델명 소문자인 question, 둘다 가능.
    model = Question
    #템플릿 파일명을 디폴트로 사용하지 않고, polls/detail.html로 지정해주고 있다.
    template_name = 'polls/detail.html'

#ResultViews 클래스는 DetailView 제네릭 뷰를 사용하고 있습니다.
#유의할 점은 템플릿 시스템에 넘겨주는 객체는 Choice 객체가 아닌 Question 객체.
#즉 특정 Question 객체를 구해서 해당 객체와 ForeignKey로 연결된 Choice 객체들을 구하는 로직.
#이 로직은 results.html 템플릿 파일에서 question.choice_set.all() 구문으로 구현.
class ResultsView(generic.DetailView):
    #Question 테이블로부터 특정 레코드를 가져와 컨텍스트 변수를 구성.
    #컨텍스트 변수명은 디폴트 값을 사용하며, object와 모델명 소문자인 question 둘다 가능.
    model = Question
    #템플릿 파일명을 디폴트로 사용하지 않고, polls/results.html로 지정.
    template_name = 'polls/results.html'

# Funtion-based View
def vote(request, question_id):
    #로거 객체의 debug() 메소드를 호출해 로거에게 DEBUG 수준으로 로그 레코드를 생성하도록 요청.
    #settings.py 로깅 설정에 따라, file 핸들러를 사용해 ch5\logs\mysite.log 파일에 로그 메시지를 기록.
    logger.debug("vote().question_id:%s" %question_id) # 추가
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 설문 투표 폼을 다시 보여준다.
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_mesage':"You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST 데이터를 정상적으로 처리했으면 항상 HttpResponseRedirect를 반환하여 리다이렉션 처리.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

'''
# Create your views here.
#뷰 함수를 정의합니다. request객체는 뷰 함수의 필수 인자입니다.
def index(request):
    #템플릿에게 넘겨줄 객체의 이름은 latest_question_list입니다.
    #latest_question_list객체는 Question 테이블 객체에서 pub_date칼럼의 역순으로 정렬하여 5개의 최근 Question객체를
    #가져와서 만듭니다.
    latest_question_list = Question.objects.all().order_by('-pub_date')[:5]
    #render() 함수는 템플릿 파일인 polls/index.html에 context 변수를 적용하여 사용자에게 보여줄 최종 HTML 텍스트를 만들고,
    #이를 담아서 HttpResponse 객체를 반환합니다.
    context = {'latest_question_list':latest_question_list}
    #index() 뷰 함수는 최종적으로 클라이언트에게 응답할 데이터인 HttpResponse 객체를 반환합니다.
    return render(request, 'polls/index.html', context)

#뷰 함수를 정의합니다. request객체는 필수 인자이고, 추가적으로 question_id인자를 더 받습니다.
#URL패턴에서 정규표현식으로 추출한 question_id 파라미터가 뷰 함수의 인자로 넘어오는 것.
#path('polls/<int:question_id>/', views.detail, name='detail'),
def detail(request, question_id):
    #이 함수의 첫 번째 인자는 모델 클래스이고, 두 번째인자부터는 검색 조건을 여러 개 사용할 수 있습니다.
    #Qusetion모델 클래스로부터 pk=question_id검색 조건에 맞는 객체를 조회합니다.
    #조건에 맞는 객체가 없으면 Http404 익셉션을 발생시킵니다.
    question = get_object_or_404(Question, pk=question_id)
    #polls/detail.html에 컨텍스트 변수를 적용하여 사용자에게 보여줄 최종 HTML 텍스트를 만들고, 이를 담아 HttpResponse
    #객체를 반환합니다.
    #템플릿에게 넘겨주는 컨텍스트 사전을 render() 함수의 인자로 직접 써주고 있고, 템플릿 파일에서는 question이란
    #변수를 사용할 수 있게 되었습니다.
    #detail()뷰 함수는 최종적으로 detail.html의 텍스트 데이터를 담은 HttpResponse 객체를 반환합니다.
    return render(request, 'polls/detail.html', {'question':question})

#뷰 함수를 정의합니다. request 객체는 필수 인자이고, question_id인자를 더 받습니다.
#path('polls/<int:question_id>/vote/', views.vote, name='vote'),
#이 라인에 의해 vote() 뷰 함수로 인자가 넘어옵니다.
def vote(request, question_id):
    #Choice 테이블을 검색하고 있습니다.
    #검색 조건은 pk=request.POST['choice']입니다.
    #request.POST는 제출된 폼의 데이터를 담고 있는 객체로서, 파이썬 사전처럼 키로 그 값을 구할 수 있습니다.
    #request.POST['choice']는 폼 데이터에서 키가 'choice'에 해당하는 값인 choice.id를 스트링으로 리턴합니다.
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #폼의 POST 데이터에서 'choice'라는 키가 없으면 KeyError 익셉션을 발생시킵니다.
    #또는 검색 조건에 맞는 객체가 없으면 Choice.DoesNotExist 익셉션이 발생.
    except (KeyError, Choice.DoesNotExist):
        #설문 투표 폼을 다시 보여준다.
        #익셉션이 발생하면 render() 함수에 의해 question과 error_message컨텍스트 변수를 detail.html템플릿으로 전달.
        #그 결과 사용자에게는 에러 메시지와 함께 질문 항목 폼을 다시 보여줘서 데이터를 재입력할 수 있도록 합니다.
        return render(request, 'polls/detail.html', {
            'question':question,
            'error_message':"You didn't select a choice",
        })
    #익셉션이 발생하지 않고 정상 처리하는 경우.
    else:
        #Choice 객체.votes 속성, 즉 선택 카운트를 +1 증가시킵니다.
        selected_choice.votes += 1
        #변경사항을 해당 Choice 테이블에 저장합니다.
        selected_choice.save()
        #POST 데이터를 정상적으로 처리하였으면,
        #항상 HttpResponseRedirect를 반환하여 리다이렉션 처리함
        #vote() 뷰 함수가 반환하는 객체는 HttpResponse가 아닌 HttpResponseRedirect입니다.
        #HttpResponseRedirect 객체의 생성자는 리다이렉트할 타겟 URL을 인자로 받습니다.
        #타겟 URL은 reverse() 함수로 만듭니다.
        #최종적으로 vote() 뷰 함수는 리다이렉트할 타겟 URL을 담은 HttpResponseRedirect 객체를 반환합니다.
        #웹 프로그램에서 POST 방식의 폼 데이터를 처리하는 경우, 그 결과를 보여줄 수 있는 페이지로 이동시키기 위해
        #HttpResponseRedirect 객체를 리턴하는 것이 일반적.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

#뷰 함수를 정의합니다. 첫 번째 request객체는 필수 인자이고, 두 번째 question_id인자는 다음 라인의 실행 결과로 넘어옴.
#path('polls/<int:question_id>/results/', views.resultsm name='results'),
def results(request, question_id):
    #get_object_or_404() 단축함수를 사용.
    #Question 모델 클래스로부터 pk=question_id 검색 조건에 맞는 객체를 조회합니다.
    #조건에 맞는 객체가 없으면 Http404 익셉션을 발생시킵니다.
    question = get_object_or_404(Question, pk=question_id)
    #question변수를 넘겨주는 것은 동일하지만 템플릿 파일이 다르므로, 사용자에게 보여주는 화면은 달라집니다.
    #results() 뷰 함수는 최종적으로 results.html 템플릿 코드를 랜더링한 결과인 HTML 텍스트 데이터를 담은
    #HttpResponse 객체를 반환합니다.
    return render(request, 'polls/results.html', {'question':question})
'''