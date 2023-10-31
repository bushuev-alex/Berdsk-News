from django import template
from news.models import News, Category
from django.db.models.query import QuerySet

# bad_words += [word.capitalize() for word in bad_words]

register = template.Library()


@register.filter()
def news_by_category(category_id: int) -> QuerySet:
    news_qs = News.objects.filter(category=category_id).order_by('-id')
    return news_qs


# @register.filter()
# def current_hour(tz):
#    return datetime.now(zoneinfo.ZoneInfo(tz)).hour


# @register.filter()
# def censor(sentence: str):
#     sentence_ = re.sub("[\"\',.!:;]", '', sentence)  # delete punctuation marks
#     words = sentence_.split(' ')  # split sentence by ' '
#     bad_exist = set(words).intersection(bad_words)  #
#     for bad_word in bad_exist:
#         replace_by = bad_word[0] + '*' * (len(bad_word) - 1)
#         sentence = re.sub(bad_word, replace_by, sentence)
#     return sentence


if __name__ == '__main__':
    pass
    # import re
    # sent = re.sub(f"my ({'|'.join(bad_words)})", "good_news", "This is bad_news.")
    # print(sent)
