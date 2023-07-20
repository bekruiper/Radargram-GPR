import os
import json
import tkinter as tk
from tkinter import ttk

PRESETS_FOLDER = "presets"

def create_preset(preset_name, parameter_values):
    # Function to create a preset with the given name and parameter values
    preset_path = os.path.join(PRESETS_FOLDER, f"{preset_name}.json")
    with open(preset_path, 'w') as file:
        json.dump(parameter_values, file)

def erase_preset(preset_name):
    # Function to erase the selected preset
    preset_path = os.path.join(PRESETS_FOLDER, f"{preset_name}.json")
    if os.path.exists(preset_path):
        os.remove(preset_path)

def load_preset(preset_name):
    # Function to load the selected preset and set the sliders accordingly
    preset_path = os.path.join(PRESETS_FOLDER, f"{preset_name}.json")
    if os.path.exists(preset_path):
        with open(preset_path, 'r') as file:
            parameter_values = json.load(file)
            for parameter, values in parameter_values.items():
                for variable, value in values.items():
                    # Set the sliders with the values from the preset
                    # (You can implement this based on your UI design)

def create_coordinate_plane(parameter_name, variables):
    plane_window = tk.Toplevel()
    plane_window.title(f"{parameter_name} Coordinate Plane")

    # Create sliders for the variables
    sliders = {}
    for variable in variables:
        label = tk.Label(plane_window, text=f"{variable}:")
        slider = ttk.Scale(plane_window, from_=0, to=100, orient=tk.HORIZONTAL)
        label.pack()
        slider.pack()
        sliders[variable] = slider

    def read_parameters():
        # Function to read the selected parameter values
        values = {variable: slider.get() for variable, slider in sliders.items()}
        print(f"{parameter_name} Values:", values)

    # Create a button to save the preset
    def save_preset():
        parameter_values = {variable: slider.get() for variable, slider in sliders.items()}
        preset_name = parameter_name.replace(" ", "_")  # Create a valid filename
        create_preset(preset_name, {parameter_name: parameter_values})

    save_preset_button = tk.Button(plane_window, text="Save Preset", command=save_preset)
    save_preset_button.pack()

    # Create a button to erase the preset
    def erase_selected_preset():
        selected_preset = preset_var.get()
        erase_preset(selected_preset)

    erase_preset_button = tk.Button(plane_window, text="Erase Preset", command=erase_selected_preset)
    erase_preset_button.pack()

    # Create a button to read the parameter values
    read_button = tk.Button(plane_window, text="Read Parameters", command=read_parameters)
    read_button.pack()

def main():
    root = tk.Tk()
    root.title("Ground-Penetrating Radar Preprocessing GUI")

    # Parameters and their variables
    parameters = {
        "Moisture": ["Soil Moisture", "Water Table Depth", "Relative Humidity"],
        "Roughness": ["Surface Roughness"],
        "Temperature": ["Ambient Temperature", "Soil Temperature"],
        "Texture": ["Soil Texture", "Surface Texture"]
    }

    # Create buttons to open the coordinate planes for different parameters
    for parameter, variables in parameters.items():
        button = tk.Button(root, text=parameter, command=lambda p=parameter, v=variables: create_coordinate_plane(p, v))
        button.pack()

    # Create the 'presets' folder if it doesn't exist
    if not os.path.exists(PRESETS_FOLDER):
        os.makedirs(PRESETS_FOLDER)

    root.mainloop()

if __name__ == '__main__':
    main()
