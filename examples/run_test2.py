import os
from pathlib import Path
import sys
base_path = Path("Q:/Sachuriga/Sachuriga_Python")
base_data_folder = Path("S:/Sachuriga/")
project_path = fr"{base_path}/quality_metrix/"

# change to project root
sys.path.append(project_path)

from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix
from postprocess.nwbPHYnOPHYS import nwbPHYnOPHYS
from postprocess.add_wfcor import add_wf_cor
# set params for nwb
sex = "F"
ID = "65409"
age = "P45+"
species = "Mus musculus"
vedio_search_directory = base_data_folder/fr"Ephys_Vedio/CR_CA1/"
path_save = base_data_folder/fr"nwb"

def main():
    

    #getting sorted files
    folder_path = fr"{str(base_data_folder)}/Ephys_Recording/CR_CA1/{ID}/"


    ##for quality metrix
    sorted_files = load_data(folder_path, file_suffix='_phy_k')

    ##for nwb
    #sorted_files = load_data(folder_path, file_suffix='_phy_k_manual')
    #quality_metrix and export to new phy folder

    for file in sorted_files[-1:]:
        print(file)

        qualitymetrix(file)
        #add_wf_cor(file)
        #nwbPHYnOPHYS(file,
        #             sex,
        #             age,
        #             species,
        #             vedio_search_directory,
        #             path_to_save_nwbfile = path_save)
    
    print("completet!!!!")

if __name__== "__main__":
    main()