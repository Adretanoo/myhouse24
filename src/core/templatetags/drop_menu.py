from django import template

register = template.Library()
urls_system = ["payment_details", "service_settings"]


@register.simple_tag(takes_context=True)
def menu_active(context):
    req = context.get("request")
    if not req:
        return ""
    current_url = req.resolver_match.url_name
    if current_url in urls_system:
        return "menu-open"
    return ""


@register.simple_tag(takes_context=True)
def link_active(context, url_name):
    req = context.get("request")
    if not req:
        return ""
    current_url = req.resolver_match.url_name
    if current_url == url_name:
        return "active-custom"
    return ""
