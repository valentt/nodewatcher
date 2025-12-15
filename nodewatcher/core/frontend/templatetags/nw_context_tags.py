# Override django-missing contextblock to fix Django 4.2 compatibility
# The original contextblock has must_be_first = True which prevents {% load %} before it
# This version removes that constraint

from django.conf import settings
from django import template
from django.template import loader_tags, base

CONTEXT_BLOCK_NAME = '__context_block__'

register = template.Library()


class ContextBlockNode(loader_tags.BlockNode):
    # Django 4.2 fix: Remove must_be_first constraint to allow {% load %} before contextblock
    must_be_first = False

    def __init__(self, name, nodelist):
        super(ContextBlockNode, self).__init__(CONTEXT_BLOCK_NAME, nodelist)

    def _render(self, context):
        block_context = context.render_context.get(loader_tags.BLOCK_CONTEXT_KEY)
        if block_context is None:
            context['block'] = self
            result = self.nodelist.render(context)
        else:
            push = block = block_context.pop(self.name)
            if block is None:
                block = self
            block = type(self)(block.name, block.nodelist)
            block.context = context
            context['block'] = block
            result = block.nodelist.render(context)
            if push is not None:
                block_context.push(self.name, push)
        return result

    def render(self, context):
        try:
            self._render(context)
        except:
            if settings.DEBUG:
                raise
        return u''

    def super(self):
        if not hasattr(self, 'context'):
            return u''
        super(ContextBlockNode, self).super()
        render_context = self.context.render_context
        if (loader_tags.BLOCK_CONTEXT_KEY in render_context and
            render_context[loader_tags.BLOCK_CONTEXT_KEY].get_block(self.name) is not None):
            render_context[loader_tags.BLOCK_CONTEXT_KEY].pop(self.name)
        return u''


@register.tag
def contextblock(parser, token):
    """
    A context block tag compatible with Django 4.2+.
    This version allows {% load %} tags to come before {% contextblock %}.
    """
    nodelist = parser.parse(('endcontextblock',))

    if hasattr(base, 'TokenType'):
        TOKEN_VAR = base.TokenType.VAR
    else:
        TOKEN_VAR = base.TOKEN_VAR

    block_super_token = base.Token(TOKEN_VAR, 'block.super')
    if hasattr(token, 'source'):
        block_super_token.source = token.source
    filter_expression = parser.compile_filter(block_super_token.contents)
    var_node = base.VariableNode(filter_expression)
    parser.extend_nodelist(nodelist, var_node, block_super_token)
    var_node = nodelist.pop()
    nodelist.insert(0, var_node)

    parser.delete_first_token()

    return ContextBlockNode(None, nodelist)
