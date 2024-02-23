from datetime import datetime
from uuid import uuid4
import glob
import os
import pandas as pd
import numpy as np
from dateutil.tz import tzlocal
from pathlib import Path
import h5py  
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from pynwb.behavior import (
    BehavioralEpochs,
    BehavioralEvents,
    BehavioralTimeSeries,
    CompassDirection,
    EyeTracking,
    Position,
    PupilTracking,
    SpatialSeries,
)
from pynwb.epoch import TimeIntervals
from pynwb.misc import IntervalSeries

#vedio_search_directory = 'S:/Sachuriga/Ephys_Vedio/CR_CA1/'
#folder_path = fr"S:/Sachuriga/Ephys_Recording/CR_CA1/65410/65410_2023-12-04_13-38-02_A/Record Node 102/"

def load_positions(path,vedio_search_directory,folder_path,UD):

    search_pattern = os.path.join(vedio_search_directory, f"*{UD[0]}*{UD[3]}{UD[1]}*600000_sk_filtered.csv")
    print(search_pattern)
    search_pattern1 = os.path.join(folder_path, '**/**/TTL/timestamps.npy')
    search_pattern3 = os.path.join(folder_path, '**/**/TTL/states.npy')
    #search_pattern2 = os.path.join(folder_path, '**/**/continuous/*/timestamps.npy')

    # Use glob to find files matching the pattern

    matching_files = glob.glob(search_pattern,recursive=True)
    matching_files = np.unique(matching_files)

    dlc_path=Path(matching_files[0])

    df = pd.read_csv(dlc_path)
    pos = df[['DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000',
            'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.1',
            'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.12',
            'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.13']]
    positions = np.float32(pos[3:].to_numpy())


    matching_files = glob.glob(search_pattern1,recursive=True)
    matching_files = np.unique(matching_files)
    v_time = np.load(matching_files[0])

    matching_files = glob.glob(search_pattern3,recursive=True)
    matching_files = np.unique(matching_files)
    v_state = np.load(matching_files[0])
    f_time = v_time[np.where(v_state==3)[0]]


    arr_with_new_col =  np.insert(positions , 0, f_time[:len(positions)], axis=1)



    return arr_with_new_col
