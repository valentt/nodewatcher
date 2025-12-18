# Sekizai template library with added "prepend_data" and "prependtoblock" tags
# See: https://github.com/ojii/django-sekizai/issues/33

from django import template
from sekizai.templatetags.sekizai_tags import (
    SekizaiTag, Options, Argument, Flag, AddtoblockParser, get_varname
)

# Create our own register for this module
register = template.Library()


class PrependData(SekizaiTag):
    name = 'prepend_data'

    options = Options(
        Argument('key'),
        Argument('value'),
    )

    def render_tag(self, context, key, value):
        varname = get_varname()
        context[varname][key].insert(0, value)
        return u''

register.tag('prepend_data', PrependData)


class Prependtoblock(SekizaiTag):
    name = 'prependtoblock'

    options = Options(
        Argument('name'),
        Flag('strip', default=False, true_values=['strip']),
        parser_class=AddtoblockParser,
    )

    def render_tag(self, context, name, strip, nodelist):
        rendered_contents = nodelist.render(context)
        if strip:
            rendered_contents = rendered_contents.strip()
        varname = get_varname()
        context[varname][name].insert(0, rendered_contents)
        return u''

register.tag('prependtoblock', Prependtoblock)
