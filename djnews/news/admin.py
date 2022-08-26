from django.contrib import admin
from djnews.news import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "body", "slug", "tags_list", "date")
    icon_name = 'description'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tags_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())


admin.site.register(Post, PostAdmin)
