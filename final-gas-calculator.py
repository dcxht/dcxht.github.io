import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

class AboutWindow:
    def __init__(self, parent):
        about_window = tk.Toplevel(parent)
        about_window.title("About - Gas Density Calculator")
        about_window.resizable(False, False)
        
        about_window.transient(parent)
        about_window.grab_set()
        
        text = """Gas Density Equations

Main Formula:
Density (g/L) = (P × M) / (R × T)

where:
P = Pressure (atm)
M = Molar mass (g/mol)
R = 0.08206 L⋅atm/(mol⋅K)
T = Temperature (K) = °C + 273.15

Molar Masses (g/mol):
O₂: 32.0    N₂: 28.01
He: 4.002   CO₂: 44.01

For Mixtures:
• Avg Molar Mass = Σ(percentage × molar mass)/100
• Gas Density = Mix Density × (gas percentage/100)"""

        # Optimized size to show all content without scrolling
        label_frame = ttk.Frame(about_window, padding="20")
        label_frame.pack(fill='both', expand=True)
        
        # Using a label instead of text widget to avoid scroll
        text_label = ttk.Label(
            label_frame, 
            text=text,
            font=('Courier', 14),
            justify='left'
        )
        text_label.pack(pady=(0, 10))

        # Larger close button
        close_btn = ttk.Button(
            label_frame, 
            text="Close", 
            command=about_window.destroy, 
            width=20
        )
        close_btn.pack(pady=(0, 10))
        
        # Position window
        about_window.update_idletasks()
        width = about_window.winfo_width()
        height = about_window.winfo_height()
        x = (about_window.winfo_screenwidth() // 2) - (width // 2)
        y = (about_window.winfo_screenheight() // 2) - (height // 2)
        about_window.geometry(f'{width}x{height}+{x}+{y}')

class MultiGasDensityCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Gas Density Calculator")
        self.root.resizable(False, False)
        
        self.R = 0.08206
        self.MOLAR_MASSES = {
            'O₂': 32.0,
            'N₂': 28.01,
            'He': 4.002,
            'CO₂': 44.01
        }

        # Define common styles
        self.large_font = tkfont.Font(size=12, weight='bold')
        self.extra_large_font = tkfont.Font(size=16, weight='bold')
        
        # Main frame with increased padding
        main_frame = ttk.Frame(root, padding="15")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # About button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0,10))
        about_btn = ttk.Button(button_frame, text="About", command=lambda: AboutWindow(root), width=12)
        about_btn.pack(side=tk.LEFT, padx=2)
        
        # Parameters frame
        param_frame = ttk.Frame(main_frame)
        param_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(param_frame, text="P (atm):", font=self.large_font, width=8).grid(row=0, column=0, sticky=tk.W)
        self.pressure_var = tk.StringVar(value="1.0")
        ttk.Entry(param_frame, textvariable=self.pressure_var, width=10, font=self.large_font).grid(row=0, column=1, padx=5, pady=2)
        
        ttk.Label(param_frame, text="T (°C):", font=self.large_font, width=8).grid(row=0, column=2, sticky=tk.W)
        self.temperature_var = tk.StringVar(value="25.0")
        ttk.Entry(param_frame, textvariable=self.temperature_var, width=10, font=self.large_font).grid(row=0, column=3, padx=5, pady=2)
        
        # Gas percentage inputs in 2x2 grid
        gas_frame = ttk.LabelFrame(main_frame, text="Gas %", padding="10", style='Large.TLabelframe')
        gas_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.gas_vars = {}
        gases = list(self.MOLAR_MASSES.keys())
        for i in range(2):  # rows
            for j in range(2):  # columns
                idx = i * 2 + j
                if idx < len(gases):
                    gas = gases[idx]
                    ttk.Label(gas_frame, text=f"{gas}:", font=self.large_font, width=5).grid(row=i, column=j*2, sticky=tk.W, padx=(5,0))
                    self.gas_vars[gas] = tk.StringVar(value="0.0")
                    if gas == 'N₂':
                        self.gas_vars[gas].set("79.0")
                    elif gas == 'O₂':
                        self.gas_vars[gas].set("21.0")
                    ttk.Entry(gas_frame, textvariable=self.gas_vars[gas], width=10, font=self.large_font).grid(row=i, column=j*2+1, padx=(0,10), pady=5)
        
        # Calculate button
        calc_button = ttk.Button(main_frame, text="Calculate", command=self.calculate, width=20)
        calc_button.grid(row=3, column=0, pady=10)
        
        # Mixture density frame
        mix_frame = ttk.Frame(main_frame)
        mix_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(mix_frame, text="Mix Density:", font=self.extra_large_font).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.mixture_density_var = tk.StringVar()
        mix_label = ttk.Label(mix_frame, textvariable=self.mixture_density_var, font=self.extra_large_font)
        mix_label.grid(row=0, column=1, sticky=tk.E)
        ttk.Label(mix_frame, text="g/L", font=self.extra_large_font).grid(row=0, column=2, sticky=tk.E, padx=(5,5))
        
        # Individual gas results
        results_frame = ttk.LabelFrame(main_frame, text="Individual Gas Densities (g/L)", padding="10", style='Large.TLabelframe')
        results_frame.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.gas_density_vars = {}
        for i, gas in enumerate(self.MOLAR_MASSES.keys()):
            self.gas_density_vars[gas] = tk.StringVar()
            ttk.Label(results_frame, text=f"{gas}:", font=self.large_font).grid(row=i, column=0, sticky=tk.W, padx=5)
            ttk.Label(results_frame, textvariable=self.gas_density_vars[gas], width=12, font=self.large_font).grid(row=i, column=1, sticky=tk.E, padx=5, pady=3)

        # Credit label (slightly larger than before but still small)
        credit_style = ttk.Style()
        credit_style.configure("Small.TLabel", font=('Arial', 9))
        credit_label = ttk.Label(main_frame, text="CHIP'N'STRIPS™ per TGB", style="Small.TLabel")
        credit_label.grid(row=6, column=0, pady=(10,2))

        # Configure style for LabelFrame headers
        style = ttk.Style()
        style.configure('Large.TLabelframe.Label', font=self.large_font)

    def celsius_to_kelvin(self, celsius):
        return celsius + 273.15

    def calculate(self):
        try:
            pressure = float(self.pressure_var.get())
            temperature_celsius = float(self.temperature_var.get())
            temperature_kelvin = self.celsius_to_kelvin(temperature_celsius)
            
            if temperature_kelvin <= 0:
                raise ValueError("Temperature cannot be below absolute zero")
            if pressure <= 0:
                raise ValueError("Pressure must be positive")
            
            gas_percentages = {}
            total_percentage = 0
            for gas, var in self.gas_vars.items():
                percentage = float(var.get())
                if percentage < 0 or percentage > 100:
                    raise ValueError(f"{gas} percentage must be between 0 and 100")
                gas_percentages[gas] = percentage
                total_percentage += percentage
            
            if abs(total_percentage - 100) > 0.01:
                messagebox.showerror("Error", f"Gas percentages must sum to 100% (current sum: {total_percentage:.1f}%)")
                return
            
            avg_molar_mass = sum(self.MOLAR_MASSES[gas] * (percentage/100) 
                               for gas, percentage in gas_percentages.items())
            
            mixture_density = (pressure * avg_molar_mass) / (self.R * temperature_kelvin)
            self.mixture_density_var.set(f"{mixture_density:.4f}")
            
            for gas, percentage in gas_percentages.items():
                gas_density = mixture_density * (percentage/100)
                self.gas_density_vars[gas].set(f"{gas_density:.4f}")
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.mixture_density_var.set("Error")
            for var in self.gas_density_vars.values():
                var.set("Error")

def main():
    root = tk.Tk()
    MultiGasDensityCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main()
