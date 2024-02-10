from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import pytz
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
        return f"{self.user}: rating {self.rating}"


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

    def split_by_XYWZ(self):
        res: list[str] = self.full_text.split('XYWZ')
        if res[-1].startswith("Ранее мы"):
            return res[:-1]
        return res

    def replace_XYWZ(self):
        return self.full_text.replace("XYWZ", " ")[:50]

    def split_photo_urls(self) -> list:
        return self.images_urls.split()

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

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


# class NewsPhotos(models.Model):
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     photo = models.ForeignKey(Photo, on_delete=models.CASCADE)


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     news = models.ForeignKey(News, on_delete=models.CASCADE)
#     answer = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
#     text = models.TextField()
#     date_time = models.DateTimeField(auto_now_add=True)
#     rating = models.IntegerField(default=0)
#
#     def like(self):
#         self.rating += 1
#         self.save()
#         return ''
#
#     def dislike(self):
#         self.rating -= 1
#         self.save()
#         return ''
#
#
# class CmntToCmnt(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     # comment_to_cmnt = models.ForeignKey('self', on_delete=models.CASCADE, default=' ')
#     text = models.TextField()
#     date_time = models.DateTimeField(auto_now_add=True)
#     rating = models.IntegerField(null=False, default=0)


class Advertiser(models.Model):
    name = models.TextField(default='')
    phone = models.CharField(max_length=20, default='')
    address = models.TextField(default='')
    email = models.EmailField(default='bushuev-alex@mail.ru')


class Advertisement(models.Model):
    photo = models.ImageField(default='')
    name = models.TextField(default='')
    description = models.TextField(default='')
    link = models.URLField()
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_after = models.TimeField()
    price = models.FloatField(default=0.0)
    rating = models.IntegerField(default=0)

    def click(self):
        self.rating += 1
        self.save()

