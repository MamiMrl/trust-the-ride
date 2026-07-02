import customtkinter as ctk
from tkinter import Tk, font
from pycarmaker import CarMaker, Quantity
import time
from logger import SliderLogger

class TeslaStyleApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Tesla Style Slider')
        self.geometry('1920x1080')

        # Set the Tesla-style color theme
        self.configure(bg='#333333')  # Dark background
        ctk.set_appearance_mode("Dark")  # Dark theme for customtkinter
        ctk.set_default_color_theme("dark-blue")  # Blue accents

        # Verify if Gotham font is available
        available_fonts = list(font.families())
        self.custom_font = ('Gotham', 12) if 'Gotham' in available_fonts else ('Arial', 12)
        
        # Change participant id variable each time testing takes place
        self.logger = SliderLogger(participant_id="test")

        # Initialize and connect to CarMaker
        self.init_carmaker()

        # Add sliders and labels
        self.add_slider('acceleration', 'Acceleration: 0 m/s²', from_=2.0, to=7.6, row=0)  # Range taken from CarMaker and Bae Paper.
        self.add_slider('deceleration', 'Deceleration: 0 m/s²', from_=-2.0, to=-7.6, row=1)  # example range
        self.add_slider('lane_offset', 'Lane Offset: 0m    ', from_=-2.0, to=2.0, row=2)  # example range
        self.add_toggle('consider', 'Consider Overtake: OFF', values=[0, 1], row=3)  # example range
        self.add_toggle('overtake', 'Overtake: OFF         ', values=[0, 1], row=4)  # example range
        self.add_slider('steer_trq', 'Steering Torque: 0 nm', from_=-15.0, to=15.0, row=5)  # -π to π radians
        self.add_slider('steerAccel', 'Steering Acceleration: 0 deg/s²', from_=1500.0, to=20000.0, row=6)  # example range
        self.add_slider('steerVeloc', 'Steering Velocity: 0 deg/s', from_=0.0, to=10.0, row=7)  # example range
        self.add_slider('speed', 'Speed: 0 km/h      ', from_=0.0, to=250.0, row=8)  # example range
        self.add_slider('lateralAcc', 'Lateral Acceleration: 0 km/h      ', from_=0.3, to=7.6, row=9)  # example range
        #self.add_toggle('driveMode', 'Drive Mode: Off      ', values=["Default", "Neutral", "Reverse", "Aggressive"], row=9)

    def add_slider(self, name, text, from_, to, row):
        slider_frame = ctk.CTkFrame(self)
        slider_frame.pack(pady=10, padx=10, fill='x')  # Increased padding here

        slider_label = ctk.CTkLabel(slider_frame, text=text)
        slider_label.pack(side='left', pady=10, padx=10)  # Increased padding here
        slider_label.configure(font=self.custom_font)
        setattr(self, f"{name}_slider_label", slider_label)

        slider = ctk.CTkSlider(slider_frame, from_=from_, to=to, number_of_steps=1000)
        slider.pack(side='right', pady=10, padx=10, fill='x', expand=True)  # Increased padding here
        slider.configure(width = 10, height = 50)
        setattr(self, f"{name}_slider", slider)
        
        slider.bind('<B1-Motion>', getattr(self, f"update_{name}_value"))

    def add_toggle(self, name, text, values, row):
        toggle_frame = ctk.CTkFrame(self)
        toggle_frame.pack(pady=10, padx=10, fill='x')  # Increased padding here

        toggle_label = ctk.CTkLabel(toggle_frame, text=text)
        toggle_label.pack(side='left', pady=10, padx=10)  # Increased padding here
        toggle_label.configure(font=self.custom_font)
        setattr(self, f"{name}_toggle_label", toggle_label)

        button_frame = ctk.CTkFrame(toggle_frame)
        button_frame.pack(side='right', pady=10, padx=10, fill='x', expand=True)  # Increased padding here

        self.toggle_state = {name: values[0]}  # Initialize toggle state
        
        for value in values:
            button = ctk.CTkButton(button_frame, text=str(value), command=lambda v=value: self.update_toggle(name, v))
            button.pack(side='left', padx=5)
            setattr(self, f"{name}_button_{value}", button)
        
        # Initial state
        self.update_toggle_label(name, values[0])

    def update_toggle_label(self, name, value):
        toggle_label = getattr(self, f"{name}_toggle_label")
        toggle_label.configure(text=f"{toggle_label.cget('text').split(':')[0]}: {value}")
        self.toggle_state[name] = value

    def update_toggle(self, name, value):
        self.update_toggle_label(name, value)
        self.cm.DVA_write(getattr(self, f"q{name}"), value)
        self.logger.log_value_change(self.get_log_values())

    def get_log_values(self):
        # Ensure values are logged in the correct order
        return [
            self.acceleration_slider.get(),
            self.deceleration_slider.get(),
            self.lane_offset_slider.get(),
            self.toggle_state.get('consider', None),
            self.toggle_state.get('overtake', None),
            self.steer_trq_slider.get(),
            self.steerAccel_slider.get(),
            self.steerVeloc_slider.get(),
            self.speed_slider.get(),
            self.lateralAcc_slider.get(),
        ]

    # ------------------- Update Value -------------------      

    def update_acceleration_value(self, event):
        value = self.acceleration_slider.get()
        self.acceleration_slider_label.configure(text=f"Acceleration: {value:.2f} m/s²")
        # self.cm.DVA_write(self.qacceleration, value)
        self.logger.log_value_change(self.get_log_values())

    def update_deceleration_value(self, event):
        value = self.deceleration_slider.get()
        self.deceleration_slider_label.configure(text=f"Deceleration: {value:.2f} m/s²")
        # self.cm.DVA_write(self.qdeceleration, value)
        self.logger.log_value_change(self.get_log_values())

    def update_lane_offset_value(self, event):
        value = self.lane_offset_slider.get()
        self.lane_offset_slider_label.configure(text=f"Lane Offset: {value:.2f}")
        # self.cm.DVA_write(self.qlane_offset, value)
        self.logger.log_value_change(self.get_log_values())

    def update_steer_trq_value(self, event):
        value = self.steer_trq_slider.get()
        self.steer_trq_slider_label.configure(text=f"Steering Torque: {value:.2f} rad")
        # self.cm.DVA_write(self.qsteer_trq, value)
        self.logger.log_value_change(self.get_log_values())

    def update_steerAccel_value(self, event):
        value = self.steerAccel_slider.get()
        self.steerAccel_slider_label.configure(text=f"Steering Acceleration: {value:.2f}")
        # self.cm.DVA_write(self.qsteerAccel, value)
        self.logger.log_value_change(self.get_log_values())

    def update_steerVeloc_value(self, event):
        value = self.steerVeloc_slider.get()
        self.steerVeloc_slider_label.configure(text=f"Steering Velocity: {value:.2f}")
        # self.cm.DVA_write(self.qsteerVeloc, value)
        self.logger.log_value_change(self.get_log_values())

    def update_speed_value(self, event):
        value = self.speed_slider.get()
        self.speed_slider_label.configure(text=f"Speed: {value:.2f}")
        # self.cm.DVA_write(self.qspeed, value)
        self.logger.log_value_change(self.get_log_values())

    def update_lateralAcc_value(self, event):
        value = self.lateralAcc_slider.get()
        self.lateralAcc_slider_label.configure(text=f"Lateral Acceleration: {value:.2f}")
        self.cm.DVA_write(self.qlateralAcc, value)
        self.logger.log_value_change(self.get_log_values())

    # ------------------- CarMaker -------------------

    def init_carmaker(self):
        # Change IP_ADDRESS to 192.168.1.240 in Lab
        IP_ADDRESS = "localhost"
        PORT = 16660
        self.cm = CarMaker(IP_ADDRESS, PORT)
        self.cm.connect()
        self.qacceleration = Quantity("Driver.ReCon.Accel", Quantity.FLOAT)
        self.qdeceleration = Quantity("Driver.ReCon.Decel", Quantity.FLOAT)
        self.qlane_offset = Quantity("DM.LaneOffset", Quantity.FLOAT)
        self.qconsider = Quantity("Driver.ReCon.Trf_Consider", Quantity.INT)
        self.qovertake = Quantity("Driver.ReCon.Trf_Overtake", Quantity.INT)
        self.qsteer_trq = Quantity("Driver.Steer.Trq", Quantity.FLOAT)
        self.qsteerAccel = Quantity("Driver.Steer.AngAcc", Quantity.FLOAT)
        self.qsteerVeloc = Quantity("Driver.Steer.AngVel", Quantity.FLOAT)
        self.qspeed = Quantity("Driver.ReCon.Speed", Quantity.FLOAT)
        self.qlateralAcc = Quantity("Driver.ReCon.DriveChar.CF_axy", Quantity.FLOAT)

# Run the application
if __name__ == "__main__":
    app = TeslaStyleApp()
    app.mainloop()

