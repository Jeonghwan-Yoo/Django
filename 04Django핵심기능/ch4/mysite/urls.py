"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

'''
#필요한 모듈과 함수를 임포트합니다. adimn모듈과 path()함수는 장고에서 제공하는 것이고, views모듈은 코딩.
from django.contrib import admin
from django.urls import path
from polls import views

#URL/뷰 매핑을 정의하는 방식은 항상 동일하므로, 그대로 따라서 코딩.
#URL 패턴 매칭은 위에서 아래로 진행하므로 정의하는 순서에 유의.
urlpatterns = [
    #장고의 Admin 사이트에 대한 URLconf는 이미 정의되어 있다.
    #Admin사이트를 사용하려면 항상 이렇게 정의.
    path('admin/', admin.site.urls),
    #polls 애플리케이션에 대한 URL/뷰 매핑을 정의.
    path('polls/', views.index, name='index'),
    path('polls/<int:question_id>/', views.detail, name='detail'),
    path('polls/<int:question_id>/results/', views.results, name='results'),
    path('polls/<int:question_id>/vote/', views.vote, name='vote'),
]
'''

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
]