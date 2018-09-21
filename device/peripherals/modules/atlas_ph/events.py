# Import standard python modules
import time

# Import typing modules
from typing import Optional, Tuple, List, Dict, Any

# Import device utilities
from device.utilities.modes import Modes

# Import peripheral modules
from device.peripherals.classes.peripheral.events import PeripheralEvents
from device.peripherals.classes.atlas.exceptions import DriverError

LOW_POINT_CALIBRATION_EVENT = "Low Point Calibration"
MID_POINT_CALIBRATION_EVENT = "Mid Point Calibration"
HIGH_POINT_CALIBRATION_EVENT = "High Point Calibration"
CLEAR_CALIBRATION_EVENT = "Clear Calibration"


class AtlasPHEvents(PeripheralEvents):  # type: ignore
    """Event mixin for manager."""

    # Initialize var types
    mode: str

    def process_peripheral_specific_event(
        self, request: Dict[str, Any]
    ) -> Tuple[str, int]:
        """Processes peripheral specific events."""

        # Execute request
        if request["type"] == LOW_POINT_CALIBRATION_EVENT:
            return self.process_low_point_calibration_event(request)
        elif request["type"] == MID_POINT_CALIBRATION_EVENT:
            return self.process_mid_point_calibration_event(request)
        elif request["type"] == HIGH_POINT_CALIBRATION_EVENT:
            return self.process_high_point_calibration_event(request)
        elif request["type"] == CLEAR_CALIBRATION_EVENT:
            return self.process_clear_calibration_event()
        else:
            return "Unknown event request type", 400

    def process_low_point_calibration_event(
        self, request: Dict[str, Any]
    ) -> Tuple[str, int]:
        """Processes low point calibration event. Gets request parameters,
        executes request, returns response. Requires calibration value 
        to be within range 0-4."""
        self.logger.info("Processing low point calibration event")

        # Verify value in request
        try:
            value = float(request["value"])
        except KeyError as e:
            message = "Invalid request parameters: {}".format(e)
            self.logger.debug(message)
            return message, 400
        except ValueError as e:
            message = "Invalid request value: `{}`".format(request["value"])
            self.logger.debug(message)
            return message, 400

        # Verify value within valid range
        if value not in range(4, 10):
            message = "Invalid request value, not in range 4-10"
            self.logger.debug(message)
            return message, 400

        # Require mode to be in CALIBRATE
        if self.mode != Modes.CALIBRATE:
            message = "Must be in calibration mode to take single point calibration"
            self.logger.debug(message)
            return message, 400

        # Send command
        try:
            self.driver.take_low_point_calibration_reading(value)
        except DriverError:
            message = "Unable to process low point calibration event"
            self.logger.exception(message)
            self.mode = Modes.ERROR
            return message, 500

        # Successfully took low point calibration reading
        return "Successfully took low point calibration reading", 200

    def process_mid_point_calibration_event(
        self, request: Dict[str, Any]
    ) -> Tuple[str, int]:
        """Processes mid point calibration event. Gets request parameters,
        executes request, returns response. Requires calibration value 
        to be in range 4-10. """
        self.logger.info("Processing mid point calibration event")

        # Verify value in request
        try:
            value = float(request["value"])
        except KeyError as e:
            message = "Invalid request parameters: {}".format(e)
            self.logger.debug(message)
            return message, 400
        except ValueError as e:
            message = "Invalid request value: `{}`".format(request["value"])
            self.logger.debug(message)
            return message, 400

        # Verify value within valid range
        if value not in range(4, 10):
            message = "Invalid request value, not in range 4-10"
            self.logger.debug(message)
            return message, 400

        # Require mode to be in CALIBRATE
        if self.mode != Modes.CALIBRATE:
            message = "Must be in calibration mode to take single point calibration"
            self.logger.debug(message)
            return message, 400

        # Send command
        try:
            self.driver.take_mid_point_calibration_reading(value)
        except DriverError:
            message = "Unable to process mid point calibration event"
            self.logger.exception(message)
            self.mode = Modes.ERROR
            return message, 500

        # Successfully took mid point calibration reading
        return "Successfully took mid point calibration reading", 200

    def process_high_point_calibration_event(
        self, request: Dict[str, Any]
    ) -> Tuple[str, int]:
        """Processes high point calibration event. Gets request parameters,
        executes request, returns response. Requires calibration value 
        to be within range 10-14. """
        self.logger.info("Processing high point calibration event")

        # Verify value in request
        try:
            value = float(request["value"])
        except KeyError as e:
            message = "Invalid request parameters: {}".format(e)
            self.logger.debug(message)
            return message, 400
        except ValueError as e:
            message = "Invalid request value: `{}`".format(request["value"])
            self.logger.debug(message)
            return message, 400

        # Verify value within valid range
        if value not in range(10, 14):
            message = "Invalid request value, not in range 10-14"
            self.logger.debug(message)
            return message, 400

        # Require mode to be in CALIBRATE
        if self.mode != Modes.CALIBRATE:
            message = "Must be in calibration mode to take single point calibration"
            self.logger.debug(message)
            return message, 400

        # Send command
        try:
            self.driver.take_high_point_calibration_reading(value)
        except DriverError:
            message = "Unable to process high point calibration event"
            self.logger.exception(message)
            self.mode = Modes.ERROR
            return message, 500

        # Successfully took high point calibration reading
        return "Successfully took high point calibration reading", 500

    def process_clear_calibration_event(self) -> Tuple[str, int]:
        """ Processes clear calibration event. """
        self.logger.info("Processing clear calibration event")

        # Require mode to be in CALIBRATE
        if self.mode != Modes.CALIBRATE:
            message = "Must be in calibration mode to clear calibration"
            self.logger.debug(message)
            return message, 400

        # Send command
        try:
            self.driver.clear_calibration_readings()
        except DriverError:
            message = "Unable to process clear calibration event"
            self.logger.exception(message)
            self.mode = Modes.ERROR
            return message, 500

        # Successfully cleared calibration readings
        return "Successfully cleared calibration readings", 200
