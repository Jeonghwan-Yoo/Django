#장고의 단축함수인 render() 함수를 임포트합니다.
#장고의 단축함수인 get_object_or_404() 함수를 임포트.
from django.shortcuts import get_object_or_404, render
#리다이렉트 기능이 필요해, HttpResponseRedirect 클래스를 임포트.
from django.http import HttpResponseRedirect, HttpResponse
#url 처리를 위해 reverse() 함수를 임포트.
#from django.core.urlresolvers import reverse 이전 버전
from django.urls import reverse
#Question테이블에 액세스하기 위해 polls.models.Question 클래스를 임포트.
from polls.models import Choice, Question

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