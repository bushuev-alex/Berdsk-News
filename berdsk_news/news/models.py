from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.utils.translation import gettext


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="static/img/users")
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # суммарный рейтинг каждой статьи автора
        news = News.objects.filter(author=self)
        articles_rating = sum((news_.rating for news_ in news))

        # суммарный рейтинг всех комментариев автора
        comments = Comment.objects.filter(user=self.user)
        comments_by_author_rating = sum((comment.rating for comment in comments))

        # суммарный рейтинг всех комментариев к статьям автора.
        news = News.objects.filter(author=self)
        sets_of_comments = (Comment.objects.filter(news=news_) for news_ in news)

        comments_to_author_rating = 0
        for set_ in sets_of_comments:
            for comment in set_:
                comments_to_author_rating += comment.rating

        self.rating = articles_rating * 3 + comments_by_author_rating + comments_to_author_rating
        self.save()

    def __str__(self):
        return f"{self.user}: rating {self.rating}"


class Category(models.Model):
    power = 'PO'
    business = 'BU'
    finance = 'FI'
    economics = 'EC'
    society = 'SO'
    culture = 'CU'
    sport = 'SP'
    technology = 'TE'
    ecology = 'EC'
    roads = 'RO'
    helth = 'HE'
    housing = 'HO'
    young = 'YO'
    pensions = 'PE'
    photo = 'PH'
    region_154 = 'RE'
    advertisement = 'AD'
    weather = 'WE'
    other = 'OT'

    CATEGORY_TYPE = [(power, 'Политика'),
                     (business, 'Бизнес'),
                     (finance, 'Финансы'),
                     (economics, 'Экономика'),
                     (society, 'Общество'),
                     (culture, 'Культура'),
                     (sport, 'Спорт'),
                     (technology, 'Технологии'),
                     (ecology, 'Экология'),
                     (roads, 'Дороги и транспорт'),
                     (housing, 'ЖКХ'),
                     (young, 'Молодежь'),
                     (pensions, 'Пенсии и пособия'),
                     (photo, 'Фото'),
                     (region_154, 'Новости региона'),
                     (advertisement, 'Объявления'),
                     (weather, 'Погода'),
                     (other, 'Остальное')]

    name = models.CharField(max_length=2, unique=True, choices=CATEGORY_TYPE, default=society)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def get_full_name(self):
        return [x[1] for x in self.CATEGORY_TYPE if x[0] == self.name]

    def __str__(self):
        return self.name


class Photo(models.Model):
    image = models.ImageField(upload_to='static/img')
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=50, default='')


class News(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='NewsCategory', default='SO')
    title = models.TextField()
    text = models.TextField()
    main_photo = models.ImageField(upload_to='static/img', default="static/img/post-slide-1.jpg")
    photo = models.ManyToManyField(Photo, through='NewsPhotos')
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        if len(self.text) < 124:
            return self.text[:len(self.text)]
        return self.text[:124] + "..."

    def get_newest_from_each_category(self):
        pass

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])

    def __str__(self):
        return f"{self.title}: {self.text[:124]}"


class NewsCategory(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class NewsPhotos(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    # comment = models.OneToOneField('self', on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


class CmntToCmnt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=False, default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


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
