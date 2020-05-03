from django.shortcuts import render, HttpResponse
from django.views import generic
from django.views.generic import View
from news.models import Category, Location, Heading, Publisher, Author, News
from news.forms import NewsForm
# Create your views here.
def index(request):
	categories = Category.objects.all()
	return render(request, 'news/home.html', {'categories': categories,})


'''def post_news(request, method="POST"):
	if request.method == "POST":
		news_form = request.get.post()
	else:
		news_form = NewsForm()
		return render(request, 'news/news_form.html', {'news_form': news_form})'''

class post_news(View):
	news_form = NewsForm

	def get(self,request):
		news_form = self.news_form(None)
		return render(request, 'news/news_form.html', {'news_form': news_form})

	def post(self,request):
		news_form = self.news_form(request.POST)

		if news_form.is_valid():
			news = News(
				news_title = news_form.cleaned_data['news_title'],
				pub_date = news_form.cleaned_data['pub_date'],
				link = news_form.cleaned_data['link'],
				heading = news_form.cleaned_data['heading'],
				author = news_form.cleaned_data['author'],
				publisher = news_form.cleaned_data['publisher'],
				category = news_form.cleaned_data['category'],
				Location = news_form.cleaned_data['location'],
				status = 'Pending',
				upvotes = 0
				)
			news.save()

			return render(request, 'news/news_form.html', {'news_form':news_form})











