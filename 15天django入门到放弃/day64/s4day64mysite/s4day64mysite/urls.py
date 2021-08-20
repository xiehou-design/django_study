"""s4day64mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from django.shortcuts import HttpResponse,render,redirect
def login(request):
    """
    处理用户请求，并返回内容
    :param request: 用户请求相关的所有信息（对象）
    :return:
    """
    # 字符串
    # return HttpResponse('<input type="text" />')
    # return HttpResponse('login.html')
    # 自动找到模板路径下的login.html文件，读取内容并返回给用户
    # 模板路径的配置
    print(request.GET)
    if request.method == "GET":
        return render(request,'login.html')
    else:
        # 用户POST提交的数据（请求体）
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        if u == 'root' and p == '123123':
            # 登录成功
            # return redirect('http://www.oldboyedu.com')
            return redirect('/index/')
        else:
            # 登录失败
            return render(request,'login.html',{'msg': '用户名或密码错误'})

def index(request):
    # return HttpResponse('Index')
    return render(
        request,
        'index.html',
        {
            'name': 'alex',
            'users':['李志','李杰'],
            'user_dict':{'k1': 'v1','k2':'v2'},
            'user_list_dict': [
                {'id':1, 'name': 'alex', 'email': 'alex3714@163.com'},
                {'id':2, 'name': 'alex2', 'email': 'alex3714@1632.com'},
                {'id':3, 'name': 'alex3', 'email': 'alex3713@1632.com'},
            ]
        }
    )

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^login/', login),
    url(r'^index/', index),
]
