from django.urls import path, re_path
from . import views

appname = 'news'

urlpatterns = [
	path('', views.index, name='index'),
	path('post_news', views.post_news, name='post_news'),
	path('get_data', views.get_data, name='get_data'),
	path('post_headline', views.post_headline,name='post_headline'),
	path('memory', views.memory, name='memory'),
	path('headlines', views.headlines_selection, name='headlines'),
]