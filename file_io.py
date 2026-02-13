import numpy as np 

def read_frd(filename):
    """
    Read a .frd file and extract frequency, amplitude, and phase data.

    Parameters:
        filename (str): Path to the .frd file to be read.

    Returns:
        tuple: Three NumPy arrays (freqs, dbs, phases):
            - freqs (np.ndarray): Frequencies in Hz.
            - dbs (np.ndarray): Amplitudes in dB SPL.
            - phases (np.ndarray): Phases in degrees.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains non-numeric data.
    """
    freqs = []
    dbs = []
    phases = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() == '' or line.startswith('#'):
                    continue
                columns = line.split()
                if len(columns) >= 3:
                    freqs.append(float(columns[0]))
                    dbs.append(float(columns[1]))
                    phases.append(float(columns[2]))
    except FileNotFoundError:
        raise FileNotFoundError(f"FRD file '{filename}' not found.")
    except ValueError:
        raise ValueError(f"Invalid data in '{filename}'. Expected numeric values.")
    
    return np.array(freqs), np.array(dbs), np.array(phases)

def read_zma(filename):
    """
    Read a .zma file and extract frequency, impedance, and phase data.

    Parameters:
        filename (str): Path to the .zma file to be read.

    Returns:
        tuple: Three NumPy arrays (freqs, impedances, phases):
            - freqs (np.ndarray): Frequencies in Hz.
            - impedances (np.ndarray): Impedance magnitudes in Ohms.
            - phases (np.ndarray): Phases in degrees.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file contains non-numeric data.
    """
    freqs = []
    impedances = []
    phases = []
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                if line.strip() == '' or line.startswith('#'):
                    continue
                columns = line.split()
                if len(columns) >= 3:
                    freqs.append(float(columns[0]))
                    impedances.append(float(columns[1]))
                    phases.append(float(columns[2]))
    except FileNotFoundError:
        raise FileNotFoundError(f"ZMA file '{filename}' not found.")
    except ValueError:
        raise ValueError(f"Invalid data in '{filename}'. Expected numeric values.")
    
    return np.array(freqs), np.array(impedances), np.array(phases)