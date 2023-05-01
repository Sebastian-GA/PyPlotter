from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from constants import *
from serial_communication import SerialCommunication

# from plot import Plot


raspberry_pi = SerialCommunication()


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title(TITLE)
        self.root.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.root.minsize(WIDTH, HEIGHT)
        self.root.resizable(0, 0)

        self.root.configure(bg=BG)
        title = Label(self.root, text=TITLE, bg=BG, fg=FG, font=FONT)
        title.pack()

        # -------- Buttons -------- #
        self.options_frame = Frame(self.root, bg=BG)
        self.options_frame.pack()

        # CONNECT BUTTON
        self.connect_button = Button(
            self.options_frame,
            text="Connect",
            bg=BG,
            fg=FG,
            font=FONT,
            command=self.connect,
        )
        self.connect_button.pack()

        # REFRESH BUTTON
        self.refresh_button = Button(
            self.options_frame,
            text="Refresh",
            bg=BG,
            fg=FG,
            font=FONT,
            command=self.refresh,
        )
        self.refresh_button.pack()

        # -------- Entries -------- #
        # PORT ENTRY
        self.port_entry = ttk.Combobox(
            self.options_frame,
            values=raspberry_pi.get_ports(),
            state="readonly",
            font=FONT,
        )
        self.port_entry.pack()
        self.port_entry.current(0)

        # BAUDRATE ENTRY
        self.baudrate_entry = ttk.Combobox(
            self.options_frame,
            values=raspberry_pi.get_baudrates(),
            state="readonly",
            font=FONT,
        )
        self.baudrate_entry.pack()
        self.baudrate_entry.current(12)

        # -------- Plot -------- #
        # self.plot = Plot(self.root, raspberry_pi)

    def run(self):
        self.root.mainloop()

    def connect(self):
        port = self.port_entry.get()
        baudrate = self.baudrate_entry.get()
        if raspberry_pi.connect(port, baudrate):
            self.connect_button.configure(text="Disconnect", command=self.disconnect)
            self.refresh_button.configure(state="disabled")
            self.port_entry.configure(state="disabled")
            self.baudrate_entry.configure(state="disabled")

    def disconnect(self):
        raspberry_pi.disconnect()
        self.connect_button.configure(text="Connect", command=self.connect)
        self.refresh_button.configure(state="normal")
        self.port_entry.configure(state="normal")
        self.baudrate_entry.configure(state="normal")

    def refresh(self):
        self.port_entry.configure(values=raspberry_pi.get_ports())
        self.port_entry.current(0)
        self.baudrate_entry.configure(values=raspberry_pi.get_baudrates())
        self.baudrate_entry.current(12)


if __name__ == "__main__":
    window = MainWindow()
    window.run()
