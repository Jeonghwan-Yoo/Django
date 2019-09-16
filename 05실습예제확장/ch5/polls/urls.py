from django.urls import path
#from . import views
from polls import views

app_name = 'polls'
'''
urlpatterns = [
    path('', views.index, name='index'),                                 #/polls/
    path('<int:question_id>/', views.detail, name='detail'),             #/polls/5/
    path('<int:question_id>/results/', views.results, name='results'),   #/polls/5/results
    path('<int:question_id>/vote/', views.vote, name='vote'),            #/polls/5/vote
]
'''
#뷰 이름이 클래스형 뷰로 변경되었습니다.
#URL 패턴의 파라미터 이름이 <pk>로 변경되었습니다. 이는 DetailView 제네릭 뷰의 동작 방식 때문.
#즉 테이블의 특정 레코드를 조회하는 경우 Primary Key로 검색을 하는데, Primary Key를 담을 변수명을 pk로 사용.
urlpatterns = [
    # /polls/
    path('', views.IndexView.as_view(), name='index'),
    # /polls/99/
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /polls/99/results/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    # /polls/99/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]