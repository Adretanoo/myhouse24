from django import template


register = template.Library()

urls_system = {
    "payment_items": ["payment_items", "payment_items_add", "payment_items_edit"],
    "payment_details": ["payment_details"],
    "service_settings": ["service_settings"],
    "roles": ["roles"],
}


@register.simple_tag(takes_context=True)
def menu_active(context, *url_names):
    req = context.get("request")
    if not req:
        return ""
    current_url = req.resolver_match.url_name
    if current_url in url_names:
        return "menu-open"
    return ""


@register.simple_tag(takes_context=True)
def link_active(context, url_name):
    req = context.get("request")
    if not req:
        return ""
    current_url = req.resolver_match.url_name
    if current_url == url_name or current_url.startswith(url_name + "_"):
        return "active-custom"
    return ""
