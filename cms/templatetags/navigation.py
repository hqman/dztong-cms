from django import template
import re
register = template.Library()

def rootpath(value):
    path=value.split("/")[1]
    if(len(value)<3):
        path="news"
    return  path 


register.filter('rootpath', rootpath)

@register.tag
def current_nav(parser, token):
    args = token.split_contents()
    template_tag = args[0]
    if len(args) < 2:
        raise template.TemplateSyntaxError, "%r tag requires at least one argument" % template_tag
    return NavSelectedNode(args[1])

class NavSelectedNode(template.Node):
    def __init__(self, url):
        self.url = url

    def render(self, context):
        path = context['request'].path
        pValue = template.Variable(self.url).resolve(context)
        if (pValue == '/' or pValue == '') and not (path  == '/' or path == ''):
            return ""
        if path.startswith(pValue):
            return ' class="selected"'
        return ""

