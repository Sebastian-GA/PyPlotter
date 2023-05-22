from serial_communication import SerialCommunication
import collections

from constants import *


class Device(SerialCommunication):
    def __init__(self, num_signals=1) -> None:
        super().__init__()
        self.max_data = PLOT_X_LIM

        self.signals = [
            collections.deque([0] * self.max_data, maxlen=self.max_data)
            for _ in range(num_signals)
        ]

    def _process_data(self):
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
