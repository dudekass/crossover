import numpy as np

def apply_capacitor_filter(freqs, C, imp_mags, imp_phases):
    """
    Apply a series capacitor (high-pass filter) to a driver's response.

    Parameters:
        freqs (np.ndarray): Frequencies in Hz.
        C (float): Capacitance in Farads.
        imp_mags (np.ndarray): Driver impedance magnitudes in Ohms.
        imp_phases (np.ndarray): Driver impedance phases in degrees.

    Returns:
        tuple: (mag_dB, phase_deg)
            - mag_dB (np.ndarray): Filter magnitude effect in dB.
            - phase_deg (np.ndarray): Filter phase effect in degrees.

    Raises:
        ValueError: If capacitance is not positive.
    """
    if C <= 0:
        raise ValueError("Capacitance must be positive.")
    
    w = 2 * np.pi * freqs
    Z_C = 1 / (1j * w * C)
    Z_load = imp_mags * np.exp(1j * np.radians(imp_phases))
    H = Z_load / (Z_C + Z_load)
    
    return 20 * np.log10(np.abs(H)), np.angle(H, deg=True)

def apply_inductor_filter(freqs, L, imp_mags, imp_phases):
    """
    Apply a series inductor (low-pass filter) to a driver's response.

    Parameters:
        freqs (np.ndarray): Frequencies in Hz.
        L (float): Inductance in Henries.
        imp_mags (np.ndarray): Driver impedance magnitudes in Ohms.
        imp_phases (np.ndarray): Driver impedance phases in degrees.

    Returns:
        tuple: (mag_dB, phase_deg)
            - mag_dB (np.ndarray): Filter magnitude effect in dB.
            - phase_deg (np.ndarray): Filter phase effect in degrees.

    Raises:
        ValueError: If inductance is not positive.
    """
    if L <= 0:
        raise ValueError("Inductance must be positive.")
    
    w = 2 * np.pi * freqs
    Z_L = 1j * w * L
    Z_load = imp_mags * np.exp(1j * np.radians(imp_phases))
    H = Z_load / (Z_L + Z_load)
    
    return 20 * np.log10(np.abs(H)), np.angle(H, deg=True)

def apply_resistor_filter(freqs, R, imp_mags, imp_phases):
    """
    Apply a series resistor to a driver's response (attenuates signal).

    Parameters:
        freqs (np.ndarray): Frequencies in Hz.
        R (float): Resistance in Ohms.
        imp_mags (np.ndarray): Driver impedance magnitudes in Ohms.
        imp_phases (np.ndarray): Driver impedance phases in degrees.

    Returns:
        tuple: (mag_dB, phase_deg)
            - mag_dB (np.ndarray): Filter magnitude effect in dB.
            - phase_deg (np.ndarray): Filter phase effect in degrees.

    Raises:
        ValueError: If resistance is negative.
    """
    if R < 0:
        raise ValueError("Resistance cannot be negative.")
    
    Z_R = R
    Z_load = imp_mags * np.exp(1j * np.radians(imp_phases))
    H = Z_load / (Z_R + Z_load)
    
    return 20 * np.log10(np.abs(H)), np.angle(H, deg=True)