from django.shortcuts import render, HttpResponse, redirect
import requests
import datetime
import string
from bs4 import BeautifulSoup
from django.views import generic
from urllib.request import urlopen
from django.db.models import Q, Count
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from collections import defaultdict
from django.views.generic import View
from news.models import Category, Location, Heading, Publisher, Author, News
#from news.forms import NewsForm
# Create your views here.
def index(request):
	headings = Heading.objects.all()
	#categories = Category.objects.all()
	#news = News.objects.all()

	return render(request, 'news/home.html', {'headings': headings,})

def post_news(request):
	return render(request, 'news/news_form.html')

def get_data(request, method="POST"):
	#news_form = NewsForm()
	if request.method == "POST":
		#category = request.POST.get('category')
		news_url = request.POST.get('news_url')

		webpage = requests.get(news_url)
		soup = BeautifulSoup(webpage.text, "lxml")

		#TITLE
		try:
			news_title = soup.find("meta", property="og:title")
			title = news_title.attrs['content']
		except:
			try:
				news_title = soup.find("meta", {"name":"title"})
				title = news_title.attrs['content']
			except:
				title = ""

		#URL
		try:
			news_url = soup.find("meta", property="og:url")
			url = news_url.attrs['content']
		except:
			try:
				news_url = soup.find("meta", {"name": "url"})
				url = news_url.attrs['content']
			except:
				url = ""

		#IMAGE
		try:
			news_image = soup.find("meta", property="og:image")
			image = news_image.attrs['content']
		except:
			try:
				news_image = soup.find("meta", {"name":"image"})
				image = news_image.attrs['content']
			except:
				image = ""

		#DESCRIPTION
		try:
			news_description = soup.find("meta", property="og:description")
			description = news_description.attrs['content']
		except:
			try:
				news_description = soup.find("meta", {"name": "description"})
				description = news_description.attrs['content']
			except:
				description = ""

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
		

		#query for possible duplicates 
		existing_news = []

		#duplicates = News.objects.filter(news_title__icontains=title)

		#get the title
		stop_words = set(stopwords.words('english'))
						
		word_tokens = word_tokenize(title)
		#split title into words, remove stopwords and put them into a varialbe
		pre_filtered_sentence = [w for w in word_tokens if not w in stop_words] 
		
		punctuations = list(string.punctuation)
		punctuations.append("''")

		filtered_sentence = [i for i in pre_filtered_sentence if i not in punctuations]
		#use postgres search functionality e.g. weights
		vector = SearchVector('news_title', weight='A') + SearchVector('description', weight='B') + SearchVector('headings__heading_title', weight='C')

		selection = defaultdict(list)

		for keyword in filtered_sentence:
			query = SearchQuery(keyword)
			duplicates = News.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.3).order_by('rank')

			if duplicates:
				for news in duplicates:
					#check if it already exists otherwise append
					selection[].append()

		#iterate thrue the variable

			#query the News objects for object which has the word

			#if there is, append them in an array or a list??

		'''for headline in related_headlines:
								if news_title is not None:
									related_news = News.objects.filter(Q(news_title__icontains=news_title) & Q(headings__heading_title__iexact=headline.heading_title))
									if related_news:
										for news in related_news:
											headlines[headline.heading_title].append(news.news_title)
									else:
										headlines[headline.heading_title].append(None)
								else:
									headlines[headline.heading_title].append(None)
						'''
		#DO SOMETHING LIKE THIS BEFORE PLACING LIST INTO CONTEXT:
		if duplicates:
			for news in duplicates:
				#iterate thru the multiple categories and headings FOR EACH NEWS
					for category,heading in zip(news.categories.all(), news.headings.all()):
						cat_heading = {}
						cat_heading['category'] = category.category_name
						cat_heading['heading'] = heading.heading_title
						existing_news.append(cat_heading)

			return render(request, 'news/news_preview.html', {'news_title': title,'news_image': image,'news_description': description, 'news_url': url, 'news_site_name': site, 'news_author': author, 'existing_news': existing_news,})
		else:
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
			heading = Heading()
			
			heading.heading_title = request.POST.get('headline')
			heading.expiration = datetime.datetime.now() + datetime.timedelta(days=7)
			heading.number_of_news = 0
			heading.status = 'Pending'
			heading.upvotes = 0
			heading.location = location
			#downvotes = 0,
			heading.save()
			heading.categories.add(category)

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

		news = News()
		news.news_title = request.POST.get('news_title')
		news.description = request.POST.get('news_description')
		news.pub_date = datetime.datetime.now()
		news.link = request.POST.get('news_url')
		news.status = 'Pending'
		news.upvotes = 0
		#headings.set(heading),
		#headings = heading,
		news.author = author
		news.publisher = publisher
		#categories = category,
		news.location = location
		news.save()
		#look for heading and category
		#related_news = News.objects.filter(headings_heading_title__iexact=heading.heading_title)
		#related_news = News.objects.filter(headings__heading_title__iexact=request.POST.get('headline').count()
		#if related_news > 0:

		#check if duplicates exist
		#if no duplicates, save

		news.headings.add(heading)
		news.categories.add(category)

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
		news_title = request.POST.get('news_title', None)
	else:
		keyword = ''
		news_title = ''

	#get the headlines which has the keyword
	related_headlines = Heading.objects.filter(heading_title__icontains=keyword)
	
	headlines = defaultdict(list)

	for headline in related_headlines:
		if news_title is not None:
			related_news = News.objects.filter(Q(news_title__icontains=news_title) & Q(headings__heading_title__iexact=headline.heading_title))
			if related_news:
				for news in related_news:
					headlines[headline.heading_title].append(news.news_title)
			else:
				headlines[headline.heading_title].append(None)
		else:
			headlines[headline.heading_title].append(None)

	return render(request, 'news/headlines.html', {'headlines':headlines.items(),})

