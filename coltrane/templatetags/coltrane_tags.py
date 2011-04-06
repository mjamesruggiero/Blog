from django import template
from django.db.models import get_model
from coltrane.models import Entry

def do_latest_entries(parser, token):
    return LatestEntriesNode()

def do_latest_content(parser, token):
    """Return set of latest content items"""
    bits = token.split_contents()
    if len( bits ) != 5:
        raise template.TemplateSyntaxError(
                "get_latest_entries tag takes exactly four arguments")
    model_args = bits[1].split('.')
    if len(model_args) != 2:
        raise template.TemplateSyntaxError("First argument to do_latest_content tag \
               must be 'application_name'.'model_name' string (you passed %s)" % bits[1])
    model = get_model(*model_args)
    if model is None:
        raise template.TemplateSyntaxError(
                "'get_latest_content' tag got invalid model: %s" % bits[1])
    return LatestContentsNode(model, bits[2], bits[4])
         
class LatestContentsNode(template.Node):
    """Generates latest node for template sidebars"""
    def __init__(self, model, num, varname):
        self.model = model
        self.num = int( num )
        self.varname = varname
            
    def render(self, context):
        """Return the string value"""
        context[self.varname] = self.model._default_manager.all()[:self.num]
        return ''

class LatestEntriesNode(template.Node):
    def render(self, context):
        context['latest_entries'] = Entry.live.all()[:5]
        return ''



register = template.Library()
register.tag('get_latest_content', do_latest_content);
