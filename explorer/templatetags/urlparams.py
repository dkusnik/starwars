from django import template

register = template.Library()


@register.simple_tag
def get_filter_url(params, param_to_change):
    url_params = params.copy()
    if param_to_change in url_params:
        url_params.remove(param_to_change)
    else:
        url_params.append(param_to_change)
    return f'?{"&".join(url_params)}'
