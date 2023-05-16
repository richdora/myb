from django import template
from django.utils.html import strip_tags
import re

register = template.Library()

@register.filter
def strip_images(text):
    text = strip_tags(text)
    text = re.sub(r'\[\[Image:.+\]\]', '', text)
    text = re.sub('&nbsp;', ' ', text)  # This line removes &nbsp;
    return text
