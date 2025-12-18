from django.utils.translation import gettext_lazy as _

from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class TPLinkCPE210v1(cgm_devices.DeviceBase):
    """
    TP-Link CPE210 v1 device descriptor.
    """

    identifier = 'tp-cpe210-v1'
    name = "CPE210 (v1)"
    manufacturer = "TP-Link"
    url = 'http://www.tp-link.com/'
    architecture = 'ar71xx'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio"), [
            cgm_protocols.IEEE80211BGN(
                cgm_protocols.IEEE80211BGN.SHORT_GI_20,
                cgm_protocols.IEEE80211BGN.SHORT_GI_40,
                cgm_protocols.IEEE80211BGN.RX_STBC1,
                cgm_protocols.IEEE80211BGN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna0")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ])
    ]
    switches = [
        cgm_devices.Switch(
            'sw0', "Switch0",
            ports=[0, 4, 5],
            cpu_port=0,
            cpu_tagged=True,
            vlans=16,
            presets=[
                cgm_devices.SwitchPreset('default', _("Default VLAN configuration"), vlans=[
                    cgm_devices.SwitchVLANPreset(
                        'wan0', "Wan0",
                        vlan=2,
                        ports=[0, 5],
                    ),
                    cgm_devices.SwitchVLANPreset(
                        'lan0', "Lan0",
                        vlan=1,
                        ports=[0, 4],
                    )
                ])
            ]
        )
    ]
    ports = []
    antennas = [
        # TODO: This information is probably not correct
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='horizontal',
            angle_horizontal=360,
            angle_vertical=75,
            gain=2,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'sw0': cgm_devices.SwitchPortMap('switch0', vlans='eth0.{vlan}'),
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211'
        }
    }
    profiles = {
        'openwrt': {
            'name': 'CPE510',
            'files': [
                '*-ar71xx-generic-cpe210-220-510-520-squashfs-factory.bin',
                '*-ar71xx-generic-cpe210-220-510-520-squashfs-sysupgrade.bin'
            ]
        },
        'lede': {
            'name': 'cpe210-220',
            'files': [
                '*-ar71xx-generic-cpe210-220-squashfs-factory.bin',
                '*-ar71xx-generic-cpe210-220-squashfs-sysupgrade.bin'
            ]
        }
    }


class TPLinkCPE220v1(TPLinkCPE210v1):
    """
    TP-Link CPE220 v1 device descriptor.
    """

    identifier = 'tp-cpe220-v1'
    name = "CPE220 (v1)"


class TPLinkCPE510v1(TPLinkCPE210v1):
    """
    TP-Link CPE510 v1 device descriptor.
    """

    identifier = 'tp-cpe510-v1'
    name = "CPE510 (v1)"
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio"), [
            cgm_protocols.IEEE80211AN(
                cgm_protocols.IEEE80211AN.SHORT_GI_20,
                cgm_protocols.IEEE80211AN.SHORT_GI_40,
                cgm_protocols.IEEE80211AN.RX_STBC1,
                cgm_protocols.IEEE80211AN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna0")
        ], [
            cgm_devices.DeviceRadio.MultipleSSID,
        ])
    ]
    profiles = {
        'lede': {
            'name': 'cpe510-520',
            'files': [
                '*-ar71xx-generic-cpe510-520-squashfs-factory.bin',
                '*-ar71xx-generic-cpe510-520-squashfs-sysupgrade.bin'
            ]
        }
    }


class TPLinkCPE520v1(TPLinkCPE510v1):
    """
    TP-Link CPE520 v1 device descriptor.
    """

    identifier = 'tp-cpe520-v1'
    name = "CPE520 (v1)"

