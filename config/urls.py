"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path("todo/",include("todo.urls")),
    path("accounts/",include("user.urls")),

    # 과제에 주어진 logout 구현 방법 
    # path("accounts/",include("django.contrib.auth.urls")), 처럼 작성
    # 위 처럼 작성하면 accounts/logout/ 의 url 사용 가능 html에서 url 잡아주면 로그아웃 기능 사용가능 아래 처럼

    #<form action="{% url "logout" %}" method="POST">
                #{% csrf_token %}
                #<button>로그아웃</button>
    
]
