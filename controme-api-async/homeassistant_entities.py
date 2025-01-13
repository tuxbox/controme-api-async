"""The models required for the Controme API data."""

class ContromeEntity:
    """base controme entity."""

    def __init__(self, id: str, name: str, floor: str, room: str) -> None:
        """Initialize the entity."""
        self._state: float = 0.0
        self._id = id
        self._name = name
        self._floor = floor
        self._room = room
        self._last_updated: str | None = None

    @property
    def id(self) -> str:
        """Get the id of the entity."""
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        """Set the id of the entity."""
        self._id = value

    @property
    def name(self) -> str:
        """Get the name of the entity."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the id of the entity."""
        self._name = value

    @property
    def floor(self) -> str:
        """Get the floor of the entity."""
        return self._floor

    @floor.setter
    def floor(self, value: str) -> None:
        """Set the id of the entity."""
        self._floor = value

    @property
    def room(self) -> str:
        """Get the room of the entity."""
        return self._room

    @room.setter
    def room(self, value: str) -> None:
        """Set the id of the entity."""
        self._room = value

    @property
    def state(self) -> float:
        """Get the state of the entity."""
        return self._state

    @state.setter
    def state(self, value: float) -> None:
        """Set the id of the entity."""
        self._state = value

    @property
    def last_updated(self) -> str | None:
        """Get the last updated time of the entity."""
        return self._last_updated

    @last_updated.setter
    def last_updated(self, value: str) -> None:
        """Set the id of the entity."""
        self._last_updated = value

    def format_value(self, value: float) -> str:
        """Format a value to conform with the Controme API limitations."""
        result = "00.00"
        if value is not None:
            int_value = int(value)
            # Weird calculation of decimals due to stupid controme api limitations
            decimal_value = int((value - int(value)) * 10000)
            if decimal_value < 625:
                decimal_value = 0
            elif decimal_value < 1875:
                decimal_value = 12
            elif decimal_value < 3125:
                decimal_value = 25
            elif decimal_value < 4375:
                decimal_value = 37
            elif decimal_value < 5625:
                decimal_value = 50
            elif decimal_value < 6875:
                decimal_value = 62
            elif decimal_value < 8125:
                decimal_value = 75
            elif decimal_value < 9375:
                decimal_value = 87
            else:
                int_value = int_value + 1
                decimal_value = 0
            result = f"{int_value:02d}.{decimal_value:02d}"
        return result


class ContromeSensor(ContromeEntity):
    """Representation of a Controme entity."""

    def __init__(self, id: str, name: str, floor: str, room: str) -> None:
        """Initialize the entity."""
        super().__init__(id, name, floor, room)
        self._state = 0.0

    @property
    def state(self) -> float:
        """Get the state of the entity."""
        return self._state

    @state.setter
    def state(self, value: float) -> None:
        """Set the state of the entity."""
        self._state = value

    def get_formatted_state(self) -> str:
        """Get the formatted state of the entity."""
        return self.format_value(self._state)


class ContromeThermostat(ContromeSensor):
    """Representation of a Controme thermostat."""

    def __init__(self, id: str, name: str, floor: str, room: str) -> None:
        """Initialize the thermostat."""
        super().__init__(id, name, floor, room)
        self._state = 0.0
        self._target_state = 0.0

    @property
    def target_state(self) -> float:
        """Get the target state of the thermostat."""
        return self._target_state

    @target_state.setter
    def target_state(self, value: float) -> None:
        """Set the target state of the thermostat."""
        self._target_state = value

    def get_formatted_target_state(self) -> str:
        """Get the formatted target state of the thermostat."""
        return self.format_value(self._target_state)
