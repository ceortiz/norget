
from django.db import models
import datetime
from django.forms import ModelForm, formset_factory, Textarea
from django.core.validators import MaxValueValidator, MinValueValidator
from django import forms
from news.models import Category, Location, Heading, Publisher, Author, News

'''class NewsForm(ModelForm):
	class Meta:
		model = News
		fields = ['news_title', 'link', 'heading', 'author', 'pub_date', 'publisher', 'category', 'location']

'''