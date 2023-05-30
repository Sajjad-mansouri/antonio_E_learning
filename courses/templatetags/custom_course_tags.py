from django import template

register=template.Library()


@register.filter
def get_model(obj):
	try:
		return obj._meta.model_name
	except AttributeError:
		return None

