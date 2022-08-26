from django_filters import rest_framework as filters
from rest_framework.generics import ListAPIView
from djnews.news import PostREADSerializer
from djnews.news import Post
from taggit.forms import TagField


class TagFilter(filters.CharFilter):
    field_class = TagField

    # Override "lookup_expr" as it is defaults to exact
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("lookup_expr", "in")
        super().__init__(*args, **kwargs)


class PostDateTagFilter(filters.FilterSet):
    date__exact = filters.DateTimeFilter(field_name="date__date", lookup_expr="exact")
    date__gt = filters.DateTimeFilter(field_name="date__date", lookup_expr="gt")
    date__lt = filters.DateTimeFilter(field_name="date__date", lookup_expr="lt")
    tags = TagFilter(field_name="tags__name")

    class Meta:
        model = Post
        fields = ("date", "tags")


class NewsApiView(ListAPIView):
    filterset_class = PostDateTagFilter
    filter_backends = (filters.DjangoFilterBackend,)
    serializer_class = PostREADSerializer
    queryset = Post.objects.all()
    paginate_by = 10
