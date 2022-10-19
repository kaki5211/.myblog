
from django import template

register = template.Library()

@register.filter(name='get_tag_el')
def get_img_src(value, key):
    key_ = "<"+key
    word_ = value.split(key_,1)[1].split('>')[0]

    
    """
        ...
    """
    return word_