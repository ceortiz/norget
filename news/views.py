from django.shortcuts import render, HttpResponse, redirect
import requests
import datetime
from bs4 import BeautifulSoup
from django.views import generic
from urllib.request import urlopen
from django.views.generic import View
from news.models import Category, Location, Heading, Publisher, Author, News
from news.forms import NewsForm
# Create your views here.
def index(request):
	headings = Heading.objects.all()
	#categories = Category.objects.all()
	#news = News.objects.all()

	return render(request, 'news/home.html', {'headings': headings,})

def post_news(request):
	return render(request, 'news/news_form.html')

def get_data(request, method="POST"):
	news_form = NewsForm()
	if request.method == "POST":
		news_url = request.POST.get('news_url')

		webpage = requests.get(news_url)
		soup = BeautifulSoup(webpage.text, "lxml")

		#TITLE
		news_title = soup.find("meta", property="og:title")
		title = news_title.attrs['content']

		#URL
		news_url = soup.find("meta", property="og:url")
		url = news_url.attrs['content']

		#IMAGE
		news_image = soup.find("meta", property="og:image")
		image = news_image.attrs['content']

		#DESCRIPTION
		try:
			news_description = soup.find("meta", property="og:description")
			description = news_description.attrs['content']
		except:
			pass

		#WEBSITE (needs improvement)
		try:
			news_site = soup.find("meta", property="og:site_name")	
			site = news_site.attrs['content']	
		except:
			try:
				news_site = soup.find("meta", {"name":"source"})
				site = news_site.attrs['content']
			except:
				site = ""
		#AUTHOR
		try:
			news_author = soup.find("meta", property="article:author")
			author = news_author.attrs['content']
		except:
			try:
				news_author = soup.find("meta", {"name":"author"})
				author = news_author.attrs['content']
			except:
				author = ""
		
		return render(request, 'news/news_preview.html', {'news_title': title,'news_image': image,'news_description': description, 'news_url': url, 'news_site_name': site, 'news_author': author,})

	else:
		return render(request, 'news/news_forms.html', {'news_form':news_form})


def post_headline(request, method="POST"):
	if request.method == "POST":
		try:
			#get category object if already existing
			category = Category.objects.get(category_name = request.POST.get('categories'))
		except:
			#create new category if no similar category exists
			category = Category(category_name = request.POST.get('categories'))
			category.save()

		try:
			location = Location.objects.get(address = 'Dancalan')
		except:
			location = Location(request.POST.get('location'))
			location.save()

		try:
			heading = Heading.objects.get(heading_title = request.POST.get('headline'))
		except:
			heading = Heading(
				heading_title = request.POST.get('headline'),
				expiration = datetime.datetime.now() + datetime.timedelta(days=7),
				number_of_news = 0,
				status = 'Pending',
				upvotes = 0,
				#downvotes = 0,
				category = category,
				location = location,
				)
			heading.save()

		try:
			publisher = Publisher.objects.get(publisher_name = request.POST.get('news_site_name'))
		except:
			publisher = Publisher(
				publisher_name = request.POST.get('news_site_name'),
				address = 'Philippines',
				location = location,
				website = request.POST.get('news_url'),
				)
			publisher.save()

		try:
			author = Author.objects.get(author_name = request.POST.get('news_author'))
		except:
			author = Author(
				salutation = 'Ms',
				author_name = request.POST.get('news_author'),
				email = 'ceortiz@up.edu.ph',
				)
			author.save()


		news = News(
			news_title = request.POST.get('news_title'),
			pub_date = datetime.datetime.now(),
			link = request.POST.get('news_url'),
			status = 'Pending',
			upvotes = 0,
			heading = heading,
			author = author,
			publisher = publisher,
			category = category,
			location = location,
			)
		news.save()

		#return render(request, 'news/home.html', {'news':news,})
		return redirect('index')

	else:
		return render(request, 'news/home.html')

	return render(request, 'news/home.html')

def memory(request):
	return render(request, 'news/memory.html')


def headlines_selection(request, method="POST"):
	if request.method == "POST":
		keyword = request.POST.get('keyword', None)
	else:
		keyword = ''

	headlines = Heading.objects.filter(heading_title__icontains=keyword)

	return render(request, 'news/headlines.html', {'headlines':headlines,})

