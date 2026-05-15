# CrossoverSim — Speaker Crossover Network Simulator for macOS
 
A Python-based crossover network design and simulation tool for speaker builders, developed as a macOS-compatible alternative to XSim — a widely used Windows-only crossover simulator with no Mac equivalent.
 
CrossoverSim loads real driver measurement data, applies passive crossover filter components (capacitors, inductors, resistors), computes the combined frequency and phase response across all drivers, and plots the result in real time. It is designed for the speaker DIY community and supports industry-standard measurement file formats out of the box.
 
---
 
## The Problem
 
XSim is the go-to free crossover simulator for speaker DIY enthusiasts — but it is Windows-only. Mac users have historically had no equivalent lightweight, free tool for passive crossover design using real driver measurement data. CrossoverSim was built to fill that gap.
 
---
 
## Features
 
- **FRD / ZMA file support** — reads industry-standard frequency response (`.frd`) and impedance (`.zma`) measurement files exported from tools like REW, ARTA, and VituixCAD
- **Passive crossover components** — capacitor (high-pass), inductor (low-pass), and resistor (attenuation) filters applied per driver
- **Impedance-based transfer function math** — filter responses computed from real driver impedance data using H = Z_load / (Z_filter + Z_load), not simplified approximations
- **Complex response summation** — driver responses summed correctly in the complex domain (magnitude + phase) before conversion to dB
- **Frequency interpolation** — mismatched frequency arrays between drivers are automatically interpolated to a common reference grid
- **Live embedded plots** — frequency response and phase response update in real time inside the GUI without launching separate windows
- **Multi-driver support** — load any number of drivers (woofer, tweeter, midrange, etc.) and configure each independently
- **macOS native** — runs on any platform with Python 3, with no Windows dependencies
---
 
## Project Structure
 
```
crossover-sim/
├── xsim_gui.py       # Main GUI — driver loader, filter config, embedded live plots
├── crossover.py      # Original step-through GUI (per-driver configuration flow)
├── simulation.py     # Core engine — combines driver responses with filter effects
├── filters.py        # Filter transfer functions — capacitor, inductor, resistor
├── file_io.py        # FRD and ZMA file parsers
├── plotting.py       # Standalone matplotlib plotting (non-GUI mode)
└── README.md
```
 
---
 
## How It Works
 
### Signal chain per driver:
```
.frd file (frequency response)   +   .zma file (impedance)
              ↓                                ↓
         raw SPL (dB)              complex impedance Z_load(f)
              ↓
    Filter transfer function:  H(f) = Z_load / (Z_filter + Z_load)
              ↓
    Filtered SPL = raw SPL + 20·log10(|H|)
    Filtered phase = raw phase + ∠H
              ↓
    Convert to complex: A·e^(jφ)
```
 
### Combined response:
```
Total(f) = Σ [ A_i(f) · e^(jφ_i(f)) ]   for all drivers i
Combined SPL   = 20·log10(|Total|)
Combined phase = ∠Total
```
 
This correctly models acoustic summation including phase interactions between drivers — the key factor in crossover design that determines lobing, cancellation, and overall system response.
 
---
 
## Setup
 
**Requirements:** Python 3.8+
 
```bash
git clone <repository-url>
cd crossover-sim
pip install numpy matplotlib
```
 
---
 
## Running
 
**GUI mode (recommended):**
```bash
python xsim_gui.py
```
 
1. Go to **File → Load Driver**
2. Select the `.frd` file for your driver
3. Select the `.zma` file for the same driver
4. Enter a name (e.g. "Woofer", "Tweeter")
5. Repeat for each driver
6. Select a driver in the list, choose a filter type and value, click **Apply Filter**
7. Click **Update Plot** to see the combined response
**Standalone mode (no GUI, scripted):**
```bash
python crossover.py
```
Requires `woofer.frd`, `woofer.zma`, `tweeter.frd`, `tweeter.zma` in the working directory.
 
---
 
## File Format Reference
 
### FRD (Frequency Response Data)
```
# Frequency(Hz)  SPL(dB)  Phase(deg)
20.0             82.3     -12.4
25.0             83.1     -11.8
...
```
 
### ZMA (Impedance Data)
```
# Frequency(Hz)  Impedance(Ohm)  Phase(deg)
20.0             6.2             18.3
25.0             6.5             19.1
...
```
Lines beginning with `#` and blank lines are ignored. Compatible with REW, ARTA, Dayton Audio DATS, and VituixCAD exports.
 
---
 
## Filter Reference
 
| Component  | Effect       | Unit    | GUI Input |
|------------|--------------|---------|-----------|
| Capacitor  | High-pass    | µF      | e.g. 33   |
| Inductor   | Low-pass     | mH      | e.g. 0.5  |
| Resistor   | Attenuation  | Ω       | e.g. 4.7  |
 
---
 
## Roadmap
 
- [ ] Zobel network (impedance equalization) support
- [ ] Second and third-order filter topologies (L-pad, Butterworth, Linkwitz-Riley)
- [ ] Thiele-Small parameter input for enclosure-corrected response
- [ ] Export combined response as FRD for use in other tools
- [ ] Project save/load (driver + filter configurations)
- [ ] Acoustic offset / time alignment between drivers
---
 
## Background
 
This project grew out of practical frustration — designing crossovers for [Maaleh](https://github.com/[your-profile]) speaker builds on a Mac with no suitable free tool available. The physics and math are grounded in standard passive network theory and complex acoustic summation, the same foundation used by commercial crossover design software.
 
---
 
## Author
 
Eduarda (Duda) [Last Name]
Computer Engineering, Brigham Young University
[your email] · [your LinkedIn] · [your GitHub]
