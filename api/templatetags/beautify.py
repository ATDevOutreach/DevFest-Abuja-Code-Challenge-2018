from django import template

register = template.Library()


@register.filter
def add_class(modelform_input, css_class):
    return modelform_input.as_widget(attrs={'class':css_class})