"""The Version integration."""
from __future__ import annotations

from pyhaversion import HaVersion

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    BOARD_MAP,
    CONF_BOARD,
    CONF_CHANNEL,
    CONF_IMAGE,
    CONF_SOURCE,
    DOMAIN,
    PLATFORMS,
)
from .coordinator import VersionDataUpdateCoordinator


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the version integration from a config entry."""
    coordinator = VersionDataUpdateCoordinator(
        hass=hass,
        api=HaVersion(
            session=async_get_clientsession(hass),
            source=entry.data[CONF_SOURCE],
            image=entry.data[CONF_IMAGE],
            board=BOARD_MAP[entry.data[CONF_BOARD]],
            channel=entry.data[CONF_CHANNEL].lower(),
        ),
    )
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload the config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
