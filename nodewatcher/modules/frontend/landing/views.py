from django.views import generic

from nodewatcher.modules.frontend.list import views as list_views


class LandingPage(generic.TemplateView):
    template_name = 'landing/index.html'


class OldHomepage(list_views.NodesList):
    """Old homepage showing the node list for comparison."""
    pass
