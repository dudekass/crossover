import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np

# Matplotlib imports for embedding charts into Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Import your backend modules:
from file_io import read_frd, read_zma
from simulation import combine_driver_responses
# (Your filters.py is used indirectly by simulation.py; that's fine)

class XSimGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Crossover Simulator (MVP)")

        # Store driver data and filter settings here
        self.drivers_data = []   # list of tuples: (freqs, mags, phases, imp_mags, imp_phases)
        self.driver_names = []   # e.g. ["Woofer", "Tweeter"]
        self.filters = []        # parallel list of filter dicts, one per driver

        # Build the main window layout
        self.build_menu()
        self.build_main_layout()

        self.root.mainloop()

    def build_menu(self):
        """Create a simple menu bar with 'Load Driver' and 'Exit' options."""
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(label="Load Driver...", command=self.load_driver)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menubar)

    def build_main_layout(self):
        """
        Main layout:
          Left frame: 
            - List of drivers 
            - Filter config controls 
            - 'Apply Filter' and 'Update Plot' buttons
          Right frame: 
            - Embedded Matplotlib figure
        """
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # -- Left Panel (Driver list + Filter config)
        left_frame = ttk.Frame(main_frame, padding=5)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Driver list
        ttk.Label(left_frame, text="Loaded Drivers:").pack(anchor=tk.W)
        self.driver_listbox = tk.Listbox(left_frame, height=6)
        self.driver_listbox.pack(fill=tk.X, pady=5)

        # Filter type & value
        ttk.Label(left_frame, text="Filter Type:").pack(anchor=tk.W)
        self.filter_var = tk.StringVar(value="none")
        self.filter_menu = ttk.Combobox(
            left_frame, textvariable=self.filter_var, 
            values=["none", "capacitor", "inductor", "resistor"], 
            state="readonly"
        )
        self.filter_menu.pack(pady=5)

        ttk.Label(left_frame, text="Filter Value:").pack(anchor=tk.W)
        self.filter_val_var = tk.StringVar()
        self.filter_val_entry = ttk.Entry(left_frame, textvariable=self.filter_val_var)
        self.filter_val_entry.pack(pady=5)

        # Buttons
        ttk.Button(left_frame, text="Apply Filter", command=self.set_filter).pack(pady=(10,5))
        ttk.Button(left_frame, text="Update Plot", command=self.update_plot).pack()

        # -- Right Panel (Plot area)
        self.plot_frame = ttk.Frame(main_frame, padding=5)
        self.plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Create a blank figure & axes
        self.fig = Figure(figsize=(6, 4))
        self.ax1 = self.fig.add_subplot(211)
        self.ax2 = self.fig.add_subplot(212)

        # Embed figure in Tk canvas
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_driver(self):
        """Prompt the user to select FRD and ZMA files, then store them and create a default filter."""
        # Ask for FRD file
        frd_path = filedialog.askopenfilename(title="Open FRD File", 
                                              filetypes=[("FRD Files","*.frd"), ("All Files","*.*")])
        if not frd_path:
            return

        # Ask for ZMA file
        zma_path = filedialog.askopenfilename(title="Open ZMA File", 
                                              filetypes=[("ZMA Files","*.zma"), ("All Files","*.*")])
        if not zma_path:
            return

        # Ask for a name for this driver (could also do a simple dialog or just auto-name)
        name = tk.simpledialog.askstring("Driver Name", "Enter a name/label for this driver:")
        if not name:
            name = f"Driver {len(self.driver_names)+1}"

        # Read data
        try:
            freqs, mags, phases = read_frd(frd_path)
            _, imp_mags, imp_phases = read_zma(zma_path)
        except Exception as e:
            messagebox.showerror("Load Error", f"Could not read driver data:\n{e}")
            return

        # Store in lists
        self.driver_names.append(name)
        self.drivers_data.append((freqs, mags, phases, imp_mags, imp_phases))
        self.filters.append({'type': 'none'})  # Default: no filter

        # Show in listbox
        self.driver_listbox.insert(tk.END, name)

    def set_filter(self):
        """Apply the chosen filter type & value to the selected driver."""
        sel = self.driver_listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a driver first.")
            return
        index = sel[0]

        ftype = self.filter_var.get()
        val_str = self.filter_val_var.get().strip()

        try:
            if ftype == "capacitor":
                # Value in microfarads => convert to Farads
                c_val = float(val_str) * 1e-6
                self.filters[index] = {'type': 'capacitor', 'C': c_val}
            elif ftype == "inductor":
                # Value in millihenries => convert to Henries
                l_val = float(val_str) * 1e-3
                self.filters[index] = {'type': 'inductor', 'L': l_val}
            elif ftype == "resistor":
                r_val = float(val_str)
                self.filters[index] = {'type': 'resistor', 'R': r_val}
            else:
                # "none"
                self.filters[index] = {'type': 'none'}
        except ValueError:
            messagebox.showerror("Invalid Value", "Please enter a valid numeric filter value.")
            return

        messagebox.showinfo("Filter Applied", 
                            f"Filter '{ftype}' applied to driver '{self.driver_names[index]}'.")

    def update_plot(self):
        """Recalculate and plot the combined response of all drivers (with their filters)."""
        if not self.drivers_data:
            return

        # Combine responses
        try:
            freqs, final_mags, final_phases, filtered_responses = combine_driver_responses(
                self.drivers_data, self.filters
            )
        except Exception as e:
            messagebox.showerror("Simulation Error", f"Could not combine responses:\n{e}")
            return

        # Clear old plots
        self.ax1.clear()
        self.ax2.clear()

        # Plot each driver: raw vs filtered
        for i, (raw_mags, raw_phases, filt_mags, filt_phases) in enumerate(filtered_responses):
            self.ax1.semilogx(freqs, raw_mags, '--', alpha=0.5, 
                              label=f"{self.driver_names[i]} Raw")
            self.ax1.semilogx(freqs, filt_mags, label=f"{self.driver_names[i]} Filtered")

            self.ax2.semilogx(freqs, raw_phases, '--', alpha=0.5, 
                              label=f"{self.driver_names[i]} Raw")
            self.ax2.semilogx(freqs, filt_phases, label=f"{self.driver_names[i]} Filtered")

        # Plot combined
        self.ax1.semilogx(freqs, final_mags, 'k-', linewidth=2, label="Combined")
        self.ax2.semilogx(freqs, final_phases, 'k-', linewidth=2, label="Combined")

        # Axis labels, titles, etc.
        self.ax1.set_title("Frequency Response")
        self.ax1.set_xlabel("Frequency (Hz)")
        self.ax1.set_ylabel("Magnitude (dB SPL)")
        self.ax1.legend()
        self.ax1.grid(True)

        self.ax2.set_title("Phase Response")
        self.ax2.set_xlabel("Frequency (Hz)")
        self.ax2.set_ylabel("Phase (degrees)")
        self.ax2.legend()
        self.ax2.grid(True)

        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    XSimGUI()