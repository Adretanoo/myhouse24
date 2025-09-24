from django import template

register = template.Library()

urls_system = {
    "service_settings": ["service_settings"],
    "tariffs": ["tariffs", "tariffs_add", "tariffs_edit", "tariffs_copy"],
    "payment_items": ["payment_items", "payment_items_add", "payment_items_edit"],
    "payment_details": ["payment_details"],
    "users": ["users", "users_add", "users_edit"],
    "roles": ["roles"],
    "main_page": ["main_page"],
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
