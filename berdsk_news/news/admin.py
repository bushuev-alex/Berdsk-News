from django.contrib import admin

from .models import (Author,
                     Category,
                     Photo,
                     News,
                     NewsCategory,
                     NewsPhotos,
                     Comment,
                     CmntToCmnt,
                     Advertiser,
                     Advertisement,
                     )


# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Photo)
admin.site.register(News)
admin.site.register(NewsCategory)
admin.site.register(NewsPhotos)
admin.site.register(Comment)
admin.site.register(CmntToCmnt)
admin.site.register(Advertiser)
admin.site.register(Advertisement)
