from tkinter import Tk, Frame, Button, Label, ttk, PhotoImage
from constants import *
from serial_communication import SerialCommunication
from plot import Plot


raspberry_pi = SerialCommunication()


class MainWindow:
    def __init__(self):
        self.root = Tk()
        self.root.title(TITLE)
        self.root.geometry("{}x{}".format(WIDTH, HEIGHT))
        self.root.minsize(WIDTH, HEIGHT)
        self.root.resizable(1, 1)

        self.root.configure(bg=BG1, width=WIDTH, height=HEIGHT)
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.root.protocol("WM_DELETE_WINDOW", self.close)  # Close everything

        # -------- Options Frame -------- #
        self.right_frame = Frame(self.root, bg=BG2)
        self.right_frame.grid(row=0, column=1, sticky="nse", padx=20, pady=20)

        self.options_frame = Frame(self.right_frame, bg=BG2)
        self.options_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        for i in range(4):
            self.options_frame.rowconfigure(i, pad=10)
            self.options_frame.columnconfigure(0, pad=10)

        title = Label(
            self.options_frame, text=TITLE, bg=BG2, fg=FG, font=FONT, justify="center"
        )
        title.grid(row=0, column=0, columnspan=2, sticky="we", padx=10)

        # -------- Entries -------- #
        # PORT ENTRY
        Label(self.options_frame, text="Port:", bg=BG2, fg=FG).grid(
            row=1, column=0, sticky="w"
        )
        self.port_entry = ttk.Combobox(
            self.options_frame,
            values=raspberry_pi.get_ports(),
            state="readonly",
            justify="center",
            width=10,
        )
        self.port_entry.current(0)
        self.port_entry.grid(row=1, column=1)

        # BAUDRATE ENTRY
        Label(self.options_frame, text="Baudrate:", bg=BG2, fg=FG).grid(
            row=2, column=0, sticky="w"
        )
        self.baudrate_entry = ttk.Combobox(
            self.options_frame,
            values=raspberry_pi.get_baudrates(),
            state="readonly",
            justify="center",
            width=10,
        )
        self.baudrate_entry.current(12)
        self.baudrate_entry.grid(row=2, column=1)

        # -------- Buttons -------- #
        # CONNECT BUTTON
        self.connect_button = Button(
            self.options_frame,
            text="Connect",
            bg=BG1,
            fg=FG,
            command=self.connect,
        )
        self.connect_button.grid(
            row=3, column=0, columnspan=2, sticky="we", padx=20, pady=2, ipady=2
        )

        # REFRESH BUTTON
        self.refresh_button = Button(
            self.options_frame,
            text="Refresh",
            bg=BG1,
            fg=FG,
            command=self.refresh,
        )
        self.refresh_button.grid(
            row=4, column=0, columnspan=2, sticky="we", padx=20, pady=2, ipady=2
        )

        # -------- Plot -------- #
        # self.plot = Plot(self.root, raspberry_pi)
        # self.plot.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

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

    def close(self):
        self.disconnect()
        self.root.quit()


if __name__ == "__main__":
    window = MainWindow()
    window.run()
