from django import template

register = template.Library()

@register.filter
def format_duration(value):
    """Converts duration from minutes to hours and minutes."""
    hours = value // 60
    minutes = value % 60
    return f"{hours}h {minutes}m" if hours else f"{minutes}m"