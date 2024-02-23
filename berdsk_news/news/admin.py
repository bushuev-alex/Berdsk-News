from django.contrib import admin

from .models import (Author,
                     Category,
                     Photo,
                     News,
                     Origin,
                     Tag,
                     NewsCategory,
                     NewsTag,
                     Advertiser,
                     Advertisement,
                     Search
                     )


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(News)
admin.site.register(Origin)
admin.site.register(Tag)
admin.site.register(Search)
admin.site.register(NewsCategory)
admin.site.register(NewsTag)
admin.site.register(Advertiser)
admin.site.register(Advertisement)
