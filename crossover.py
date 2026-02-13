import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox

# FILE BREAK: gui.py (or main.py)
class FilterConfigGUI:
    def __init__(self, driver_names, callback):
        self.driver_names = driver_names
        self.callback = callback  # Function to call with filter configs
        self.filters = []
        self.current_driver = 0
        self.root = tk.Tk()
        self.root.title("Crossover Filter Configuration")
        self.build_gui()

    def build_gui(self):
        self.root.geometry("400x250")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # Frame for driver config
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Driver label
        self.driver_label = ttk.Label(self.frame, text=f"Configure filter for {self.driver_names[self.current_driver]}")
        self.driver_label.pack(pady=5)

        # Filter type dropdown
        ttk.Label(self.frame, text="Filter Type:").pack()
        self.filter_var = tk.StringVar(value="none")
        self.filter_menu = ttk.Combobox(self.frame, textvariable=self.filter_var, 
                                       values=["none", "capacitor", "inductor", "resistor"], state="readonly")
        self.filter_menu.pack(pady=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.toggle_value_entry)

        # Value entry
        self.value_frame = ttk.Frame(self.frame)
        self.value_label = ttk.Label(self.value_frame, text="")
        self.value_label.pack(side=tk.LEFT)
        self.value_var = tk.StringVar()
        self.value_entry = ttk.Entry(self.value_frame, textvariable=self.value_var)
        self.value_entry.pack(side=tk.LEFT, padx=5)
        self.value_frame.pack(pady=5)

        # Buttons
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(pady=10)
        self.next_btn = ttk.Button(button_frame, text="Next", command=self.next_driver)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_close).pack(side=tk.LEFT)

        self.toggle_value_entry()  # Initial state
        self.root.mainloop()

    def toggle_value_entry(self, event=None):
        filter_type = self.filter_var.get()
        self.value_entry.delete(0, tk.END)
        if filter_type == "capacitor":
            self.value_label.config(text="Capacitance (µF):")
            self.value_frame.pack()
        elif filter_type == "inductor":
            self.value_label.config(text="Inductance (mH):")
            self.value_frame.pack()
        elif filter_type == "resistor":
            self.value_label.config(text="Resistance (Ω):")
            self.value_frame.pack()
        else:
            self.value_frame.pack_forget()

    def next_driver(self):
        filter_type = self.filter_var.get()
        try:
            if filter_type == "capacitor":
                C = float(self.value_var.get()) * 1e-6
                self.filters.append({'type': 'capacitor', 'C': C})
            elif filter_type == "inductor":
                L = float(self.value_var.get()) * 1e-3
                self.filters.append({'type': 'inductor', 'L': L})
            elif filter_type == "resistor":
                R = float(self.value_var.get())
                self.filters.append({'type': 'resistor', 'R': R})
            elif filter_type == "none":
                self.filters.append({'type': 'none'})
        except ValueError:
            messagebox.showerror("Error", "Invalid value entered. Using no filter.")
            self.filters.append({'type': 'none'})

        self.current_driver += 1
        if self.current_driver < len(self.driver_names):
            self.driver_label.config(text=f"Configure filter for {self.driver_names[self.current_driver]}")
            self.filter_var.set("none")
            self.value_entry.delete(0, tk.END)
            self.toggle_value_entry()
        else:
            self.root.quit()
            self.root.destroy()
            self.callback(self.filters)

    def on_close(self):
        self.root.quit()
        self.root.destroy()
        self.callback([])  # Return empty list if cancelled

def main():
    """Main function to run the crossover simulation with GUI."""
    driver_files = [
        ("Woofer", "woofer.frd", "woofer.zma"),
        ("Tweeter", "tweeter.frd", "tweeter.zma")
    ]
    
    drivers_data = []
    driver_names = []
    for name, frd_file, zma_file in driver_files:
        try:
            frd_data = read_frd(frd_file)
            zma_data = read_zma(zma_file)
            drivers_data.append((frd_data[0], frd_data[1], frd_data[2], zma_data[1], zma_data[2]))
            driver_names.append(name)
        except (FileNotFoundError, ValueError) as e:
            print(f"Error loading {name}: {e}")
            return
    
    if not drivers_data:
        print("No drivers loaded. Exiting.")
        return

    def run_simulation(filters):
        if not filters:
            print("Simulation cancelled.")
            return
        try:
            freqs, final_mags, final_phases, filtered_responses = combine_driver_responses(drivers_data, filters)
            plot_responses(freqs, final_mags, final_phases, filtered_responses, driver_names)
        except ValueError as e:
            print(f"Simulation error: {e}")

    FilterConfigGUI(driver_names, run_simulation)

if __name__ == "__main__":
    main()   