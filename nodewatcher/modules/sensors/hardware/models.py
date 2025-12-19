from django.db import models
from django.utils.translation import gettext_noop

from nodewatcher.core.registry import registration
from nodewatcher.modules.monitor.datastream import fields as ds_fields, models as ds_models
from nodewatcher.modules.monitor.datastream.pool import pool as ds_pool


class CpuTemperatureMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    CPU temperature monitoring data.
    """

    last_updated = models.DateTimeField(auto_now=True)
    temperature = models.FloatField(null=True, help_text="CPU temperature in Celsius")
    temperature_max = models.FloatField(null=True, help_text="Maximum safe temperature")
    thermal_throttling = models.BooleanField(default=False, help_text="CPU is thermal throttling")

    class RegistryMeta:
        registry_id = 'sensors.temperature'

registration.point('node.monitoring').register_item(CpuTemperatureMonitor)


class CpuTemperatureMonitorStreams(ds_models.RegistryItemStreams):
    temperature = ds_fields.FloatField(tags={
        'title': gettext_noop("CPU Temperature"),
        'unit': 'C',
        'group': 'hardware_temperature',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 120,
        }
    })

ds_pool.register(CpuTemperatureMonitor, CpuTemperatureMonitorStreams)


class FlashHealthMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    Flash/storage health monitoring data.
    """

    last_updated = models.DateTimeField(auto_now=True)
    total_bytes = models.BigIntegerField(null=True, help_text="Total flash size in bytes")
    used_bytes = models.BigIntegerField(null=True, help_text="Used space in bytes")
    free_bytes = models.BigIntegerField(null=True, help_text="Free space in bytes")
    usage_percent = models.FloatField(null=True, help_text="Usage percentage")
    write_cycles = models.BigIntegerField(null=True, help_text="Estimated write cycles")
    bad_blocks = models.IntegerField(null=True, help_text="Number of bad blocks")
    health_percent = models.FloatField(null=True, help_text="Overall health percentage")

    class RegistryMeta:
        registry_id = 'sensors.flash'

registration.point('node.monitoring').register_item(FlashHealthMonitor)


class FlashHealthMonitorStreams(ds_models.RegistryItemStreams):
    usage_percent = ds_fields.FloatField(tags={
        'title': gettext_noop("Flash Usage"),
        'unit': '%',
        'group': 'storage',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 100,
        }
    })

    health_percent = ds_fields.FloatField(tags={
        'title': gettext_noop("Flash Health"),
        'unit': '%',
        'group': 'storage',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 100,
        }
    })

ds_pool.register(FlashHealthMonitor, FlashHealthMonitorStreams)


class MemoryDetailedMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    Detailed memory/RAM monitoring data.
    """

    last_updated = models.DateTimeField(auto_now=True)
    total = models.BigIntegerField(null=True, help_text="Total RAM in bytes")
    free = models.BigIntegerField(null=True, help_text="Free RAM in bytes")
    available = models.BigIntegerField(null=True, help_text="Available RAM in bytes")
    buffers = models.BigIntegerField(null=True, help_text="Buffer memory in bytes")
    cached = models.BigIntegerField(null=True, help_text="Cached memory in bytes")
    swap_total = models.BigIntegerField(null=True, help_text="Total swap in bytes")
    swap_free = models.BigIntegerField(null=True, help_text="Free swap in bytes")
    usage_percent = models.FloatField(null=True, help_text="RAM usage percentage")

    class RegistryMeta:
        registry_id = 'sensors.memory'

registration.point('node.monitoring').register_item(MemoryDetailedMonitor)


class MemoryDetailedMonitorStreams(ds_models.RegistryItemStreams):
    usage_percent = ds_fields.FloatField(tags={
        'title': gettext_noop("Memory Usage"),
        'unit': '%',
        'group': 'memory',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 100,
        }
    })

    available = ds_fields.IntegerField(tags={
        'title': gettext_noop("Available Memory"),
        'unit': 'bytes',
        'group': 'memory',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
        }
    })

ds_pool.register(MemoryDetailedMonitor, MemoryDetailedMonitorStreams)


class PowerMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    Power consumption and energy monitoring data.
    """

    last_updated = models.DateTimeField(auto_now=True)
    voltage = models.FloatField(null=True, help_text="Input voltage in V")
    current = models.FloatField(null=True, help_text="Current draw in A")
    power_watts = models.FloatField(null=True, help_text="Power consumption in W")
    power_source = models.CharField(max_length=50, null=True, help_text="Power source (ac, poe, battery)")
    poe_standard = models.CharField(max_length=50, null=True, help_text="PoE standard if applicable")
    battery_percent = models.FloatField(null=True, help_text="Battery percentage if on battery")
    uptime_seconds = models.BigIntegerField(null=True, help_text="Uptime in seconds")

    class RegistryMeta:
        registry_id = 'sensors.power'

registration.point('node.monitoring').register_item(PowerMonitor)


class PowerMonitorStreams(ds_models.RegistryItemStreams):
    power_watts = ds_fields.FloatField(tags={
        'title': gettext_noop("Power Consumption"),
        'unit': 'W',
        'group': 'power',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
        }
    })

    voltage = ds_fields.FloatField(tags={
        'title': gettext_noop("Input Voltage"),
        'unit': 'V',
        'group': 'power',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
        }
    })

ds_pool.register(PowerMonitor, PowerMonitorStreams)
