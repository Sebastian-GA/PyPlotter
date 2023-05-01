import serial, serial.tools.list_ports
from threading import Thread, Event


class SerialCommunication:
    def __init__(self) -> None:
        self.device = None
        self.recieved_data = None
        self.sent_data = None

        self.thread = None
        self.signal = Event()

    def get_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def get_baudrates(self):
        return serial.Serial.BAUDRATES

    def connect(self, port, baudrate):
        self.device = serial.Serial(port, baudrate)
        self.device.timeout = 0.1
        try:
            self.device.open()
        except:
            pass
        if self.device.is_open:
            self.start_thread()
            print("Connected to {} at {} baud".format(port, baudrate))
            return True
        return False

    def disconnect(self):
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
                    self.recieved_data = data
                    print("Recieved: {}".format(data))
        except:
            pass
        return "Finished"

    def send_data(self, data):
        if self.device.is_open:
            self.sent_data = data + "\n"
            self.device.write(self.sent_data.encode("utf-8"))
            print("Sent: {}".format(data))
            return True
        else:
            print("Device is not connected")
            return False

