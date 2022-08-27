from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(max_length=5000, verbose_name="Содержание")
    date = models.DateTimeField(verbose_name="Дата публикации")
    slug = models.SlugField(max_length=255, allow_unicode=True, verbose_name="Слаг")
    tags = TaggableManager(verbose_name="Тэги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

