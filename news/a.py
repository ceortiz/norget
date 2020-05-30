from difflib import SequenceMatcher

from django.db.models import Q

#fulltext = ANIMAL
def create_query(fulltext):
    #retrieve objects of 2 models
    illustration_names = Illustration.objects.values_list('name', flat=True)
    tag_names = Tag.objects.values_list('name', flat=True)
    query = []
    #query would like: query = [Q(name="dog"), Q(name="cat"), Q(name="mouse"), Q(tags_name="transpore", Q(tags_name="tops"))]
    
    #iterate thru the objects of Illustration
    for name in illustration_names:
        score = SequenceMatcher(None, name, fulltext).ratio()
        if score == 1:
            # Perfect Match for name
            return [Q(name=name)]

         if score >= THRESHOLD:
            query.append(Q(name=name))

    #iterate thru the objects of Tags
    for name in tag_names:
        score = SequenceMatcher(None, name, fulltext).ratio()
        if score == 1:
            # Perfect Match for name
            return [Q(tags__name=name)]

         if score >= THRESHOLD:
            query.append(Q(tags__name=name))

    return query


   #output: query = [Q(name="dog"), Q(name="cat"), Q(name="mouse"), Q(tags_name="transpore", Q(tags_name="tops"))]
    

from functools import reduce # Needed only in python 3
from operator import or_

queryset = Illustration.objects.filter(reduce(or_, create_query(fulltext)))

#output: queryset = Illustration.objects.filter(query)

#annotate = per object summaries
#aggregate = per entire queryset

new = News.objects.annotate(
          rank=SearchRank(vector, query),
          similarity=TrigramSimilarity(
              'news_title', query
            ) + TrigramSimilarity(
              'headings__heading_title', query
            ),
        ).filter(Q(rank__gte=0.3) | Q(similarity__gt=0.3)).order_by('-rank')[:20]

#define vector

#define query

#find a way so that searchquery(china) also looks for chinese
query = SearchQuery('China') | SearchQuery('Chinese')
new = News.objects.annotate(
          rank=SearchRank(vector, query)
        ).filter(rank__gte=0.1).order_by('-rank')


if f:
...     my = SearchQuery(f.pop())
...     for a in f:
...             my |= SearchQuery(a)

x = News.objects.filter(news_title__trigram_similar="China")

#list
if filters:

    #last element of the list (SearchQuery(last element of filters))
    my_filter = SearchQuery(filters.pop())

    #filters is one less element
    for f in filters:
        #SearchQuery(last element) | SearchQuery(first)
        my_filter |= SearchQuery(f)

#WITHOUT USING TRIGRAM SIMILARITY , ONLY SEARCHQUERY, SEARCHVECTOR, SEARCHRANK
>>> tit = "Little hope ASEAN can rein in China in sea dispute – analyst"
>>> stop = set(stopwords.words('english'))
>>> toks = word_tokenize(tit)
>>> pre = [i for i in toks if i not in stop]
>>> print(pre)
['Little', 'hope', 'ASEAN', 'rein', 'China', 'sea', 'dispute', '–', 'analyst']
>>> vector = SearchVector('news_title', weight='A') + SearchVector('description', weight='B') + SearchVector('headings__heading_title', weight='C')
>>> 
>>> if pre:
...     my = SearchQuery(pre.pop())
...     for i in pre:
...             my |= SearchQuery(i)
... 
>>> print my


>>> new = News.objects.annotate(
...           rank=SearchRank(vector, query)
...         ).filter(rank__gte=0.0).order_by('-rank')
>>> 
News.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gte=0.1).order_by('-rank')
#WITH TRIGRAM SIMILARITY 
#WORKING ALREADY IN SHELL W/ PROPER IMPORTS
#MAYBE YOU COULD NOW START COMBINING W/ SEARCH VECTOR
n = News.objects.annotate(
    similarity=Greatest(
        TrigramSimilarity('news_title', test), 
        TrigramSimilarity('description', test),
        TrigramSimilarity('headings__heading_title', test)
    )).filter(similarity__gte=0.12).order_by('-similarity')


News.objects.annotate(similarity=TrigramSimilarity('news_title', test), TrigramSimilarity('description', test), TrigramSimilarity('categories__category_name', test)).filter(similarity__gt=0.1).order_by('-similarity')

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
                '''if duplicates:
                                            for news in duplicates:
                                                #iterate thru the multiple categories and headings FOR EACH NEWS
                                                    for category,heading in zip(news.categories.all(), news.headings.all()):
                                                        cat_heading = {}
                                                        cat_heading['category'] = category.category_name
                                                        cat_heading['heading'] = heading.heading_title
                                                        existing_news.append(cat_heading)'''

def get_queryset(a):
    search_query = SearchQuery(a)
    vector = SearchVector('news_title', weight='A') + SearchVector('description',weight='B')
    return News.objects.annotate(rank=SearchRank(vector, search_query), similarity=TrigramSimilarity('news_title', search_query) + TrigramSimilarity('description', search_query)).filter(Q(rank__gte=0.3) | Q(similarity__gt=0.3)).order_by('-rank')


def getn(test):
   return News.objects.annotate(
    similarity=Greatest(
        TrigramSimilarity('news_title', test), 
        TrigramSimilarity('description', test),
        TrigramSimilarity('headings__heading_title', test)
    )).filter(similarity__gte=0.09).order_by('-similarity').distinct()

def gitn(test):
   return News.objects.filter(
    Q(news_title__trigram_similar = test) | 
    Q(description__trigram_similar = test) |
    Q(headings__heading_title__trigram_similar = test))
    

def gotn(test):
    vector = SearchVector('news_title', weight='A') + SearchVector('description', weight='B') + SearchVector('headings__heading_title', weight='C')
    return News.objects.annotate(rank=SearchRank(vector, test)).filter(rank__gte=0.1).order_by('-rank')



stop_words = set(stopwords.words('english'))
        
word_tokens = word_tokenize(title)
#split title into words, remove stopwords and put them into a varialbe
pre_filtered_sentence = [w for w in word_tokens if not w in stop_words] 

punctuations = list(string.punctuation)
punctuations.append("''")

filtered_sentence = [i for i in pre_filtered_sentence if i not in punctuations]
