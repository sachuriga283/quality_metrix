from datetime import datetime
from dateutil import tz
from pathlib import Path
from neuroconv.datainterfaces import PhySortingInterface
from neuroconv.datainterfaces import OpenEphysRecordingInterface
from neuroconv import ConverterPipe

def nwbPHYnOPHYS(path):

    temp = path[-35:]
    path1 = temp.split("\\")

    file = path.split("_phy_")
    ECEPHY_DATA_PATH = file[0]
    path_to_save_nwbfile = "S:/Sachuriga/nwb"
    stream_name = 'Record Node 102#OE_FPGA_Acquisition_Board-101.Rhythm Data'
    folder_path = f"{ECEPHY_DATA_PATH}"
    print(folder_path)
    # Change the folder_path to the appropriate location in your system
    interface_ophys = OpenEphysRecordingInterface(folder_path=folder_path,stream_name=stream_name)

    # Extract what metadata we can from the source files
    folder1_path = f"{path}"  # Change the folder_path to the location of the data in your system
    interface_phy = PhySortingInterface(folder_path=folder1_path, verbose=False)

    converter = ConverterPipe(data_interfaces=[interface_ophys, interface_phy], verbose=False)

    # Extract what metadata we can from the source files
    metadata = converter.get_metadata()
    # For data provenance we add the time zone information to the conversion
    session_start_time = metadata["NWBFile"]["session_start_time"].replace(tzinfo=tz.gettz("US/Pacific"))
    metadata["NWBFile"].update(session_start_time=session_start_time)

    # Choose a path for saving the nwb file and run the conversion
    nwbfile_path = f"{path_to_save_nwbfile}/path1/{path1[1]}.nwb"
    converter.run_conversion(nwbfile_path=nwbfile_path, metadata=metadata)