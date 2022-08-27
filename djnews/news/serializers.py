from rest_framework import serializers
from news.models import Post
from taggit.serializers import (TagListSerializerField,
                                TaggitSerializer)


class PostREADSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Post
        fields = "__all__"
