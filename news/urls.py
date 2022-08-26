from django.urls import path
from news.views import NewsApiView

urlpatterns = [
      path('', NewsApiView.as_view(), name='news_list'),
]
