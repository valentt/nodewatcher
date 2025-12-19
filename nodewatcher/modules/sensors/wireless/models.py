from django.db import models
from django.utils.translation import gettext_noop

from nodewatcher.core.registry import registration
from nodewatcher.modules.monitor.datastream import fields as ds_fields, models as ds_models
from nodewatcher.modules.monitor.datastream.pool import pool as ds_pool


class WifiAirtimeMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    WiFi airtime monitoring data per interface.
    """

    interface = models.CharField(max_length=50)
    last_updated = models.DateTimeField(auto_now=True)

    # Airtime metrics (in microseconds or percentage)
    busy_time = models.BigIntegerField(null=True, help_text="Channel busy time in microseconds")
    receive_time = models.BigIntegerField(null=True, help_text="Receive time in microseconds")
    transmit_time = models.BigIntegerField(null=True, help_text="Transmit time in microseconds")
    active_time = models.BigIntegerField(null=True, help_text="Active time in microseconds")

    # Calculated percentages
    busy_percent = models.FloatField(null=True, help_text="Channel busy percentage")
    rx_percent = models.FloatField(null=True, help_text="RX airtime percentage")
    tx_percent = models.FloatField(null=True, help_text="TX airtime percentage")

    # Channel info
    channel = models.IntegerField(null=True, help_text="Current channel")
    channel_width = models.IntegerField(null=True, help_text="Channel width in MHz")
    noise_floor = models.IntegerField(null=True, help_text="Noise floor in dBm")

    class RegistryMeta:
        registry_id = 'sensors.airtime'
        multiple = True

registration.point('node.monitoring').register_item(WifiAirtimeMonitor)


class WifiAirtimeMonitorStreams(ds_models.RegistryItemStreams):
    busy_percent = ds_fields.FloatField(tags={
        'title': ds_fields.TagReference('interface', gettext_noop("%(interface)s Busy")),
        'unit': '%',
        'group': 'airtime',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 100,
        }
    })

    noise_floor = ds_fields.IntegerField(tags={
        'title': ds_fields.TagReference('interface', gettext_noop("%(interface)s Noise")),
        'unit': 'dBm',
        'group': 'airtime',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
        }
    })

    def get_stream_query_tags(self):
        tags = super(WifiAirtimeMonitorStreams, self).get_stream_query_tags()
        tags.update({'interface': self._model.interface})
        return tags

    def get_stream_tags(self):
        tags = super(WifiAirtimeMonitorStreams, self).get_stream_tags()
        tags.update({'interface': self._model.interface})
        return tags

ds_pool.register(WifiAirtimeMonitor, WifiAirtimeMonitorStreams)


class MeshQualityMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    Mesh network link quality monitoring data.
    """

    peer_id = models.CharField(max_length=100, help_text="Peer node identifier")
    last_updated = models.DateTimeField(auto_now=True)

    # Link quality metrics
    link_quality = models.FloatField(null=True, help_text="Link quality (0-1)")
    neighbor_link_quality = models.FloatField(null=True, help_text="Neighbor's link quality (0-1)")
    expected_throughput = models.BigIntegerField(null=True, help_text="Expected throughput in Kbps")

    # Signal metrics
    signal_strength = models.IntegerField(null=True, help_text="Signal strength in dBm")
    signal_noise = models.IntegerField(null=True, help_text="Signal noise in dBm")
    snr = models.FloatField(null=True, help_text="Signal to noise ratio in dB")

    # Packet stats
    tx_packets = models.BigIntegerField(null=True, help_text="Transmitted packets")
    rx_packets = models.BigIntegerField(null=True, help_text="Received packets")
    tx_bytes = models.BigIntegerField(null=True, help_text="Transmitted bytes")
    rx_bytes = models.BigIntegerField(null=True, help_text="Received bytes")
    tx_retries = models.BigIntegerField(null=True, help_text="TX retries")
    tx_failed = models.BigIntegerField(null=True, help_text="TX failures")

    # Connection info
    mcs_rate = models.IntegerField(null=True, help_text="MCS rate index")
    bitrate = models.FloatField(null=True, help_text="Current bitrate in Mbps")
    protocol = models.CharField(max_length=50, null=True, help_text="Mesh protocol (batman, olsr, babel)")

    class RegistryMeta:
        registry_id = 'sensors.mesh'
        multiple = True

