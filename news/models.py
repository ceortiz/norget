from django.db import models

from datetime import datetime, date
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
'''class UserManager(BaseUserManager):

	user_in_migrations = True

	def _create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError('The given email must be set.')
		email = self.normalize_email(email)
		user = self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, email, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(email, password, **extra_fields)

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(email, password, **extra_fields)'''

'''class User(AbstractUser):
	"""User model"""

	username = None
	email = models.EmailField(_('email address'), unique=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []
	
	objects = UserManager()
	
	Choose = ''
	MALE = 'M'
	FEMALE = 'F'
	SEX_CHOICES = (
		(Choose, ''),
        (MALE, 'Male'),
        (FEMALE, 'Female'),
	)
	middle_name = models.CharField(max_length=30)
	gender = models.CharField(max_length=1, choices=SEX_CHOICES, default=Choose)
	birthday = models.DateField(default=timezone.now) #help_text="Please use the following format: <em>YYYY-MM-DD</em>.")
	address = models.CharField(max_length=250)
	phone_number = models.CharField(max_length=13)
	registration_date = models.DateTimeField(default=datetime.now)
	#profession = models.CharField(max_length=30, choices=PROFESSIONS_CHOICES, default=Choose)'''


class Category(models.Model):
	'''Choose = ''
	Politics = 'Politics'
	Health = 'Health'
	Environment = 'Environment'
	Entertainment = 'Entertainment'
	CATEGORIES = (
		('', 'Choose'),
		(Politics, 'Politics'),
		(Health, 'Health'),
		(Environment, 'Environment'),
		(Entertainment, 'Entertainment'),
		)'''
	category_name = models.CharField(max_length=30)

	def __str__(self):
		return self.category_name

class Location(models.Model):
	#location_name = model.CharField(max_length=250)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=60) 
	state_province = models.CharField(max_length=30) 
	country = models.CharField(max_length=50)

	def __str__(self):
		return self.address

class Heading(models.Model):
	Choose = ''
	Resolved = 'Resolved'
	Pending = 'Pending'
	STATUS_CHOICES = (
		('', 'Choose'),
		(Resolved, 'Resolved'),
		(Pending, 'Pending'),
		)
	heading_title = models.CharField(max_length=50)
	expiration = models.DateField()
	number_of_news = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)]) 
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=Choose)
	#upvotes should be equivalent to the number of users who sent the news to staging area
	upvotes = models.IntegerField(default=0)
	#downvotes are new numbers that will determine if news will be sent to permanent space
	#downvotes = models.IntegerField(default=0)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self): 
		return self.heading_title

class CounterHeading(models.Model):
	Choose = ''
	Resolved = 'Resolved'
	Pending = 'Pending'
	STATUS_CHOICES = (
		('', 'Choose'),
		(Resolved, 'Resolved'),
		(Pending, 'Pending'),
		)
	counterheading_title = models.CharField(max_length=50)
	counter_expiration = models.DateField()
	counter_number_of_news = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(24)]) 
	counter_status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=Choose)
	#upvotes should be equivalent to the number of users who sent the news to staging area
	counter_upvotes = models.IntegerField(default=0)
	#downvotes are new numbers that will determine if news will be sent to permanent space
	#counter_downvotes = models.IntegerField(default=0)
	counter_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	counter_location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self): 
		return self.counterheading_title

class Publisher(models.Model):
	publisher_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)
	#city = models.CharField(max_length=60) 
	#state_province = models.CharField(max_length=30) 
	#country = models.CharField(max_length=50) 
	website = models.URLField(max_length=200)
	
	class Meta:
		ordering = ["-publisher_name"]

	def __str__(self): 
		return self.publisher_name

class Author(models.Model):
	salutation = models.CharField(max_length=10)
	author_name = models.CharField(max_length=200)
	email = models.EmailField()
	#headshot = models.ImageField(upload_to='author_headshots')
	
	def __str__(self): 
		return self.author_name

class News(models.Model):
	Choose = ''
	Staged = 'Staged'
	Pending = 'Pending'
	STATUS_CHOICES = (
		('', 'Choose'),
		(Pending, 'Pending'),
		(Staged, 'Staged'),
		)
	news_title = models.CharField(max_length=250)
	pub_date = pub_date = models.DateTimeField('date published')
	link = models.URLField()
	status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=Choose)
	upvotes = models.IntegerField(default=0)
	#downvotes = models.IntegerField(default=0)
	heading = models.ForeignKey(Heading, on_delete=models.CASCADE)
	author = models.ForeignKey(Author, on_delete=models.CASCADE)
	publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self):
		return self.news_title





