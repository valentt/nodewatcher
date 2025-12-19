from nodewatcher.core.monitor import processors as monitor_processors
from nodewatcher.modules.monitor.sources.http import processors as http_processors

from . import models


class WifiAirtime(monitor_processors.NodeProcessor):
    """
    Stores WiFi airtime monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.wireless.airtime')

        existing = {}
        for item in node.monitoring.sensors.wireless.airtime():
            item.busy_time = None
            item.receive_time = None
            item.transmit_time = None
            item.active_time = None
            item.busy_percent = None
            item.rx_percent = None
            item.tx_percent = None
            existing[item.interface] = item

        if version >= 1:
            try:
                for iface, data in context.http.sensors.wireless.airtime.items():
                    if iface.startswith('_'):
                        continue

                    node.monitoring.sensors.wireless.airtime(queryset=True).update_or_create(
                        root=node,
                        interface=iface,
                        defaults={
                            'busy_time': int(data.busy_time) if hasattr(data, 'busy_time') else None,
                            'receive_time': int(data.receive_time) if hasattr(data, 'receive_time') else None,
                            'transmit_time': int(data.transmit_time) if hasattr(data, 'transmit_time') else None,
                            'active_time': int(data.active_time) if hasattr(data, 'active_time') else None,
                            'busy_percent': float(data.busy_percent) if hasattr(data, 'busy_percent') else None,
                            'rx_percent': float(data.rx_percent) if hasattr(data, 'rx_percent') else None,
                            'tx_percent': float(data.tx_percent) if hasattr(data, 'tx_percent') else None,
                            'channel': int(data.channel) if hasattr(data, 'channel') else None,
                            'channel_width': int(data.channel_width) if hasattr(data, 'channel_width') else None,
                            'noise_floor': int(data.noise_floor) if hasattr(data, 'noise_floor') else None,
                        }
                    )

                    if iface in existing:
                        del existing[iface]
            except (AttributeError, TypeError, ValueError):
                pass

        for item in existing.values():
            item.save()

        return context


class MeshQuality(monitor_processors.NodeProcessor):
    """
    Stores mesh network quality monitor data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.wireless.mesh_quality')

        existing = {}
        for item in node.monitoring.sensors.wireless.mesh_quality():
            item.link_quality = None
            item.neighbor_link_quality = None
            item.expected_throughput = None
            item.signal_strength = None
            existing[item.peer_id] = item

        if version >= 1:
            try:
                for peer_id, data in context.http.sensors.wireless.mesh_quality.items():
                    if peer_id.startswith('_'):
                        continue

                    node.monitoring.sensors.wireless.mesh_quality(queryset=True).update_or_create(
                        root=node,
                        peer_id=peer_id,
                        defaults={
                            'link_quality': float(data.link_quality) if hasattr(data, 'link_quality') else None,
                            'neighbor_link_quality': float(data.neighbor_link_quality) if hasattr(data, 'neighbor_link_quality') else None,
                            'expected_throughput': int(data.expected_throughput) if hasattr(data, 'expected_throughput') else None,
                            'signal_strength': int(data.signal_strength) if hasattr(data, 'signal_strength') else None,
                            'signal_noise': int(data.signal_noise) if hasattr(data, 'signal_noise') else None,
                            'snr': float(data.snr) if hasattr(data, 'snr') else None,
                            'tx_packets': int(data.tx_packets) if hasattr(data, 'tx_packets') else None,
                            'rx_packets': int(data.rx_packets) if hasattr(data, 'rx_packets') else None,
                            'tx_bytes': int(data.tx_bytes) if hasattr(data, 'tx_bytes') else None,
                            'rx_bytes': int(data.rx_bytes) if hasattr(data, 'rx_bytes') else None,
                            'tx_retries': int(data.tx_retries) if hasattr(data, 'tx_retries') else None,
                            'tx_failed': int(data.tx_failed) if hasattr(data, 'tx_failed') else None,
                            'mcs_rate': int(data.mcs_rate) if hasattr(data, 'mcs_rate') else None,
                            'bitrate': float(data.bitrate) if hasattr(data, 'bitrate') else None,
                            'protocol': str(data.protocol) if hasattr(data, 'protocol') else None,
                        }
                    )

                    if peer_id in existing:
                        del existing[peer_id]
            except (AttributeError, TypeError, ValueError):
                pass

        for item in existing.values():
            item.save()

        return context


class ChannelSurvey(monitor_processors.NodeProcessor):
    """
    Stores WiFi channel survey data into the database.
    """

    @monitor_processors.depends_on_context('http', http_processors.HTTPTelemetryContext)
    def process(self, context, node):
        """
        Called for every processed node.

        :param context: Current context
        :param node: Node that is being processed
        :return: A (possibly) modified context
        """

        version = context.http.get_module_version('sensors.wireless.channel_survey')

        existing = {}
        for item in node.monitoring.sensors.wireless.channel_survey():
            item.busy_percent = None
            existing[(item.interface, item.channel)] = item

        if version >= 1:
            try:
                for key, data in context.http.sensors.wireless.channel_survey.items():
                    if key.startswith('_'):
                        continue

                    # Key format: "interface:channel"
                    parts = key.split(':')
                    if len(parts) != 2:
                        continue
                    iface, channel = parts[0], int(parts[1])

                    node.monitoring.sensors.wireless.channel_survey(queryset=True).update_or_create(
                        root=node,
                        interface=iface,
                        channel=channel,
                        defaults={
                            'frequency': int(data.frequency) if hasattr(data, 'frequency') else None,
                            'noise_floor': int(data.noise_floor) if hasattr(data, 'noise_floor') else None,
                            'active_time': int(data.active_time) if hasattr(data, 'active_time') else None,
                            'busy_time': int(data.busy_time) if hasattr(data, 'busy_time') else None,
                            'receive_time': int(data.receive_time) if hasattr(data, 'receive_time') else None,
                            'transmit_time': int(data.transmit_time) if hasattr(data, 'transmit_time') else None,
                            'busy_percent': float(data.busy_percent) if hasattr(data, 'busy_percent') else None,
                        }
                    )

                    if (iface, channel) in existing:
                        del existing[(iface, channel)]
            except (AttributeError, TypeError, ValueError):
                pass

        for item in existing.values():
            item.save()

        return context
