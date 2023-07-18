import customtkinter as ctk
from constants import *
from device import Device
from plot import Plot
from threading import Thread, Event
import time


microcontroller = Device()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(TITLE)
        self.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.minsize(WIDTH, HEIGHT)
        self.resizable(1, 1)
        ctk.set_appearance_mode(APPEREANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)

        self.protocol("WM_DELETE_WINDOW", self.close)  # Close everything

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        # -------- Options Frame -------- #
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)
        self.options_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        # self.options_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.options_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.options_frame.grid_columnconfigure(0, weight=1, pad=10)
        self.options_frame.grid_columnconfigure(1, weight=1)
        for i in range(7):
            self.options_frame.grid_rowconfigure(i, pad=10)

        # TITLE
        title = ctk.CTkLabel(
            self.options_frame,
            text=TITLE,
            font=FONT,
            fg_color="transparent",
            justify="center",
        )
        title.grid(row=0, column=0, columnspan=2, sticky="we", padx=10)
        self.options_frame.grid_rowconfigure(0, pad=25)

        # PORT ENTRY
        ctk.CTkLabel(self.options_frame, text="Port:", fg_color="transparent").grid(
            row=1, column=0, sticky="w"
        )
        self.port_entry = ctk.CTkComboBox(
            self.options_frame,
            values=microcontroller.get_ports(),
            state="readonly",
            justify="center",
        )
        self.port_entry.grid(row=1, column=1)

        # BAUDRATE ENTRY
        ctk.CTkLabel(
            self.options_frame,
            text="Baudrate:",
            fg_color="transparent",
        ).grid(row=2, column=0, sticky="w")
        self.baudrate_entry = ctk.CTkComboBox(
            self.options_frame,
            values=microcontroller.get_baudrates(),
            state="readonly",
            justify="center",
        )
        self.baudrate_entry.grid(row=2, column=1)

        # CONNECT BUTTON
        self.connect_button = ctk.CTkButton(
            self.options_frame,
            text="Connect",
            command=self.connect,
        )
        self.connect_button.grid(row=3, column=0, columnspan=2, pady=(10, 0), ipady=2)

        # REFRESH BUTTON
        self.refresh_button = ctk.CTkButton(
            self.options_frame,
            text="Refresh",
            command=self.refresh,
        )
        self.refresh_button.grid(row=4, column=0, columnspan=2, pady=(0, 10), ipady=2)

        # START/PAUSE BUTTON
        self.start_pause_button = ctk.CTkButton(
            self.options_frame,
            text="Pause",
            command=self.pause,
        )
        self.start_pause_button.grid(row=5, column=0, columnspan=2, ipady=2)

        # CLEAR BUTTON
        self.clear_button = ctk.CTkButton(
            self.options_frame,
            text="Clear",
            command=self.clear,
        )
        self.clear_button.grid(row=6, column=0, columnspan=2, ipady=2)

        self.refresh()  # Update port and baudrate entries

        # -------- Plot -------- #
        self.plot = Plot(self, microcontroller)
        self.plot.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)

        # -------- Threads -------- #
        self.thread = Thread(target=self.update_interface)
        self.flag = Event()

    def run(self):
        self.thread.daemon = True
        self.flag.set()
        self.thread.start()
        self.mainloop()

    def connect(self):
        port = self.port_entry.get()
        baudrate = self.baudrate_entry.get()
        if port == "" or baudrate == "":
            return

        if microcontroller.connect(port, baudrate):
            self.connect_button.configure(text="Disconnect", command=self.disconnect)
            self.refresh_button.configure(state="disabled")
            self.port_entry.configure(state="disabled")
            self.baudrate_entry.configure(state="disabled")

    def disconnect(self):
        microcontroller.disconnect()
        self.connect_button.configure(text="Connect", command=self.connect)
        self.refresh_button.configure(state="normal")
        self.port_entry.configure(state="normal")
        self.baudrate_entry.configure(state="normal")

    def refresh(self):
        self.port_entry.configure(values=microcontroller.get_ports())
        if len(self.port_entry.cget("values")) > 0:
            self.port_entry.set(self.port_entry.cget("values")[0])
        self.baudrate_entry.configure(values=microcontroller.get_baudrates())
        if len(self.baudrate_entry.cget("values")) >= 12:
            self.baudrate_entry.set(self.baudrate_entry.cget("values")[12])

    def pause(self):
        self.plot.pause()
        self.start_pause_button.configure(text="Start", command=self.start)

    def start(self):
        self.plot.start()
        self.start_pause_button.configure(text="Pause", command=self.pause)

    def clear(self):
        self.plot.clear()

    def close(self):
        self.disconnect()
        self.flag.clear()
        self.thread.join()
        self.thread = None
        self.quit()

    def update_interface(self):
        while self.flag.is_set():
            if microcontroller.errorFlag.is_set():  # Disconnect if error
                self.disconnect()
                microcontroller.errorFlag.clear()

            if not microcontroller.is_connected():  # Refresh list of ports
                if set(microcontroller.get_ports()) != set(
                    self.port_entry.cget("values")
                ):
                    self.refresh()

            time.sleep(0.1)


if __name__ == "__main__":
    app = App()
    app.run()
