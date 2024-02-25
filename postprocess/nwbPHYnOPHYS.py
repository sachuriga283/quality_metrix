from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil import tz
from pathlib import Path
from neuroconv.datainterfaces import PhySortingInterface
from neuroconv.datainterfaces import OpenEphysRecordingInterface
from neuroconv import ConverterPipe
from postprocess.Get_positions import load_positions
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
import numpy as np
from pynwb.ecephys import LFP, ElectricalSeries
from pynwb import ProcessingModule

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

def main():
    path = "S:\\Sachuriga/Ephys_Recording/CR_CA1/65409/65409_2023-12-08_16-39-36_A_phy_k_manual"
    sex = "F"
    ages = "P60"
    species = "Mus musculus"
    vedio_search_directory = "S:/Sachuriga/Ephys_Vedio/CR_CA1"
    path_to_save_nwbfile = "S:/Sachuriga/nwb"
    nwbPHYnOPHYS(path, sex, ages, species, vedio_search_directory, path_to_save_nwbfile)  # Added missing argument


def nwbPHYnOPHYS(path,sex,ages,species,vedio_search_directory,path_to_save_nwbfile):

    if path.endswith("phy_k_manual"):
        num2cal = int(41)
    elif path.endswith("phy_k"):
        num2cal = int(35)

    temp = path[0 - num2cal:]
    path1 = temp.split("/")

    file = path.split("_phy_")
    UD = path1[1].split("_")
    print(file[1])

    ECEPHY_DATA_PATH = file[0]
    stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
    folder_path = fr"{ECEPHY_DATA_PATH}/Record Node 102"
    
    folder_path = Path(folder_path)

    # Change the folder_path to the appropriate location in your system
    interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)

    # Extract what metadata we can from the source files
    folder1_path = f"{path}"  # Change the folder_path to the location of the data in your system

    sample_num = np.load(fr"{folder1_path}/spike_times.npy")
    timestemp = np.load(fr'{folder_path}\experiment1\recording1\continuous\OE_FPGA_Acquisition_Board-101.Rhythm Data/sample_numbers.npy')
    print(folder_path)
    time_spk = timestemp[sample_num]
    np.save(fr"{folder1_path}/spike_times.npy",time_spk)
    interface_phy = PhySortingInterface(folder_path=folder1_path, verbose=False)
    # For data provenance we add the time zone information to the conversionSS

    converter = ConverterPipe(data_interfaces=[interface_ophys, interface_phy,], verbose=False)
    # Extract what metadata we can from the source files
    
    arr_with_new_col = load_positions(path,vedio_search_directory,folder_path,UD)
    print(arr_with_new_col.shape)
    print(arr_with_new_col[:,[1,2]])

    position_spatial_series = SpatialSeries(
        name="SpatialSeries",
        description="Position (x, y) in an open field.",
        data=arr_with_new_col[:,[1,2]],
        timestamps=arr_with_new_col[:,0],
        reference_frame="(0,0) is top left corner",
    )
    nwbfile = NWBFile(
        session_description="Mouse exploring an open field",  # required
        identifier="sachuriga",  # required
        session_start_time=datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("America/Los_Angeles")))  # required)
    
    device = nwbfile.create_device(name="multi-shanks", 
                                   description="cambridgeneurotech_mini-amp-64-ASSY-236-F", 
                                   manufacturer="cambridgeneurotech") 
    
    nwbfile.add_electrode_column(name="label", description="label of electrode")

    nshanks = 6
    electrode_counter = 0

    for ishank in range(nshanks):
    # create an electrode group for this shank
        electrode_group = nwbfile.create_electrode_group(
        name="shank{}".format(ishank),
        description="electrode group for shank {}".format(ishank),
        device=device,
        location="hipocampus")
        if ishank==1 or ishank==6:
            nchannels_per_shank = 11
        else:
            nchannels_per_shank = 12
        # add electrodes to the electrode table
        for ielec in range(nchannels_per_shank):
            nwbfile.add_electrode(
                group=electrode_group,
                label="shank{}elec{}".format(ishank, ielec),
                location="hipocampus")
            electrode_counter += 1

    all_table_region = nwbfile.create_electrode_table_region(region=list(range(electrode_counter)),  # reference row indices 0 to N-1
                                                             description="all electrodes")
    lfp_time = np.load(fr"{folder1_path}/lfp_times.npy")
    carlafp_data = np.load(fr"{folder1_path}/lfp_car.npy")
    lfp_car_electrical_series = ElectricalSeries(
        name="car_lfp",
        data=carlafp_data,
        electrodes=all_table_region,
        starting_time=lfp_time [0],  # timestamp of the first sample in seconds relative to the session start time
        rate = 1000.0),  # in Hz)
    car_lfp = LFP(electrical_series=lfp_car_electrical_series)
    ecephys_module = nwbfile.create_processing_module(name="ecephys", 
                                                      description="1-475 Hz bandpass filtered LFP data with car reference")
    ecephys_module.add(car_lfp)

    lfp_raw = np.load(fr"{folder1_path}/lfp.npy")
    lfp_electrical_series = ElectricalSeries(
        name="lfp",
        data=lfp_raw,
        electrodes=all_table_region,
        starting_time=lfp_time[0],  # timestamp of the first sample in seconds relative to the session start time
        rate = 1000.0),  # in Hz)
    lfp = LFP(electrical_series=lfp_electrical_series)
    ecephys_module = nwbfile.create_processing_module(name="ecephys", 
                                                      description="1-475 Hz bandpass filtered LFP data")
    ecephys_module.add(lfp)

    position = Position(spatial_series=position_spatial_series)
    behavior_module = ProcessingModule(name="behavior", description="processed behavioral data")
    behavior_module.add(position)
    nwbfile.add_processing_module(behavior_module)

    nwbfile_path = fr"{path_to_save_nwbfile}/{path1[1]}.nwb"
    io = NWBHDF5IO(nwbfile_path, mode="w")
    io.write(nwbfile)
    io.close()

    metadata = converter.get_metadata()
    metadata["NWBFile"]["experimenter"] = ["sachuriga,sachuriga"]
    metadata["Subject"] = dict(
        subject_id=UD[0],
        sex=sex,
        age=ages,
        species=species
        )
    metadata["general_session_id "] = UD[3]
    metadata["lab"] = "quattrocolo lab"
    metadata["institution"] = 'kavili institute for system neuroscience'
    metadata["session_description"] = f"{UD[3]}_room open-field CA1 recording"
    
    print(metadata)
    # For data provenance we add the time zone information to the conversionSS
    session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=tz.gettz("US/Pacific"))

    metadata["NWBFile"].update(session_start_time=session_start_time)
    converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)

if __name__== "__main__":
    main()