from datetime import datetime
import sys
from zoneinfo import ZoneInfo
sys.path.append(r'Q:/sachuriga/Sachuriga_Python/quality_metrix')

from pathlib import Path
from neuroconv.datainterfaces import PhySortingInterface
from neuroconv.datainterfaces import OpenEphysRecordingInterface
from neuroconv import ConverterPipe
from postprocess.Get_positions import load_positions,calc_head_direction,moving_direction
from pynwb import NWBHDF5IO
from pynwb import NWBHDF5IO
from preprocess.down_sample_lfp import down_sample_lfp,add_lfp2nwb
from dateutil import tz
from dateutil.tz import tzlocal
from pynwb.behavior import (
    Position,
    SpatialSeries,
    CompassDirection
)
import numpy as np
from pynwb import NWBFile
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

    down_sample_lfp(fr"{path}",fr"{ECEPHY_DATA_PATH}")
    folder_path = Path(folder_path)

    # Change the folder_path to the appropriate location in your system
    try:
        interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)
    except AssertionError:
        try:
            stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
            interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)
        except AssertionError:
            folder_path = fr"{ECEPHY_DATA_PATH}/Record Node 101"
            stream_name = 'Record Node 101#Acquisition_Board-100.Rhythm Data'
            interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)

    # Extract what metadata we can from the source files
    folder1_path = f"{path}"  # Change the folder_path to the location of the data in your system
    print(fr"Animal number is {UD[0]}")
    # if UD[0] == "65409":
    print(fr"Animal number is {UD[0]} replacing the spike times")
    sample_num = np.load(fr"{folder1_path}/spike_times.npy")
    try:
        timestemp = np.load(fr'{folder_path}/continuous/OE_FPGA_Acquisition_Board-101.Rhythm Data/sample_numbers.npy')
    except FileNotFoundError:
        folder_path = fr"{ECEPHY_DATA_PATH}/Record Node 101"
        # S:\Sachuriga\Ephys_Recording\CR_CA1\65588\65588_2024-03-06_15-45-53_A\Record Node 101\experiment1\recording1\continuous\Acquisition_Board-100.Rhythm Data
        timestemp = np.load(fr'{folder_path}/experiment1/recording1/continuous/Acquisition_Board-100.Rhythm Data/sample_numbers.npy')
    print(folder_path)
    
    time_spk = timestemp[sample_num]
    np.save(fr"{folder1_path}/spike_times.npy",time_spk)
    interface_phy = PhySortingInterface(folder_path=folder1_path, verbose=True)
    # else:
    #     interface_phy = PhySortingInterface(folder_path=folder1_path, verbose=True)
    # # For data provenance we add the time zone information to the conversionSS

    converter = ConverterPipe(data_interfaces=[interface_ophys, interface_phy], verbose=False)

    # Extract what metadata we can from the source files
    arr_with_new_col = load_positions(path,vedio_search_directory,folder_path,UD)
    # print(f"{arr_with_new_col.shape[1]} output the shape of the array")

    snout2neck = arr_with_new_col[:,[0,1,2,3,4]]
    neck2back4 = arr_with_new_col[:,[0,3,4,5,6]]
    # print(f"snout2neck: {snout2neck}")  
    # print(f"neck2back4: {neck2back4}")

    hd=calc_head_direction(snout2neck)
    bd=calc_head_direction(neck2back4)
    md,new_pos = moving_direction(arr_with_new_col)
    # print(f"position: {new_pos}")
    # print(f"moving Directions: {md.shape}")
    # print(f"Head Directions: {hd}")
    # print(f"Body Directions: {bd}")

    position_spatial_series = SpatialSeries(
        name="SpatialSeries",
        description="Position (x, y) in an open field.",
        data=arr_with_new_col[:,[1,2]],
        timestamps=arr_with_new_col[:,0],
        reference_frame="(0,0) is top left corner")
    
    hd_direction_spatial_series = SpatialSeries(name="SpatialSeries",
                                             description="View angle of the subject measured in radians.",
                                             data=hd,
                                             timestamps=arr_with_new_col[:,0],
                                             reference_frame="straight ahead",
                                             unit="radians",)
    
    bd_direction_spatial_series = SpatialSeries(name="SpatialSeries",
                                             description="View angle of the subject measured in radians.",
                                             data=bd,
                                             timestamps=arr_with_new_col[:,0],
                                             reference_frame="straight back",
                                             unit="radians",)

    md_direction_spatial_series = SpatialSeries(name="SpatialSeries",
                                             description="moving angle of the subject measured in radians.",
                                             data=md,
                                             timestamps=arr_with_new_col[:,0],
                                             reference_frame="moving direction",
                                             unit="radians",)   

    nwbfile = NWBFile(
        session_description="Mouse exploring an open field",  # required
        identifier="sachuriga",  # required
        session_start_time=datetime.now(tzlocal())) # required)
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
        species=species)
    metadata["general_session_id "] = UD[3]
    metadata["lab"] = "quattrocolo lab"
    metadata["institution"] = 'kavili institute for system neuroscience'
    metadata["session_description"] = f"{UD[3]}_room open-field CA1 recording"
    print(metadata)
    # For data provenance we add the time zone information to the conversionS
    converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)
    print("completet!!!!adding conversion to nwb file")
    channel2selec = [3, 8, 24, 16, 10, 1, 31, 15, 31, 58, 53, 50, 52, 4, 63, 48, 45, 55]

    with NWBHDF5IO(nwbfile_path, "r+") as io:
        read_nwbfile = io.read()
        behavior_module = read_nwbfile.create_processing_module(name="Behavioral data", 
                                                          description="position, head direction, and body direction of the mouse in an open field.")
        position = Position(spatial_series=position_spatial_series, name='Position in pixel')
        behavior_module.add(position)
        hd_direction = CompassDirection(spatial_series=hd_direction_spatial_series, name="Head(snout2neck)_Direction")
        bd_direction = CompassDirection(spatial_series=bd_direction_spatial_series, name="Body(neck2back4)_Direction")
        md_direction = CompassDirection(spatial_series=md_direction_spatial_series, name="Moving_Direction")

        behavior_module.add(hd_direction)
        behavior_module.add(bd_direction)
        behavior_module.add(md_direction)
        print(behavior_module)
        io.write(read_nwbfile)
    add_lfp2nwb(nwbfile_path,channel2selec,folder1_path)
    print("With no positions")
    print("completet!!!!adding lfp to nwb file")
if __name__== "__main__":
    main()