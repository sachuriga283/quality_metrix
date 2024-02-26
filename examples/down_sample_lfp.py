import sys
from tabnanny import verbose
sys.path.append(r'Q:/sachuriga/Sachuriga_Python/quality_metrix')

import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.postprocessing as post
from spikeinterface.preprocessing import (bandpass_filter,
                                           common_reference,resample)
import spikeinterface.exporters as sex
import spikeinterface.qualitymetrics as sqm
from pathlib import Path
from preprocess.down_sample import down_sample # type: ignore
import numpy as np

def main():
    print(main)

def down_sample_lfp(file_path,raw_path):
    #raw_path = r'S:\Sachuriga/Ephys_Recording/CR_CA1/65409/65409_2023-12-04_15-42-35_A'
    stream_name = 'Record Node 101#OE_FPGA_Acquisition_Board-100.Rhythm Data'
    try:
        recordingo = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)
    except AssertionError:
        try:
            stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
            recordingo = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)
        except AssertionError:
            stream_name = 'Record Node 101#Acquisition_Board-100.Rhythm Data'
            recordingo = se.read_openephys(raw_path, stream_name=stream_name, load_sync_timestamps=True)

    #file_path = r'S:/Sachuriga/Ephys_Recording/CR_CA1/65409/65409_2023-12-04_15-42-35_A_phy_k_manual/recording.dat'
    sampling_frequency=30000
    num_channels = 64  # Adjust according to your MATLAB dataset
    dtype_int = 'int16'  # Adjust according to your MATLAB dataset
    gain_to_uV = 0.195  # Adjust according to your MATLAB dataset
    offset_to_uV = 0 
    recording = si.read_binary(file_paths=file_path, sampling_frequency=sampling_frequency,
                            num_channels=num_channels, dtype=dtype_int,
                            gain_to_uV=gain_to_uV, offset_to_uV=offset_to_uV)

    recp = bandpass_filter(recording, freq_min=1, freq_max=475)
    rec_lfp_car = common_reference(recp, reference='global', 
                               operator='average', 
                               dtype='int16')
    lfp_car = resample(rec_lfp_car, resample_rate=1000, margin_ms=100.0)
    lfp = resample(recp, resample_rate=1000, margin_ms=100.0)
    lfp_times = down_sample(recordingo.get_times(), lfp.get_num_samples())
    channel_ids=['CH4', 'CH9', 'CH25',
                  'CH17', 'CH11', 'CH2',
                  'CH32', 'CH16', 'CH14',
                  'CH59', 'CH54', 'CH51',
                  'CH53', 'CH58', 'CH64',
                  'CH47', 'CH36', 'CH56']
    lfp_car_slice=lfp_car.channel_slice(channel_ids=channel_ids)
    lfp_slice=lfp.channel_slice(channel_ids=channel_ids)

    print("get_traces() shape:")
    np_lfp_car=lfp_car_slice.get_traces()
    np_lfp = lfp_slice.get_traces()
    path_iron = Path(file_path)
    np.save(path_iron / 'lfp_times.npy', lfp_times) # type: ignore
    np.save(path_iron / 'lfp_car.npy',  np_lfp_car)
    np.save(path_iron / 'lfp.npy', np_lfp)  # Save the LFP data

    print(f"shape {np_lfp.shape}")
    print(f"descriptions{lfp.get_binary_description()}")
    print(np_lfp)

if __name__== "__main__":
    main()