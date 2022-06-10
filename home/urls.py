from django.urls import path, include
from django.http import HttpResponse

from .views import (
    index, 
    successful_page,
    register_page, 
    # register2_page,
    # register3_page,
    login_page, 
    login2_page, 
    login3_page, 
    logout_page,  
    reset_view, 
    passreset,


    )

# def okay (request):
#     return HttpResponse('pretend-binary-data-here', content_type='image/jpeg')



urlpatterns = [
    # url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
    # path('favicon.ico', okay),
    path('', index, name='index'),
    path('', successful_page, name='Lsuccessful'),
    path('register/', register_page, name='register'),
    # path('register2/', register2_page, name='register2'),
    # path('register3/', register3_page, name='register3'),
    path('login/', login_page, name='login'),
    path('login2/', login2_page, name='login2'),
    path('login3/', login3_page, name='login3'),
    # path('login/<str:uid>', login_from_uid, name='login_uid'),
    path('logout/', logout_page, name='logout'),
    path('reset/', reset_view, name='reset'),
    path('passreset/', passreset, name='passreset'),
    # path('about/', about, name='about'),
    # path('reset/<str:uid>', reset_from_uid, name='reset_uid'),
    
]
