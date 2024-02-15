import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.postprocessing as post
from spikeinterface.preprocessing import (bandpass_filter, notch_filter, common_reference, highpass_filter, zscore,
                                          remove_artifacts, preprocesser_dict, normalize_by_quantile, center,
                                          correct_motion, load_motion_info)
import spikeinterface.exporters as sex
import spikeinterface.qualitymetrics as sqm

def main() -> object:
    """

    :rtype: object
    """
    print("main")
def qualitymetrix(path):

    sorting = se.read_phy(folder_path=path)
    sampling_frequency = 30_000.0  # Adjust according to your MATLAB dataset
    num_channels = 64  # Adjust according to your MATLAB dataset
    dtype_int = 'int16'  # Adjust according to your MATLAB dataset
    gain_to_uV = 0.195  # Adjust according to your MATLAB dataset
    offset_to_uV = 0  # Adjust according to your MATLAB dataset

    temp_path = path.split("_phy")
    raw_path = temp_path[0]
    stream_name = 'Record Node 101#OE_FPGA_Acquisition_Board-100.Rhythm Data'
    try:
        recording = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)
    except AssertionError:
        try:
            stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
            recording = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)
        except AssertionError:
            stream_name = 'Record Node 101#Acquisition_Board-100.Rhythm Data'
            recording = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)

    #recording = si.read_binary(file_paths=path + '/recording.bin', sampling_frequency=sampling_frequency,
    #                           num_channels=num_channels, dtype=dtype_int,
    #                           gain_to_uV=gain_to_uV, offset_to_uV=offset_to_uV)
    
    rec = bandpass_filter(recording, freq_min=300, freq_max=6000)
    rec_save = common_reference(rec, reference='global', operator='median')
    
    import probeinterface as pi

    # from probeinterface import plotting
    manufacturer = 'cambridgeneurotech'
    probe_name = 'ASSY-236-F'
    probe = pi.get_probe(manufacturer, probe_name)
    print(probe)
    # probe.wiring_to_device('cambridgeneurotech_mini-amp-64')
    # map channels to device indices
    mapping_to_device = [
        # connector J2 TOP
        41, 39, 38, 37, 35, 34, 33, 32, 29, 30, 28, 26, 25, 24, 22, 20,
        46, 45, 44, 43, 42, 40, 36, 31, 27, 23, 21, 18, 19, 17, 16, 14,
        # connector J1 BOTTOM
        55, 53, 54, 52, 51, 50, 49, 48, 47, 15, 13, 12, 11, 9, 10, 8,
        63, 62, 61, 60, 59, 58, 57, 56, 7, 6, 5, 4, 3, 2, 1, 0
    ]

    probe.set_device_channel_indices(mapping_to_device)
    probegroup = pi.ProbeGroup()
    probegroup.add_probe(probe)

    pi.write_prb(f"{probe_name}.prb", probegroup, group_mode="by_shank")
    recording_prb = rec_save.set_probe(probe, group_mode="by_shank")

    wf = si.extract_waveforms(recording_prb, sorting, folder='C:/temp_waveforms', overwrite=True, allow_unfiltered=True)

    spike_locations = post.compute_unit_locations(waveform_extractor=wf,
                                                  method='center_of_mass',
                                                  radius_um=50.)

    from spikeinterface.postprocessing import compute_principal_components
    pca = compute_principal_components(waveform_extractor=wf, n_components=5, mode="by_channel_local")
    metrics = sqm.compute_quality_metrics(waveform_extractor=wf)
    assert 'isolation_distance' in metrics.columns
    path_iron = path + "_cured"
    sex.export_to_phy(waveform_extractor=wf,
                      output_folder = path_iron,
                      remove_if_exists=True,
                      use_relative_path=True,
                      copy_binary=True)

    wf.save(path + "_cured/waveforms", format='binary')
    recp = bandpass_filter(recording_prb, freq_min=1, freq_max=475)
    reclaimer = common_reference(recp, reference='global', operator='median')
    si.write_binary_recording(reclaimer, path_iron / 'recording_lfp.bin', dtype='int16')
    si.write_binary_recording(rec_save, path_iron / 'recording_hf.bin', dtype='int16')
    si.write_binary_recording(recording, path_iron / 'recording_raw.bin', dtype='int16')


if __name__ == "__main__":
    main()
