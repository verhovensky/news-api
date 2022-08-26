from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    body = models.TextField(max_length=255, verbose_name="Содержание")
    date = models.DateTimeField(verbose_name="Дата публикации")
    slug = models.SlugField(max_length=255, allow_unicode=True, verbose_name="Слаг")
    tags = TaggableManager(verbose_name="Тэги")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", args=[str(self.id)])

# create form/serializer
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = [
#             'title',
#             'description',
#             'tags',
#         ]

# then in management commands:
#     if form.is_valid():
#         newpost = form.save(commit=False)
#         newpost.slug = slugify(newpost.title)
#         newpost.save()
#         # Without this next line the tags won't be saved.
#         form.save_m2m()

