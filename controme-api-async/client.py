"""Controme client."""

from logging import getLogger

from aiohttp import ClientSession

from .const import API_RESPONSE_FIELD_TEMPERATURE
from .homeassistant_entities import ContromeEntity, ContromeSensor, ContromeThermostat

_LOGGER = getLogger(__name__)

class ContromeClient:
    """Controme client."""

    def __init__(
        self,
        session: ClientSession,
        host: str,
        port: int,
        username: str,
        password: str,
        home_id: int,
    ) -> None:
        """Initialize the client."""
        self._session = session
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._home_id = home_id

    async def get_entities(self, room_id: str = "") -> list[ContromeEntity]:
        """Get all entities."""
        suffix = ""
        if room_id != "":
            suffix = f"{room_id}/"
        async with self._session.get(
            f"http://{self._host}/get/json/v1/{self._home_id}/temps/{suffix}"
        ) as response:
            if response.status == 200:
                data = await response.json()
                entities: list[ContromeEntity] = []
                for etage in data:
                    floor = etage["etagenname"]
                    for raum in etage["raeume"]:
                        thermostat = ContromeThermostat(
                            id=raum["id"],
                            name=raum["name"],
                            floor=floor,
                            room=raum["name"],
                        )
                        thermostat.target_state = raum["solltemperatur"]
                        # just to work around a codespell error
                        thermostat.state = raum[
                            API_RESPONSE_FIELD_TEMPERATURE[
                                0 : len(API_RESPONSE_FIELD_TEMPERATURE) - 1
                            ]
                        ]
                        for sensor in raum["sensoren"]:
                            if sensor["raumtemperatursensor"]:
                                cs = ContromeSensor(
                                    id=sensor["name"],
                                    name=f"Isttemperatur {raum["name"]}",
                                    floor=floor,
                                    room=raum["name"],
                                )
                                cs.state = (
                                    0.0
                                    if sensor["wert"] is None
                                    else round(sensor["wert"], 1)
                                )
                                cs = sensor["letzte_uebertragung"]
                                thermostat.last_updated = sensor["letzte_uebertragung"]
                                entities.append(cs)
                            else:
                                s = ContromeSensor(
                                    id=sensor["name"],
                                    name=f'{sensor["beschreibung"]} {raum["name"]}',
                                    floor=floor,
                                    room=raum["name"],
                                )
                                s.state = (
                                    0.0
                                    if sensor["wert"] is None
                                    else round(sensor["wert"], 1)
                                )
                                s.last_updated = sensor["letzte_uebertragung"]
                                entities.append(s)

                        entities.append(thermostat)
        return entities

    async def update_state(self, sensor: ContromeSensor) -> None:
        """Update the state of a sensor."""
        # value = sensor.get_formatted_state()

    async def update_target_state(
        self, thermostat: ContromeThermostat, target_value: float
    ) -> None:
        """Update the target state of a thermostat."""
        formatted_target_value = f"{target_value:.2f}"
        _LOGGER.debug(
            "Updating target state for %s to %s", thermostat.id, formatted_target_value
        )
        payload = {
            "user": self._username,
            "password": self._password,
            "ziel": formatted_target_value,
            "duration": 0,  # Example duration, adjust as needed
        }
        async with self._session.post(
            f"http://{self._host}/set/json/v1/{self._home_id}/ziel/{thermostat.id}/",
            data=payload,
            headers={
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8"
            },
        ) as response:
            if response.status == 200:
                _LOGGER.info(
                    "Successfully updated target state to %s for thermostat ID %s",
                    thermostat.get_formatted_target_state(),
                    thermostat.id,
                )
            else:
                _LOGGER.error("Error updating target state")
                _LOGGER.error(response.status)
                _LOGGER.error(await response.text())
