from django.utils.translation import gettext_lazy as _

from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class ZyxelNWA50AX(cgm_devices.DeviceBase):
    """
    Zyxel NWA50AX device descriptor.
    WiFi 6 access point, popular for Freifunk networks.
    """

    identifier = 'zyxel-nwa50ax'
    name = "NWA50AX"
    manufacturer = "Zyxel"
    url = 'https://www.zyxel.com/'
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
            'name': 'zyxel_nwa50ax',
            'files': [
                '*-ramips-mt7621-zyxel_nwa50ax-squashfs-sysupgrade.bin',
            ]
        }
    }


class ZyxelWSM20(cgm_devices.DeviceBase):
    """
    Zyxel WSM20 (Multy M1) device descriptor.
    WiFi 6 mesh router, popular for Freifunk networks.
    """

    identifier = 'zyxel-wsm20'
    name = "WSM20 (Multy M1)"
    manufacturer = "Zyxel"
    url = 'https://www.zyxel.com/'
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
        cgm_devices.EthernetPort('wan0', "Wan0"),
        cgm_devices.EthernetPort('lan0', "Lan0"),
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
            'wan0': 'eth0',
            'lan0': 'eth1',
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
            'name': 'zyxel_wsm20',
            'files': [
                '*-ramips-mt7621-zyxel_wsm20-squashfs-sysupgrade.bin',
            ]
        }
    }


# Register Zyxel devices
cgm_base.register_device('openwrt', ZyxelNWA50AX)
cgm_base.register_device('openwrt', ZyxelWSM20)
