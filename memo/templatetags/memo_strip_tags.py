from django import template
from django.utils.html import strip_tags
import re
from bs4 import BeautifulSoup

register = template.Library()

@register.filter
def strip_images(text):
    text = strip_tags(text)
    text = re.sub(r'\[\[Image:.+\]\]', '', text)
    text = text.replace('&nbsp;', ' ')  # This line removes &nbsp;
    return text


@register.filter
def add_newlines(text):
    return text.replace('<p>', '\n').replace('<br>', '\n')


@register.filter
def strip_images_but_keep_newlines(value):
    soup = BeautifulSoup(value, 'html.parser')

    for tag in soup.find_all(True):
        if tag.name not in ['p', 'br']:
            tag.extract()

    return str(soup)