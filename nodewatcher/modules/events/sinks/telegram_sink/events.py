"""
Telegram Event Sink for nodewatcher.

Sends node events and warnings to Telegram.
"""
import logging
import requests

from django.conf import settings

from nodewatcher.core.events import base, pool, declarative

logger = logging.getLogger(__name__)

# Severity emoji mapping
SEVERITY_EMOJI = {
    'info': 'ℹ️',
    'warning': '⚠️',
    'error': '🔴',
    'critical': '🚨',
}


class TelegramEventSink(base.EventSink):
    """
    An event sink that sends events to Telegram.
    """

    name = 'telegram'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)

        if not self.bot_token or not self.chat_id:
            logger.warning("Telegram sink disabled: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not configured")
            self.set_enabled(False)

    def send_telegram(self, message):
        """Send message to Telegram."""
        if not self.bot_token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML',
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"Telegram send failed: {e}")
            return False

    def format_event(self, event):
        """Format event for Telegram message."""
        severity = getattr(event, 'severity', 'info')
        emoji = SEVERITY_EMOJI.get(severity, 'ℹ️')

        source_name = getattr(event, 'source_name', 'Unknown')
        source_type = getattr(event, 'source_type', 'event')

        # Get node info if available
        node_info = ""
        related_nodes = getattr(event, 'related_nodes', [])
        if related_nodes:
            node_names = [str(n) for n in related_nodes[:3]]
            node_info = f"\n<b>Node:</b> {', '.join(node_names)}"

        # Build message
        message = f"{emoji} <b>{source_type.upper()}</b>\n"
        message += f"<b>Source:</b> {source_name}{node_info}\n"
        message += f"<b>Severity:</b> {severity}\n"

        # Add record details (limited)
        record = getattr(event, 'record', {})
        for key in ['message', 'description', 'reason']:
            if key in record:
                message += f"\n{record[key]}"
                break

        return message

    def deliver(self, event):
        """
        Sends the received event to Telegram.
        """
        # Only handle node events
        if not isinstance(event, declarative.NodeEventRecord):
            return

        # Skip complement events (absence notifications)
        if event.is_absent():
            return

        message = self.format_event(event)
        self.send_telegram(message)


class TelegramWarningSink(base.EventSink):
    """
    An event sink that sends warnings to Telegram.
    """

    name = 'telegram_warning'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)

        if not self.bot_token or not self.chat_id:
            self.set_enabled(False)

    def send_telegram(self, message):
        """Send message to Telegram."""
        if not self.bot_token or not self.chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML',
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            logger.error(f"Telegram send failed: {e}")
            return False

    def deliver(self, event):
        """
        Sends the received warning to Telegram.
        """
        if not isinstance(event, declarative.NodeWarningRecord):
            return

        severity = getattr(event, 'severity', 'warning')
        emoji = SEVERITY_EMOJI.get(severity, '⚠️')

        if event.is_absent():
            # Warning resolved
            message = f"✅ <b>RESOLVED</b>\n"
            message += f"Warning cleared for {getattr(event, 'source_name', 'node')}"
        else:
            # New warning
            source_name = getattr(event, 'source_name', 'Unknown')

            related_nodes = getattr(event, 'related_nodes', [])
            node_info = ""
            if related_nodes:
                node_names = [str(n) for n in related_nodes[:3]]
                node_info = f"\n<b>Node:</b> {', '.join(node_names)}"

            message = f"{emoji} <b>WARNING</b>\n"
            message += f"<b>Source:</b> {source_name}{node_info}"

        self.send_telegram(message)


# Register sinks
pool.register_sink(TelegramEventSink)
pool.register_sink(TelegramWarningSink)
