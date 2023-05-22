import serial, serial.tools.list_ports
from threading import Thread, Event


class SerialCommunication:
    def __init__(self) -> None:
        self.device = None

        self.received_data = None

        self.thread = None
        self.signal = Event()

    def get_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def get_baudrates(self):
        return serial.Serial.BAUDRATES

    def connect(self, port, baudrate):
        if self.device is not None and self.device.is_open:
            print("Device is already connected")
            return False

        try:
            self.device = serial.Serial(port, baudrate)
            self.device.timeout = 0.1
            self.device.open()
        except:
            pass
        if self.device.is_open:
            self.start_thread()
            print("Connected to {} at {} baud".format(port, baudrate))
            return True
        print("Failed to connect")
        return False

    def disconnect(self):
        if self.device is None or not self.device.is_open:
            print("Device is already disconnected")
            return False

        self.stop_thread()
        self.device.close()
        print("Disconnected")

    def start_thread(self):
        self.thread = Thread(target=self.read_data)
        self.thread.setDaemon(True)
        self.signal.set()
        self.thread.start()

    def stop_thread(self):
        if self.thread is not None:
            self.signal.clear()
            self.thread.join()
            self.thread = None

    def read_data(self):
        try:
            while self.signal.is_set() and self.device.is_open:
                data = self.device.readline().decode("utf-8").strip()
                if len(data) > 0:
                    self.received_data = data
                    self._process_data()
                    print("Recieved: {}".format(data))
        except:
            pass
        return "Finished"

    def _process_data(self):
        pass

    def send_data(self, data):
        if self.device.is_open:
            sent_data = data + "\n"
            self.device.write(sent_data.encode("utf-8"))
            print("Sent: {}".format(data))
            return True
        else:
            print("Device is not connected")
            return False
