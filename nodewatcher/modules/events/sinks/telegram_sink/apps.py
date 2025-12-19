from django.apps import AppConfig


class TelegramSinkConfig(AppConfig):
    name = 'nodewatcher.modules.events.sinks.telegram_sink'
    label = 'events_sinks_telegram'
