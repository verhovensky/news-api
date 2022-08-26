from django.urls import path
from djnews.news import NewsApiView

urlpatterns = [
      path('', NewsApiView.as_view(), name='news_list'),
]
