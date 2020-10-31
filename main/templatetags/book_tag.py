from django import template
from main.models import Category, Genre

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()


@register.simple_tag()
def get_genres():
    return Genre.objects.all()
