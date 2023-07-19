import customtkinter as ctk
from constants import *
from threading import Thread, Event
import time


class CalibrationWindow(ctk.CTkToplevel):
    def __init__(self, master, device, *args):
        super().__init__(master, *args)
        self.title("Calibration")
        self.geometry("300x100")
        self.resizable(0, 0)

        self.protocol("WM_DELETE_WINDOW", self.close)

        self.master = master
        self.device = device

        # -------- Widgets -------- #
        # Title
        ctk.CTkLabel(self, text="Put switches in calibration position").pack(pady=10)

        # Label
        self.label = ctk.CTkLabel(self, text="Calibrating for 0°...")
        self.label.pack()

        # Progressbar
        self.progressbar = ctk.CTkProgressBar(self, orientation="horizontal")
        self.progressbar.set(0)
        self.progressbar.pack()

        # -------- Thread -------- #
        self.thread = Thread(target=self._run)
        self.flag = Event()
        self.thread.daemon = True
        self.flag.set()
        self.thread.start()

    def _run(self):
        self.master.disable_interface()
        self.focus_set()
        time.sleep(2);
        self.device.calibrate()

        while self.flag.is_set():
            self.focus_set()
            if self.device.calibrated0 and self.device.calibrated100:
                break
            if not self.device.calibrated0:
                self.label.configure(text="Calibrating for 0°...")
                self.progressbar.set(self.device.calibrating_status)
            elif not self.device.calibrated100:
                self.label.configure(text="Calibrating for 100°...")
                self.progressbar.set(self.device.calibrating_status)

            time.sleep(0.01)

        self.close()

    def close(self):
        self.master.enable_interface()
        if self.device.calibrated0 and self.device.calibrated100:
            self.master.connected()
        else:
            self.master.disconnect()

        self.flag.clear()
        time.sleep(0.02)
        self.thread = None
        self.destroy()
