import serial, serial.tools.list_ports
from threading import Thread, Event
import time


class SerialCommunication:
    def __init__(self) -> None:
        self.device = None

        self.received_data = None

        self.thread = None
        self.flag = Event()
        self.errorFlag = Event()
        self.errorFlag.clear()

    def get_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def get_baudrates(self):
        return list(map(str, serial.Serial.BAUDRATES))

    def is_connected(self):
        if self.device is None:
            return False
        return self.device.is_open

    def connect(self, port, baudrate, verbose=True):
        if self.is_connected():
            if verbose:
                print("Device is already connected")
            return False

        try:
            self.device = serial.Serial(port, baudrate, timeout=0.1)
            self.device.open()
        except serial.SerialException:
            if verbose:
                print("Permission denied. Maybe the port is already in use.")
        except Exception as e:
            if verbose:
                print("Error while connecting to device. Error message:", str(e))

        if self.is_connected():
            self.start_thread()
            if verbose:
                print("Connected to {} at {} baud".format(port, baudrate))
            return True

        if verbose:
            print("Failed to connect")
        return False

    def disconnect(self, verbose=True):
        if not self.is_connected():
            if verbose:
                print("Device is already disconnected")
            return False

        self.stop_thread()
        self.device.close()
        if verbose:
            print("Disconnected")
        return True

    def start_thread(self):
        self.thread = Thread(target=self.read_data)
        self.thread.setDaemon(True)
        self.flag.set()
        self.thread.start()

    def stop_thread(self):
        if self.thread is not None:
            self.flag.clear()
            self.thread.join()
            self.thread = None

    def read_data(self, verbose=True):
        while self.flag.is_set() and self.device.is_open:
            try:
                data = self.device.readline().decode("utf-8").strip()
                # data = self.readline().decode("utf-8").strip()
                if len(data) > 0:
                    self.received_data = data
                    self._process_data()
                    if verbose:
                        print("Recieved: {}".format(data))
            except serial.SerialException:
                self.errorFlag.set()
                if verbose:
                    print("Device was disconnected")
                break
            except Exception as e:
                if verbose:
                    print("Error while reading data. Error message:", str(e))
                    # Shows error but the program still runs and try to read data
                pass

        if verbose:
            print("Finished reading data")
        return

    def _process_data(self):
        pass

    def send_data(self, data, verbose=True):
        if self.device.is_open:
            sent_data = data + "\n"
            self.device.write(sent_data.encode("utf-8"))
            if verbose:
                print("Sent: {}".format(data))
            return True
        else:
            if verbose:
                print("Device is not connected")
            return False

    # def readline(self, tout=1):
    #     """Have to use this function instead of self.device.readline() because
    #     self.device.readline() will block the program if there is no data to read
    #     or maybe that happens when baudrate is not correct

    #     Ref: https://stackoverflow.com/questions/3437303/python-pyserial-read-line-timeout#3437411
    #     """

    #     buff = self.device.read(128)
    #     tic = time.time()
    #     while ((time.time() - tic) < tout) and not ("\n" in buff):
    #         buff += self.device.read(128)

    #     return buff
