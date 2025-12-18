from django.utils.translation import gettext_lazy as _

from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class TPLinkArcherC7v2(cgm_devices.DeviceBase):
    """
    TP-Link Archer C7 v2 device descriptor.
    Popular dual-band AC router for Freifunk networks.
    """

    identifier = 'tp-archer-c7-v2'
    name = "Archer C7 (v2)"
    manufacturer = "TP-Link"
    url = 'https://www.tp-link.com/'
    architecture = 'ar71xx'
    usb = True
    radios = [
        cgm_devices.IntegratedRadio('wifi0', _("Integrated wireless radio (5 GHz)"), [
            cgm_protocols.IEEE80211AC(
                cgm_protocols.IEEE80211AC.SHORT_GI_20,
                cgm_protocols.IEEE80211AC.SHORT_GI_40,
                cgm_protocols.IEEE80211AC.RX_STBC1,
                cgm_protocols.IEEE80211AC.DSSS_CCK_40,
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
    switches = [
        cgm_devices.Switch(
            'sw0', "Switch0",
            ports=[0, 2, 3, 4, 5, 6],
            cpu_port=0,
            cpu_tagged=True,
            vlans=16,
            configurable=True,
            presets=[
                cgm_devices.SwitchPreset('default', _("Default VLAN configuration"), vlans=[
                    cgm_devices.SwitchVLANPreset(
                        'wan0', "Wan0",
                        vlan=2,
                        ports=[0, 6],
                    ),
                    cgm_devices.SwitchVLANPreset(
                        'lan0', "Lan0",
                        vlan=1,
                        ports=[0, 2, 3, 4, 5],
                    ),
                ])
            ]
        ),
    ]
    ports = []
    antennas = [
        cgm_devices.InternalAntenna(
            identifier='a1',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=5,
        ),
        cgm_devices.InternalAntenna(
            identifier='a2',
            polarization='dual',
            angle_horizontal=360,
            angle_vertical=90,
            gain=5,
        )
    ]
    port_map = {
        'openwrt': {
            'wifi0': 'radio0',
            'wifi1': 'radio1',
            'sw0': cgm_devices.SwitchPortMap('switch0', vlans='eth1.{vlan}'),
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
            'name': 'ARCHERC7V2',
            'files': [
                '*-ar71xx-generic-archer-c7-v2-squashfs-factory*.bin',
                '*-ar71xx-generic-archer-c7-v2-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v2-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v2-squashfs-sysupgrade.bin',
            ]
        },
        'lede': {
            'name': 'tplink_archer-c7-v2',
            'files': [
                '*-ar71xx-generic-archer-c7-v2-squashfs-factory*.bin',
                '*-ar71xx-generic-archer-c7-v2-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v2-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v2-squashfs-sysupgrade.bin',
            ]
        }
    }


class TPLinkArcherC7v4(TPLinkArcherC7v2):
    """
    TP-Link Archer C7 v4 device descriptor.
    """

    identifier = 'tp-archer-c7-v4'
    name = "Archer C7 (v4)"
    profiles = {
        'openwrt': {
            'name': 'ARCHERC7V4',
            'files': [
                '*-ar71xx-generic-archer-c7-v4-squashfs-factory.bin',
                '*-ar71xx-generic-archer-c7-v4-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v4-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v4-squashfs-sysupgrade.bin',
            ]
        },
        'lede': {
            'name': 'tplink_archer-c7-v4',
            'files': [
                '*-ar71xx-generic-archer-c7-v4-squashfs-factory.bin',
                '*-ar71xx-generic-archer-c7-v4-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v4-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v4-squashfs-sysupgrade.bin',
            ]
        }
    }


class TPLinkArcherC7v5(TPLinkArcherC7v2):
    """
    TP-Link Archer C7 v5 device descriptor.
    """

    identifier = 'tp-archer-c7-v5'
    name = "Archer C7 (v5)"
    profiles = {
        'openwrt': {
            'name': 'ARCHERC7V5',
            'files': [
                '*-ar71xx-generic-archer-c7-v5-squashfs-factory.bin',
                '*-ar71xx-generic-archer-c7-v5-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v5-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v5-squashfs-sysupgrade.bin',
            ]
        },
        'lede': {
            'name': 'tplink_archer-c7-v5',
            'files': [
                '*-ar71xx-generic-archer-c7-v5-squashfs-factory.bin',
                '*-ar71xx-generic-archer-c7-v5-squashfs-sysupgrade.bin',
                '*-ath79-generic-tplink_archer-c7-v5-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-c7-v5-squashfs-sysupgrade.bin',
            ]
        }
    }


class TPLinkArcherA7v5(TPLinkArcherC7v5):
    """
    TP-Link Archer A7 v5 device descriptor.
    Similar to Archer C7 v5 but sold under different branding.
    """

    identifier = 'tp-archer-a7-v5'
    name = "Archer A7 (v5)"
    profiles = {
        'openwrt': {
            'name': 'ARCHERA7V5',
            'files': [
                '*-ath79-generic-tplink_archer-a7-v5-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-a7-v5-squashfs-sysupgrade.bin',
            ]
        },
        'lede': {
            'name': 'tplink_archer-a7-v5',
            'files': [
                '*-ath79-generic-tplink_archer-a7-v5-squashfs-factory.bin',
                '*-ath79-generic-tplink_archer-a7-v5-squashfs-sysupgrade.bin',
            ]
        }
    }


# Register the TP-Link Archer devices
cgm_base.register_device('openwrt', TPLinkArcherC7v2)
cgm_base.register_device('openwrt', TPLinkArcherC7v4)
cgm_base.register_device('openwrt', TPLinkArcherC7v5)
cgm_base.register_device('openwrt', TPLinkArcherA7v5)
