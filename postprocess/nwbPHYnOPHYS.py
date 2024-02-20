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

def nwbPHYnOPHYS(path,sex,ages,species,vedio_search_directory):

    temp = path[-35:]
    path1 = temp.split("/")

    file = path.split("_phy_")
    UD = path1[1].split("_")
    #print(UD)

    ECEPHY_DATA_PATH = file[0]
    path_to_save_nwbfile = "S:/Sachuriga/nwb"
    stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
    folder_path = fr"{ECEPHY_DATA_PATH}/Record Node 102"
    
    folder_path = Path(folder_path)
    #print(folder_path)

    # Change the folder_path to the appropriate location in your system
    interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)

    # Extract what metadata we can from the source files
    folder1_path = f"{path}"  # Change the folder_path to the location of the data in your system
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
        session_start_time = datetime(2020, 10, 31, 12, tzinfo=ZoneInfo("America/Los_Angeles")))  # required) 
    
    position = Position(spatial_series=position_spatial_series)
    behavior_module = nwbfile.create_processing_module(name="behavior", description="processed behavioral data")
    behavior_module.add(position)

 
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
    metadata["session_description"] = f"{UD[3]}room open-field CA1 recording"
    
    print(metadata)
    # For data provenance we add the time zone information to the conversionSS
    session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=tz.gettz("US/Pacific"))

    metadata["NWBFile"].update(session_start_time=session_start_time)

    converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)