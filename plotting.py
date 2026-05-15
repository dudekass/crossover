import matplotlib.pyploy as plt

def plot_responses(freqs, final_mags, final_phases, filtered_responses, driver_names, figsize=(12, 10)):
    """
    Plot raw, filtered, and combined responses.

    Parameters:
        freqs (np.ndarray): Frequencies in Hz.
        final_mags (np.ndarray): Combined magnitude in dB SPL.
        final_phases (np.ndarray): Combined phase in degrees.
        filtered_responses (list): List of (raw_mags, raw_phases, filt_mags, filt_phases).
        driver_names (list): Names of drivers.
        figsize (tuple): Figure size in inches (width, height).
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize)
    
    for i, (raw_mags, _, filt_mags, _) in enumerate(filtered_responses):
        ax1.semilogx(freqs, raw_mags, '--', label=f"{driver_names[i]} Raw", alpha=0.5)
        ax1.semilogx(freqs, filt_mags, label=f"{driver_names[i]} Filtered")
    ax1.semilogx(freqs, final_mags, 'k-', linewidth=2, label="Combined")
    ax1.grid(True)
    ax1.set_xlabel("Frequency (Hz)")
    ax1.set_ylabel("Magnitude (dB SPL)")
    ax1.set_title("Frequency Response")
    ax1.legend()
    
    for i, (_, raw_phases, _, filt_phases) in enumerate(filtered_responses):
        ax2.semilogx(freqs, raw_phases, '--', label=f"{driver_names[i]} Raw", alpha=0.5)
        ax2.semilogx(freqs, filt_phases, label=f"{driver_names[i]} Filtered")
    ax2.semilogx(freqs, final_phases, 'k-', linewidth=2, label="Combined")
    ax2.grid(True)
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Phase (degrees)")
    ax2.set_title("Phase Response")
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
