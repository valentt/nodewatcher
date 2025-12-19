import ipaddress
import re
import time

from django import http
from django.conf import settings
from django.core.cache import cache
from django.views import generic
from django.views.decorators import csrf
from django.utils import decorators, timezone

from nodewatcher.core.monitor import tasks as monitor_tasks
from nodewatcher.utils import datastructures

from . import signals

# UUID validation pattern
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)

# Rate limiting settings
RATE_LIMIT_REQUESTS = getattr(settings, 'PUSH_RATE_LIMIT_REQUESTS', 60)  # requests per window
RATE_LIMIT_WINDOW = getattr(settings, 'PUSH_RATE_LIMIT_WINDOW', 60)  # window in seconds


def get_client_ip(request):
    """
    Safely extract client IP address.
    Only trust X-Forwarded-For when behind a known proxy.
    """
    # SECURITY: Only trust X-Forwarded-For from trusted proxies
    trusted_proxies = getattr(settings, 'TRUSTED_PROXY_IPS', [])
    remote_addr = request.META.get('REMOTE_ADDR', '')

    # If remote address is a trusted proxy, use X-Forwarded-For
    if trusted_proxies and remote_addr in trusted_proxies:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            # Get the leftmost (client) IP
            client_ip = x_forwarded_for.split(',')[0].strip()
            # Validate it looks like an IP address
            try:
                ipaddress.ip_address(client_ip)
                return client_ip
            except ValueError:
                pass

    return remote_addr


def is_rate_limited(identifier):
    """
    Simple rate limiting using Django cache.
    Returns True if the identifier has exceeded the rate limit.
    """
    if not getattr(settings, 'RATELIMIT_ENABLE', True):
        return False

    cache_key = f'ratelimit:push:{identifier}'
    request_count = cache.get(cache_key, 0)

    if request_count >= RATE_LIMIT_REQUESTS:
        return True

    # Increment counter with atomic operation
    try:
        cache.incr(cache_key)
    except ValueError:
        # Key doesn't exist, create it
        cache.set(cache_key, 1, RATE_LIMIT_WINDOW)

    return False


class HttpPushEndpoint(generic.View):
    @decorators.method_decorator(csrf.csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(HttpPushEndpoint, self).dispatch(*args, **kwargs)

    def post(self, request, uuid):
        """
        Handles HTTP push requests from nodewatcher-agent.
        """
        # SECURITY: Validate UUID format to prevent injection attacks
        if not UUID_PATTERN.match(uuid):
            return http.JsonResponse({'status': 'error', 'message': 'Invalid UUID format'}, status=400)

        # Determine the remote IP address safely
        remote_ip = get_client_ip(request)

        # SECURITY: Rate limiting to prevent DoS
        rate_limit_key = f'{remote_ip}:{uuid}'
        if is_rate_limited(rate_limit_key):
            return http.JsonResponse(
                {'status': 'error', 'message': 'Rate limit exceeded'},
                status=429
            )

        context = {
            'push': {
                'source': uuid,
                'data': request.body,
                'timestamp': timezone.now(),
            },
            'identity': {
                'ip_address': remote_ip,
            }
        }

        # Emit signal to augment the context.
        contexts = signals.extract_context.send(sender=self.__class__, headers=request.META, uuid=uuid)
        for _, extracted_context in contexts:
            if not extracted_context:
                continue

            datastructures.merge_dict(context, extracted_context)

        # Schedule a new push task.
        monitor_tasks.run_pipeline.delay(
            run_id=settings.MONITOR_HTTP_PUSH_RUN,
            base_context=context,
        )

        return http.JsonResponse({'status': 'ok'})
