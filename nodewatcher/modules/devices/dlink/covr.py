from django.utils.translation import gettext_lazy as _

from nodewatcher.core.generator.cgm import base as cgm_base, protocols as cgm_protocols, devices as cgm_devices


class DLinkCOVRX1860A1(cgm_devices.DeviceBase):
    """
    D-Link COVR-X1860 A1 device descriptor.
    WiFi 6 mesh router, popular for Freifunk networks.
    """

    identifier = 'dlink-covr-x1860-a1'
    name = "COVR-X1860 (A1)"
    manufacturer = "D-Link"
    url = 'https://www.dlink.com/'
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
    switches = [
        cgm_devices.Switch(
            'sw0', "Switch0",
            ports=[0, 1, 2, 3, 4, 6],
            cpu_port=6,
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
                        ports=[1, 2, 3, 4, 6],
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
            'sw0': cgm_devices.SwitchPortMap('switch0', vlans='eth0.{vlan}'),
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
            'name': 'dlink_covr-x1860-a1',
            'files': [
                '*-ramips-mt7621-dlink_covr-x1860-a1-squashfs-factory.bin',
                '*-ramips-mt7621-dlink_covr-x1860-a1-squashfs-sysupgrade.bin',
            ]
        }
    }


# Register D-Link COVR devices
cgm_base.register_device('openwrt', DLinkCOVRX1860A1)
