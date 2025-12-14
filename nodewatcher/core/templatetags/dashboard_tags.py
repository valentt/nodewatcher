from django import template
from django.contrib.auth import models as auth_models

register = template.Library()


@register.simple_tag
def get_node_count():
    """Get total number of nodes."""
    try:
        from nodewatcher.core import models as core_models
        return core_models.Node.objects.count()
    except:
        return 0


@register.simple_tag
def get_project_count():
    """Get total number of projects."""
    try:
        from nodewatcher.modules.administration.projects import models as project_models
        return project_models.Project.objects.count()
    except:
        return 0


@register.simple_tag
def get_user_count():
    """Get total number of active users."""
    try:
        return auth_models.User.objects.filter(is_active=True).count()
    except:
        return 0


@register.simple_tag
def get_build_count():
    """Get total number of builds."""
    try:
        from nodewatcher.core.generator import models as generator_models
        return generator_models.BuildResult.objects.count()
    except:
        return 0


@register.simple_tag
def get_online_node_count():
    """Get number of online nodes (seen in last 10 minutes)."""
    try:
        from django.utils import timezone
        import datetime
        from nodewatcher.core import models as core_models
        threshold = timezone.now() - datetime.timedelta(minutes=10)
        # This requires monitoring data - simplified for now
        return 0
    except:
        return 0


@register.simple_tag
def get_pending_build_count():
    """Get number of pending builds."""
    try:
        from nodewatcher.core.generator import models as generator_models
        return generator_models.BuildResult.objects.filter(
            status__in=[generator_models.BuildResult.PENDING, generator_models.BuildResult.BUILDING]
        ).count()
    except:
        return 0


@register.simple_tag
def get_failed_build_count():
    """Get number of failed builds."""
    try:
        from nodewatcher.core.generator import models as generator_models
        return generator_models.BuildResult.objects.filter(
            status=generator_models.BuildResult.FAILED
        ).count()
    except:
        return 0


@register.simple_tag
def get_ip_pool_count():
    """Get total number of top-level IP pools."""
    try:
        from nodewatcher.core.allocation.ip import models as ip_models
        return ip_models.IpPool.objects.filter(parent=None).count()
    except:
        return 0
