"""Constants for Proxmox integration."""
from __future__ import annotations

from datetime import timedelta
from enum import Enum
from typing import Final

from homeassistant.components.sensor import SensorStateClass
from homeassistant.const import (
    ATTR_TIME,
    DATA_GIGABYTES,
    DATA_RATE_MEGABYTES_PER_SECOND,
    PERCENTAGE,
)

from .model import (
    ProxmoxBinarySensorDescription,
    ProxmoxButtonDescription,
    ProxmoxSensorDescription,
    ProxmoxSwitchDescription,
)


class Node_Type(Enum):
    """Defines Node Types as VM or Containers."""

    TYPE_VM = 0
    TYPE_CONTAINER = 1


DOMAIN = "proxmoxve"
PROXMOX_CLIENTS = "proxmox_clients"
COORDINATORS = "coordinators"

CONF_REALM = "realm"
CONF_NODE = "node"
CONF_NODES = "nodes"
CONF_VMS = "vms"
CONF_CONTAINERS = "containers"

DEFAULT_PORT = 8006
DEFAULT_REALM = "pam"
DEFAULT_VERIFY_SSL = True
DEFAULT_SCAN_INTERVAL = 60


COMMAND_REBOOT = "reboot"
COMMAND_RESUME = "resume"
COMMAND_SHUTDOWN = "shutdown"
COMMAND_START = "start"
COMMAND_STOP = "stop"
COMMAND_SUSPEND = "suspend"  # API notes 'This is experimental.'  https://pve.proxmox.com/pve-docs/api-viewer/#/nodes/{node}/lxc/{vmid}/status/suspend

VM_COMMANDS = (
    COMMAND_REBOOT,
    COMMAND_RESUME,
    COMMAND_SHUTDOWN,
    COMMAND_START,
    COMMAND_STOP,
    COMMAND_SUSPEND,
)


PROXMOX_BINARYSENSOR_TYPES: Final[tuple[ProxmoxBinarySensorDescription, ...]] = (
    ProxmoxBinarySensorDescription(
        key="status",
        icon="mdi:server",
    ),
)


PROXMOX_SENSOR_TYPES: Final[tuple[ProxmoxSensorDescription, ...]] = (
    ProxmoxSensorDescription(
        key="uptime",
        icon="mdi:database-clock-outline",
        unit_metric=ATTR_TIME,
        unit_imperial=ATTR_TIME,
        conversion=lambda x: timedelta(seconds=x),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProxmoxSensorDescription(
        key="disk",
        icon="mdi:harddisk",
        native_unit_of_measurement=DATA_GIGABYTES,
        conversion=lambda x: round(x / 1073741824, 2),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProxmoxSensorDescription(
        key="maxdisk",
        icon="mdi:harddisk-plus",
        native_unit_of_measurement=DATA_GIGABYTES,
        conversion=lambda x: round(x / 1073741824, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="diskread",
        icon="mdi:harddisk",
        native_unit_of_measurement=DATA_RATE_MEGABYTES_PER_SECOND,
        conversion=lambda x: round(x / 1048576, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="diskwrite",
        icon="mdi:harddisk",
        native_unit_of_measurement=DATA_RATE_MEGABYTES_PER_SECOND,
        conversion=lambda x: round(x / 1048576, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="cpus",
        icon="mdi:cpu-64-bit",
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="cpu",
        icon="mdi:cpu-64-bit",
        unit_metric=PERCENTAGE,
        unit_imperial=PERCENTAGE,
        native_unit_of_measurement=PERCENTAGE,
        conversion=lambda x: round(x * 100, 1),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProxmoxSensorDescription(
        key="mem",
        icon="mdi:memory",
        native_unit_of_measurement=DATA_GIGABYTES,
        conversion=lambda x: round(x / 1073741824, 2),
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProxmoxSensorDescription(
        key="maxmem",
        icon="mdi:memory",
        native_unit_of_measurement=DATA_GIGABYTES,
        conversion=lambda x: round(x / 1073741824, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="netin",
        icon="mdi:mdi:download-network-outline",
        native_unit_of_measurement=DATA_RATE_MEGABYTES_PER_SECOND,
        conversion=lambda x: round(x / 1048576, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
    ProxmoxSensorDescription(
        key="netout",
        icon="mdi:upload-network-outline",
        native_unit_of_measurement=DATA_RATE_MEGABYTES_PER_SECOND,
        conversion=lambda x: round(x / 1048576, 2),
        state_class=SensorStateClass.MEASUREMENT,
        entity_registry_enabled_default=False,
    ),
)

PROXMOX_CALCULATED_SENSOR_TYPES: Final[tuple[ProxmoxSensorDescription, ...]] = (
    ProxmoxSensorDescription(
        key="disk_pct_free",
        icon="mdi:harddisk",
        unit_metric=PERCENTAGE,
        unit_imperial=PERCENTAGE,
        native_unit_of_measurement=PERCENTAGE,
        conversion=lambda x: round(x * 100, 1),
        calculation=lambda x: 1 - x["disk"] / x["maxdisk"],
        state_class=SensorStateClass.MEASUREMENT,
    ),
    ProxmoxSensorDescription(
        key="mem_pct_free",
        icon="mdi:memory",
        unit_metric=PERCENTAGE,
        unit_imperial=PERCENTAGE,
        native_unit_of_measurement=PERCENTAGE,
        conversion=lambda x: round(x * 100, 1),
        calculation=lambda x: 1 - x["mem"] / x["maxmem"],
        state_class=SensorStateClass.MEASUREMENT,
    ),
)


PROXMOX_SWITCH_TYPES: Final[tuple[ProxmoxSwitchDescription, ...]] = (
    ProxmoxSwitchDescription(
        key="Switch",
        icon="mdi:server",
        start_command=COMMAND_START,
        stop_command=COMMAND_SHUTDOWN,
    ),
    ProxmoxSwitchDescription(
        key="Switch_Stop",
        icon="mdi:server",
        start_command=COMMAND_START,
        stop_command=COMMAND_STOP,
    ),
)

PROXMOX_BUTTON_TYPES: Final[tuple[ProxmoxButtonDescription, ...]] = (
    ProxmoxButtonDescription(
        key=COMMAND_REBOOT,
        icon="mdi:restart",
    ),
    ProxmoxButtonDescription(
        key=COMMAND_START,
        icon="mdi:server",
    ),
    ProxmoxButtonDescription(
        key=COMMAND_SHUTDOWN,
        icon="mdi:server-off",
    ),
    ProxmoxButtonDescription(
        key=COMMAND_STOP,
        icon="mdi:stop",
    ),
    ProxmoxButtonDescription(
        key=COMMAND_RESUME,
        icon="mdi:play",
        entity_registry_enabled_default=False,
    ),
    ProxmoxButtonDescription(
        key=COMMAND_SUSPEND,
        icon="mdi:pause",
        entity_registry_enabled_default=False,
    ),
)

PARSE_DATA = [
    sensor.key for sensor in PROXMOX_SENSOR_TYPES + PROXMOX_BINARYSENSOR_TYPES
] + ["name"]
PROXMOX_SENSOR_TYPES_ALL = PROXMOX_SENSOR_TYPES + PROXMOX_CALCULATED_SENSOR_TYPES
