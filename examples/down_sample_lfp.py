import sys
sys.path.append(r'Q:/sachuriga/Sachuriga_Python/quality_metrix')

import spikeinterface as si
import spikeinterface.extractors as se
import spikeinterface.postprocessing as post
from spikeinterface.preprocessing import (bandpass_filter,
                                           common_reference,resample)
import spikeinterface.exporters as sex
import spikeinterface.qualitymetrics as sqm
from pathlib import Path
from preprocess.down_sample import down_sample
import numpy as np
def main():
    raw_path = r'S:\Sachuriga/Ephys_Recording/CR_CA1/65409/65409_2023-12-04_15-42-35_A'
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

    recp = bandpass_filter(recording, freq_min=1, freq_max=475)
    lfp = resample(recp, resample_rate=1000, margin_ms=100.0)
    lfp_car =  common_reference(lfp,reference='global', operator='average')
    lfp_times = down_sample(recording.get_times(),lfp.get_num_samples())

    lfp_car.get_traces().shape



if __name__== "__main__":
    main()