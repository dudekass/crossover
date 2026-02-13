def combine_driver_responses(drivers_data, filters):
    """
    Combine multiple driver responses with filter effects into a final frequency response.

    Parameters:
        drivers_data (list): List of tuples (freqs, mags, phases, imp_mags, imp_phases).
        filters (list): List of filter dicts with 'type' and value ('C', 'L', 'R').

    Returns:
        tuple: (freqs, final_mags, final_phases, filtered_responses)
            - freqs (np.ndarray): Common frequency array in Hz.
            - final_mags (np.ndarray): Combined magnitude in dB SPL.
            - final_phases (np.ndarray): Combined phase in degrees.
            - filtered_responses (list): List of (raw_mags, raw_phases, filt_mags, filt_phases).

    Raises:
        ValueError: If number of drivers and filters don’t match or filter type is unknown.
    """
    if len(drivers_data) != len(filters):
        raise ValueError("Number of drivers and filters must match.")
    
    ref_freqs = drivers_data[0][0]
    num_freqs = len(ref_freqs)
    total_response = np.zeros(num_freqs, dtype=complex)
    filtered_responses = []
    
    for (freqs, mags, phases, imp_mags, imp_phases), filter in zip(drivers_data, filters):
        if not np.array_equal(freqs, ref_freqs):
            imp_mags = np.interp(ref_freqs, freqs, imp_mags)
            imp_phases = np.interp(ref_freqs, freqs, imp_phases)
            mags = np.interp(ref_freqs, freqs, mags)
            phases = np.interp(ref_freqs, freqs, phases)
        else:
            freqs = ref_freqs
        
        if filter['type'] == 'capacitor':
            filter_mag, filter_phase = apply_capacitor_filter(freqs, filter['C'], imp_mags, imp_phases)
        elif filter['type'] == 'inductor':
            filter_mag, filter_phase = apply_inductor_filter(freqs, filter['L'], imp_mags, imp_phases)
        elif filter['type'] == 'resistor':
            filter_mag, filter_phase = apply_resistor_filter(freqs, filter['R'], imp_mags, imp_phases)
        elif filter['type'] == 'none':
            filter_mag, filter_phase = np.zeros_like(mags), np.zeros_like(phases)
        else:
            raise ValueError(f"Unknown filter type: {filter['type']}")
        
        combined_mags = mags + filter_mag
        combined_phases = phases + filter_phase
        filtered_responses.append((mags, phases, combined_mags, combined_phases))
        
        mags_linear = 10 ** (combined_mags / 20)
        phases_rad = np.radians(combined_phases)
        driver_response = mags_linear * np.exp(1j * phases_rad)
        total_response += driver_response
    
    final_mags = 20 * np.log10(np.abs(total_response))
    final_phases = np.angle(total_response, deg=True)
    
    return ref_freqs, final_mags, final_phases, filtered_responses