registration.point('node.monitoring').register_item(MeshQualityMonitor)


class MeshQualityMonitorStreams(ds_models.RegistryItemStreams):
    link_quality = ds_fields.FloatField(tags={
        'title': ds_fields.TagReference('peer_id', gettext_noop("Link to %(peer_id)s")),
        'group': 'mesh_quality',
        'visualization': {
            'type': 'line',
            'initial_set': True,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 1,
        }
    })

    signal_strength = ds_fields.IntegerField(tags={
        'title': ds_fields.TagReference('peer_id', gettext_noop("Signal %(peer_id)s")),
        'unit': 'dBm',
        'group': 'mesh_signal',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
        }
    })

    expected_throughput = ds_fields.IntegerField(tags={
        'title': ds_fields.TagReference('peer_id', gettext_noop("Throughput %(peer_id)s")),
        'unit': 'Kbps',
        'group': 'mesh_throughput',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
        }
    })

    def get_stream_query_tags(self):
        tags = super(MeshQualityMonitorStreams, self).get_stream_query_tags()
        tags.update({'peer_id': self._model.peer_id})
        return tags

    def get_stream_tags(self):
        tags = super(MeshQualityMonitorStreams, self).get_stream_tags()
        tags.update({
            'peer_id': self._model.peer_id,
            'protocol': self._model.protocol,
        })
        return tags

ds_pool.register(MeshQualityMonitor, MeshQualityMonitorStreams)


class ChannelSurveyMonitor(registration.bases.NodeMonitoringRegistryItem):
    """
    WiFi channel survey data for spectrum analysis.
    """

    interface = models.CharField(max_length=50)
    channel = models.IntegerField(help_text="Channel number")
    last_updated = models.DateTimeField(auto_now=True)

    frequency = models.IntegerField(null=True, help_text="Frequency in MHz")
    noise_floor = models.IntegerField(null=True, help_text="Noise floor in dBm")
    active_time = models.BigIntegerField(null=True, help_text="Active time in ms")
    busy_time = models.BigIntegerField(null=True, help_text="Busy time in ms")
    receive_time = models.BigIntegerField(null=True, help_text="Receive time in ms")
    transmit_time = models.BigIntegerField(null=True, help_text="Transmit time in ms")
    busy_percent = models.FloatField(null=True, help_text="Channel utilization percentage")

    class RegistryMeta:
        registry_id = 'sensors.survey'
        multiple = True

registration.point('node.monitoring').register_item(ChannelSurveyMonitor)


class ChannelSurveyMonitorStreams(ds_models.RegistryItemStreams):
    busy_percent = ds_fields.FloatField(tags={
        'title': ds_fields.TagReference('channel', gettext_noop("Ch %(channel)s Busy")),
        'unit': '%',
        'group': 'channel_survey',
        'visualization': {
            'type': 'line',
            'initial_set': False,
            'time_downsamplers': ['mean'],
            'value_downsamplers': ['min', 'mean', 'max'],
            'minimum': 0,
            'maximum': 100,
        }
    })

    def get_stream_query_tags(self):
        tags = super(ChannelSurveyMonitorStreams, self).get_stream_query_tags()
        tags.update({
            'interface': self._model.interface,
            'channel': self._model.channel,
        })
        return tags

    def get_stream_tags(self):
        tags = super(ChannelSurveyMonitorStreams, self).get_stream_tags()
        tags.update({
            'interface': self._model.interface,
            'channel': self._model.channel,
            'frequency': self._model.frequency,
        })
        return tags

ds_pool.register(ChannelSurveyMonitor, ChannelSurveyMonitorStreams)
