from django import template
from django.utils.safestring import mark_safe

from iqtest.quill_images import lazy_load_images

register = template.Library()


@register.filter(name="lazy_images")
def lazy_images(html):
    if not html:
        return ""
    return mark_safe(lazy_load_images(str(html)))
