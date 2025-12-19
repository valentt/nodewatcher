from nodewatcher.core.monitor import processors as monitor_processors
from nodewatcher.modules.monitor.sources.http import processors as http_processors

from . import models


class CpuTemperature(monitor_processors.NodeProcessor):
    """
    Stores CPU temperature monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.hardware.cpu_temperature')

        monitor = node.monitoring.sensors.hardware.cpu_temperature()
        if monitor is not None:
            monitor.temperature = None
            monitor.temperature_max = None
            monitor.thermal_throttling = False

        if version >= 1:
            try:
                data = context.http.sensors.hardware.cpu_temperature

                if monitor is None:
                    monitor = node.monitoring.sensors.hardware.cpu_temperature(
                        create=models.CpuTemperatureMonitor
                    )

                monitor.temperature = float(data.temperature) if hasattr(data, 'temperature') else None
                monitor.temperature_max = float(data.temperature_max) if hasattr(data, 'temperature_max') else None
                monitor.thermal_throttling = bool(data.thermal_throttling) if hasattr(data, 'thermal_throttling') else False
                monitor.save()
            except (AttributeError, TypeError, ValueError):
                if monitor:
                    monitor.save()
        elif monitor:
            monitor.save()

        return context


class FlashHealth(monitor_processors.NodeProcessor):
    """
    Stores flash/storage health monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.hardware.flash_health')

        monitor = node.monitoring.sensors.hardware.flash_health()
        if monitor is not None:
            monitor.total_bytes = None
            monitor.used_bytes = None
            monitor.free_bytes = None
            monitor.usage_percent = None
            monitor.write_cycles = None
            monitor.bad_blocks = None
            monitor.health_percent = None

        if version >= 1:
            try:
                data = context.http.sensors.hardware.flash_health

                if monitor is None:
                    monitor = node.monitoring.sensors.hardware.flash_health(
                        create=models.FlashHealthMonitor
                    )

                monitor.total_bytes = int(data.total_bytes) if hasattr(data, 'total_bytes') else None
                monitor.used_bytes = int(data.used_bytes) if hasattr(data, 'used_bytes') else None
                monitor.free_bytes = int(data.free_bytes) if hasattr(data, 'free_bytes') else None
                monitor.usage_percent = float(data.usage_percent) if hasattr(data, 'usage_percent') else None
                monitor.write_cycles = int(data.write_cycles) if hasattr(data, 'write_cycles') else None
                monitor.bad_blocks = int(data.bad_blocks) if hasattr(data, 'bad_blocks') else None
                monitor.health_percent = float(data.health_percent) if hasattr(data, 'health_percent') else None
                monitor.save()
            except (AttributeError, TypeError, ValueError):
                if monitor:
                    monitor.save()
        elif monitor:
            monitor.save()

        return context


class MemoryDetailed(monitor_processors.NodeProcessor):
    """
    Stores detailed memory monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.hardware.memory_detailed')

        monitor = node.monitoring.sensors.hardware.memory_detailed()
        if monitor is not None:
            monitor.total = None
            monitor.free = None
            monitor.available = None
            monitor.buffers = None
            monitor.cached = None
            monitor.swap_total = None
            monitor.swap_free = None
            monitor.usage_percent = None

        if version >= 1:
            try:
                data = context.http.sensors.hardware.memory_detailed

                if monitor is None:
                    monitor = node.monitoring.sensors.hardware.memory_detailed(
                        create=models.MemoryDetailedMonitor
                    )

                monitor.total = int(data.total) if hasattr(data, 'total') else None
                monitor.free = int(data.free) if hasattr(data, 'free') else None
                monitor.available = int(data.available) if hasattr(data, 'available') else None
                monitor.buffers = int(data.buffers) if hasattr(data, 'buffers') else None
                monitor.cached = int(data.cached) if hasattr(data, 'cached') else None
                monitor.swap_total = int(data.swap_total) if hasattr(data, 'swap_total') else None
                monitor.swap_free = int(data.swap_free) if hasattr(data, 'swap_free') else None
                monitor.usage_percent = float(data.usage_percent) if hasattr(data, 'usage_percent') else None
                monitor.save()
            except (AttributeError, TypeError, ValueError):
                if monitor:
                    monitor.save()
        elif monitor:
            monitor.save()

        return context


class Power(monitor_processors.NodeProcessor):
    """
    Stores power consumption monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.hardware.power')

        monitor = node.monitoring.sensors.hardware.power()
        if monitor is not None:
            monitor.voltage = None
            monitor.current = None
            monitor.power_watts = None
            monitor.power_source = None
            monitor.poe_standard = None
            monitor.battery_percent = None
            monitor.uptime_seconds = None

        if version >= 1:
            try:
                data = context.http.sensors.hardware.power

                if monitor is None:
                    monitor = node.monitoring.sensors.hardware.power(
                        create=models.PowerMonitor
                    )

                monitor.voltage = float(data.voltage) if hasattr(data, 'voltage') else None
                monitor.current = float(data.current) if hasattr(data, 'current') else None
                monitor.power_watts = float(data.power_watts) if hasattr(data, 'power_watts') else None
                monitor.power_source = str(data.power_source) if hasattr(data, 'power_source') else None
                monitor.poe_standard = str(data.poe_standard) if hasattr(data, 'poe_standard') else None
                monitor.battery_percent = float(data.battery_percent) if hasattr(data, 'battery_percent') else None
                monitor.uptime_seconds = int(data.uptime_seconds) if hasattr(data, 'uptime_seconds') else None
                monitor.save()
            except (AttributeError, TypeError, ValueError):
                if monitor:
                    monitor.save()
        elif monitor:
            monitor.save()

        return context
