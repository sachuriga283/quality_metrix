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
import probeinterface as pi

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
    probe.to_dataframe(complete=True).loc[:, ["contact_ids", "shank_ids", "device_channel_indices"]]
    probegroup = pi.ProbeGroup()
    probegroup.add_probe(probe)

    pi.write_prb(f"{probe_name}.prb", probegroup, group_mode="by_shank")
    recording_prb = recordingo.set_probe(probe, group_mode="by_shank")
    recp = bandpass_filter(recording_prb, freq_min=1, freq_max=475)
    rec_lfp_car = common_reference(recp, reference='global', 
                               operator='average', 
                               dtype='int16')
    lfp_car = resample(rec_lfp_car, resample_rate=1000, margin_ms=100.0)
    lfp = resample(recp, resample_rate=1000, margin_ms=100.0)
    print(lfp_car.get_channel_ids())
    lfp_times = down_sample(recordingo.get_times(), lfp.get_num_samples())
    lfp_car_slice=lfp_car.channel_slice(channel_ids=['CH4', 'CH9', 'CH25',
                                                     'CH17', 'CH11', 'CH2',
                                                     'CH32', 'CH16', 'CH14',
                                                     'CH59', 'CH54', 'CH51',
                                                     'CH53', 'CH58', 'CH64',
                                                     'CH47', 'CH36', 'CH56'])
    
    lfp_slice=lfp.channel_slice(channel_ids=['CH4', 'CH9', 'CH25',
                                             'CH17', 'CH11', 'CH2',
                                             'CH32', 'CH16', 'CH14',
                                             'CH59', 'CH54', 'CH51',
                                             'CH53', 'CH58', 'CH64',
                                             'CH47', 'CH36', 'CH56'])

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