class TPLinkCPE210v2(cgm_devices.DeviceBase):
    """
    TP-Link CPE210 v2 device descriptor.
    Outdoor 2.4GHz 300Mbps 9dBi CPE.
    """

    identifier = 'tp-cpe210-v2'
    name = "CPE210 (v2)"
    manufacturer = "TP-Link"
    url = 'http://www.tp-link.com/'
    architecture = 'ath79'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio"), [
            cgm_protocols.IEEE80211BGN(
                cgm_protocols.IEEE80211BGN.SHORT_GI_20,
                cgm_protocols.IEEE80211BGN.SHORT_GI_40,
                cgm_protocols.IEEE80211BGN.RX_STBC1,
                cgm_protocols.IEEE80211BGN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna0")
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
            angle_horizontal=70,
            angle_vertical=45,
            gain=9,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wan0': 'eth0',
            'lan0': 'eth1',
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211'
        }
    }
    profiles = {
        'openwrt': {
            'name': 'tplink_cpe210-v2',
            'files': [
                '*-ath79-generic-tplink_cpe210-v2-squashfs-factory.bin',
                '*-ath79-generic-tplink_cpe210-v2-squashfs-sysupgrade.bin'
            ]
        }
    }


class TPLinkCPE210v3(TPLinkCPE210v2):
    """
    TP-Link CPE210 v3 device descriptor.
    """

    identifier = 'tp-cpe210-v3'
    name = "CPE210 (v3)"
    profiles = {
        'openwrt': {
            'name': 'tplink_cpe210-v3',
            'files': [
                '*-ath79-generic-tplink_cpe210-v3-squashfs-factory.bin',
                '*-ath79-generic-tplink_cpe210-v3-squashfs-sysupgrade.bin'
            ]
        }
    }


class TPLinkCPE510v2(cgm_devices.DeviceBase):
    """
    TP-Link CPE510 v2 device descriptor.
    Outdoor 5GHz 300Mbps 13dBi CPE.
    """

    identifier = 'tp-cpe510-v2'
    name = "CPE510 (v2)"
    manufacturer = "TP-Link"
    url = 'http://www.tp-link.com/'
    architecture = 'ath79'
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio"), [
            cgm_protocols.IEEE80211AN(
                cgm_protocols.IEEE80211AN.SHORT_GI_20,
                cgm_protocols.IEEE80211AN.SHORT_GI_40,
                cgm_protocols.IEEE80211AN.RX_STBC1,
                cgm_protocols.IEEE80211AN.DSSS_CCK_40,
            )
        ], [
            cgm_devices.AntennaConnector('a1', "Antenna0")
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
            angle_horizontal=45,
            angle_vertical=30,
            gain=13,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wan0': 'eth0',
            'lan0': 'eth1',
        }
    }
    drivers = {
        'openwrt': {
            'wifi0': 'mac80211'
        }
    }
    profiles = {
        'openwrt': {
            'name': 'tplink_cpe510-v2',
            'files': [
                '*-ath79-generic-tplink_cpe510-v2-squashfs-factory.bin',
                '*-ath79-generic-tplink_cpe510-v2-squashfs-sysupgrade.bin'
            ]
        }
    }


class TPLinkCPE510v3(TPLinkCPE510v2):
    """
    TP-Link CPE510 v3 device descriptor.
    """

    identifier = 'tp-cpe510-v3'
    name = "CPE510 (v3)"
    profiles = {
        'openwrt': {
            'name': 'tplink_cpe510-v3',
            'files': [
                '*-ath79-generic-tplink_cpe510-v3-squashfs-factory.bin',
                '*-ath79-generic-tplink_cpe510-v3-squashfs-sysupgrade.bin'
            ]
        }
    }


# Register the TP-Link CPE devices.
cgm_base.register_device('openwrt', TPLinkCPE210v1)
cgm_base.register_device('openwrt', TPLinkCPE220v1)
cgm_base.register_device('openwrt', TPLinkCPE510v1)
cgm_base.register_device('openwrt', TPLinkCPE520v1)
cgm_base.register_device('openwrt', TPLinkCPE210v2)
cgm_base.register_device('openwrt', TPLinkCPE210v3)
cgm_base.register_device('openwrt', TPLinkCPE510v2)
cgm_base.register_device('openwrt', TPLinkCPE510v3)
