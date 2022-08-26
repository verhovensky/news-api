from rest_framework import serializers
from taggit.serializers import TagListSerializerField
from news.models import Post


class PostREADSerializer(serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = "__all__"
