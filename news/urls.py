from django.urls import path, re_path
from . import views

appname = 'news'

urlpatterns = [
	path('', views.index, name='index'),
	path('post_news', views.post_news.as_view(), name='post_news'),
]