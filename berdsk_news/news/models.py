from django.db import models
# from django.contrib.auth.models import User
from django.urls import reverse
from berdsk_news.settings import PARTIAL_CONTENT
# import pytz
# from datetime import datetime
# from django.utils.translation import gettext
# from itertools import zip_longest


class Origin(models.Model):
    name = models.CharField(unique=True, null=False)
    base_url = models.CharField(unique=True, null=False)
    icon_url = models.CharField(null=True, default="нет")
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return ''

    def dislike(self):
        self.rating -= 1
        self.save()
        return ''

    def __str__(self):
        return f"{self.name}: {self.base_url}"


class Author(models.Model):
    first_name = models.CharField(max_length=20, null=True)
    middle_name = models.CharField(max_length=20, null=True)
    last_name = models.CharField(max_length=20, null=True)
    work_at = models.ForeignKey(Origin, null=True, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return ''

    def dislike(self):
        self.rating -= 1
        self.save()
        return ''

    def __str__(self):
        return f"{self.first_name, self.last_name}: rating {self.rating}"


class Category(models.Model):

    name = models.CharField(unique=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return ''

    def dislike(self):
        self.rating -= 1
        self.save()
        return ''

    def __str__(self):
        return self.name


class Tag(models.Model):

    name = models.CharField(unique=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return ''

    def dislike(self):
        self.rating -= 1
        self.save()
        return ''

    def __str__(self):
        return self.name


class Photo(models.Model):
    image_url = models.CharField()
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField()


class News(models.Model):
    author = models.ForeignKey(Author, null=True, on_delete=models.CASCADE)  # models.CharField()  #
    title = models.TextField()
    brief_text = models.TextField()
    full_text = models.TextField()
    title_image_url = models.TextField()
    images_urls = models.TextField(null=True)
    tag = models.ManyToManyField(Tag, through="NewsTag")
    search_words = models.TextField(null=True)
    category = models.ManyToManyField(Category, through="NewsCategory", null=True)
    parsed_from = models.ForeignKey(Origin, null=True, on_delete=models.CASCADE)  # models.CharField(30)  #
    full_text_link = models.TextField()
    published_at = models.DateTimeField()
    parsed_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()
        return ''

    def dislike(self):
        self.rating -= 1
        self.save()
        return ''

    def preview(self):
        if len(self.full_text) < 124:
            return self.full_text[:len(self.text)]
        return self.full_text[:124] + "..."

    def split_by_XYWZ(self) -> list[str]:
        if PARTIAL_CONTENT:
            partial_text_len = len(self.full_text) // 3
            return self.full_text[:partial_text_len].split('XYWZ')
        return self.full_text.split('XYWZ')

    def replace_XYWZ(self):
        return self.full_text.replace("XYWZ", " ")[:50]

    def split_photo_urls(self) -> list:
        return self.images_urls.split()

    def get_absolute_url(self):
        return reverse(viewname='news_by_id', args=[str(self.id)])

    def __str__(self):
        return f"{self.title}: {self.full_text[:20]}"


class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'category',)


class NewsTag(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('news', 'tag',)


class Advertiser(models.Model):
    name = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')
    email = models.EmailField(default='')
    subject = models.TextField(default='')
    text = models.TextField(null=False, default='')
    company_name = models.CharField(null=True, default='')
    address = models.TextField(null=True, default='')

    rating = models.IntegerField(default=0)

    def click(self):
        self.rating += 1
        self.save()


class Advertisement(models.Model):
    images_urls = models.TextField(default='', null=True)
    name = models.TextField(default='')
    description = models.TextField(default='')
    link = models.URLField()
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # expire_after = models.TimeField()
    price = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0)

    def click(self):
        self.rating += 1
        self.save()

    def get_images_urls(self) -> list:
        return self.images_urls.split()


class Search(models.Model):
    search = models.CharField(max_length=30)
