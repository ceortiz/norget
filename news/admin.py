from django.contrib import admin

# Register your models here.
from .models import Category, Location, Heading, Publisher, Author, News

admin.site.register(Category)
admin.site.register(Location)
admin.site.register(Heading)
admin.site.register(Publisher)
admin.site.register(Author)
admin.site.register(News)
