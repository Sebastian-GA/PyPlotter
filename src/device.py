from serial_communication import SerialCommunication
import collections

from constants import *


class Device(SerialCommunication):
    def __init__(self, num_signals=1) -> None:
        super().__init__()
        self.max_data = PLOT_X_LIM
        self.verbose = True

        self.signals = [
            collections.deque([0] * self.max_data, maxlen=self.max_data)
            for _ in range(num_signals)
        ]

        self.calibrated0 = False
        self.calibrated100 = False
        self.calibrating_status = 0.0

    def _process_data(self):
        if self.received_data == "clear":
            self.clear_data()
            return

        # Calibration
        if "calibration" in self.received_data:
            data = self.received_data.split(",")
            self.calibrated0 = data[1] == "1"
            self.calibrated100 = data[2] == "1"
            self.calibrating_status = float(data[3])

        # If not calibrated, don't process data
        if not self.calibrated0 or not self.calibrated100:
            return

        data = self.received_data.split(",")

        if len(data) != len(self.signals):
            raise ValueError(
                "Number of received points ({}) does not match number of signals ({})".format(
                    len(data), len(self.signals)
                )
            )

        for i in range(len(data)):
            try:
                self.signals[i].append(float(data[i]))
            except ValueError:
                self.signals[i].append(None)

    def clear_data(self):
        for signal in self.signals:
            for _ in range(len(signal)):
                signal.append(0)

    # Verbose is set to False to prevent printing to console
    def connect(self, port, baudrate):
        return super().connect(port, baudrate, verbose=self.verbose)

    def disconnect(self):
        return super().disconnect(verbose=self.verbose)

    def read_data(self):
        return super().read_data(verbose=self.verbose)

    def send_data(self, data, verbose=True):
        return super().send_data(data, verbose=verbose)

    def calibrate(self):
        self.calibrated0 = False
        self.calibrated100 = False
        return self.send_data("calibrate", False)
