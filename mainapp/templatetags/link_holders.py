from django import template
from ..models import Menu, Post, Document
from django.urls import reverse
# from django.shortcuts import get_object_or_404

register = template.Library()

@register.simple_tag
def link_holder_exists(url_code):
    return Post.objects.filter(url_code=url_code).count()

@register.simple_tag
def link_holder_content(*args, **kwargs):
    url_code = kwargs['url_code']
    print("URL_CODE", url_code)
    return Post.objects.filter(url_code=url_code).first().text

@register.simple_tag
def link_holder(url_code):
    try:
        post = Post.objects.get(url_code=url_code)
        link = reverse('page_details', kwargs={'pk': post.pk})
    except Post.DoesNotExist:
        link = '#'
    return link

@register.simple_tag
def title_holder(url_code):
    try:
        post = Post.objects.get(url_code=url_code)
        title = post.title
        button_text = post.button_text
        if button_text != 'НЕ УКАЗАН':
            title = button_text
    except Post.DoesNotExist:
        title = 'Страница еще не создана ({})'.format(url_code)
    return title

@register.simple_tag
def doc_holder(url_code):
    try:
        doc = Document.objects.get(url_code=url_code)
        url = doc.document.url
    except Document.DoesNotExist:
        url = '#'
    return url

@register.simple_tag
def doc_title(url_code):
    try:
        doc = Document.objects.get(url_code=url_code)
        title = doc.title
    except Document.DoesNotExist:
        title = 'Загрузите документ с кодом {}'.format(url_code)
    return title

