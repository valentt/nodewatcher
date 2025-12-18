from django.utils.translation import gettext_lazy as _

from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class UniFi6Lite(cgm_devices.DeviceBase):
    """
    Ubiquiti UniFi 6 Lite device descriptor.
    WiFi 6 access point, popular for Freifunk networks.
    """

    identifier = 'ubnt-unifi-6-lite'
    name = "UniFi 6 Lite"
    manufacturer = "Ubiquiti"
    url = 'https://www.ui.com/'
    architecture = 'ramips_mt7621'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio (5 GHz)"), [
            cgm_protocols.IEEE80211AX(
                cgm_protocols.IEEE80211AX.SHORT_GI_20,
                cgm_protocols.IEEE80211AX.SHORT_GI_40,
                cgm_protocols.IEEE80211AX.SHORT_GI_80,
                cgm_protocols.IEEE80211AX.RX_STBC1,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna1")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ]),
        cgm_devices.IntegratedRadio('wifi1', _("Integrated wireless radio (2.4 GHz)"), [
            cgm_protocols.IEEE80211AX(
                cgm_protocols.IEEE80211AX.SHORT_GI_20,
                cgm_protocols.IEEE80211AX.SHORT_GI_40,
                cgm_protocols.IEEE80211AX.RX_STBC1,
            )
        ], [
            cgm_devices.AntennaConnector('a2', "Antenna2")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ])
    ]
    switches = []
    ports = [
        cgm_devices.EthernetPort('lan0', "Lan0")
    ]
    antennas = [
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=4,
        ),
        cgm_devices.InternalAntenna(
            identifier='a2',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=4,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wifi1': 'radio1',
            'lan0': 'eth0',
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211',
            'wifi1': 'mac80211',
        }
    }
    profiles = {
        'openwrt': {
            'name': 'ubnt_unifi-6-lite',
            'files': [
                '*-ramips-mt7621-ubnt_unifi-6-lite-squashfs-sysupgrade.bin',
            ]
        }
    }


class UniFiACLite(cgm_devices.DeviceBase):
    """
    Ubiquiti UniFi AC Lite device descriptor.
    WiFi AC access point, very popular for Freifunk networks.
    """

    identifier = 'ubnt-unifi-ac-lite'
    name = "UniFi AC Lite"
    manufacturer = "Ubiquiti"
    url = 'https://www.ui.com/'
    architecture = 'ath79'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio (5 GHz)"), [
            cgm_protocols.IEEE80211AC(
                cgm_protocols.IEEE80211AC.SHORT_GI_20,
                cgm_protocols.IEEE80211AC.SHORT_GI_40,
                cgm_protocols.IEEE80211AC.RX_STBC1,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna1")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ]),
        cgm_devices.IntegratedRadio('wifi1', _("Integrated wireless radio (2.4 GHz)"), [
            cgm_protocols.IEEE80211BGN(
                cgm_protocols.IEEE80211BGN.SHORT_GI_20,
                cgm_protocols.IEEE80211BGN.SHORT_GI_40,
                cgm_protocols.IEEE80211BGN.RX_STBC1,
                cgm_protocols.IEEE80211BGN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a2', "Antenna2")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ])
    ]
    switches = []
    ports = [
        cgm_devices.EthernetPort('lan0', "Lan0")
    ]
    antennas = [
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=3,
        ),
        cgm_devices.InternalAntenna(
            identifier='a2',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=3,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wifi1': 'radio1',
            'lan0': 'eth0',
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211',
            'wifi1': 'mac80211',
        }
    }
    profiles = {
        'openwrt': {
            'name': 'ubnt_unifiac-lite',
            'files': [
                '*-ath79-generic-ubnt_unifiac-lite-squashfs-sysupgrade.bin',
            ]
        }
    }


class UniFiACMesh(UniFiACLite):
    """
    Ubiquiti UniFi AC Mesh device descriptor.
    Outdoor WiFi AC mesh access point.
    """

    identifier = 'ubnt-unifi-ac-mesh'
    name = "UniFi AC Mesh"
    profiles = {
        'openwrt': {
            'name': 'ubnt_unifiac-mesh',
            'files': [
                '*-ath79-generic-ubnt_unifiac-mesh-squashfs-sysupgrade.bin',
            ]
        }
    }


class UniFiACMeshPro(cgm_devices.DeviceBase):
    """
    Ubiquiti UniFi AC Mesh Pro device descriptor.
    Outdoor WiFi AC mesh access point with 3x3 MIMO.
    """

    identifier = 'ubnt-unifi-ac-mesh-pro'
    name = "UniFi AC Mesh Pro"
    manufacturer = "Ubiquiti"
    url = 'https://www.ui.com/'
    architecture = 'ath79'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio (5 GHz)"), [
            cgm_protocols.IEEE80211AC(
                cgm_protocols.IEEE80211AC.SHORT_GI_20,
                cgm_protocols.IEEE80211AC.SHORT_GI_40,
                cgm_protocols.IEEE80211AC.RX_STBC1,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna1")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ]),
        cgm_devices.IntegratedRadio('wifi1', _("Integrated wireless radio (2.4 GHz)"), [
            cgm_protocols.IEEE80211BGN(
                cgm_protocols.IEEE80211BGN.SHORT_GI_20,
                cgm_protocols.IEEE80211BGN.SHORT_GI_40,
                cgm_protocols.IEEE80211BGN.RX_STBC1,
                cgm_protocols.IEEE80211BGN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a2', "Antenna2")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ])
    ]
    switches = []
    ports = [
        cgm_devices.EthernetPort('lan0', "Lan0"),
        cgm_devices.EthernetPort('lan1', "Lan1"),
    ]
    antennas = [
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=8,
        ),
        cgm_devices.InternalAntenna(
            identifier='a2',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=3,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wifi1': 'radio1',
            'lan0': 'eth0',
            'lan1': 'eth1',
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211',
            'wifi1': 'mac80211',
        }
    }
    profiles = {
        'openwrt': {
            'name': 'ubnt_unifiac-mesh-pro',
            'files': [
                '*-ath79-generic-ubnt_unifiac-mesh-pro-squashfs-sysupgrade.bin',
            ]
        }
    }


# Register Ubiquiti devices
cgm_base.register_device('openwrt', UniFi6Lite)
cgm_base.register_device('openwrt', UniFiACLite)
cgm_base.register_device('openwrt', UniFiACMesh)
cgm_base.register_device('openwrt', UniFiACMeshPro)
