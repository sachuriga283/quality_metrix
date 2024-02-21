import os
from pathlib import Path
import sys
base_path = "S:/Sachuriga/"
os.chdir(fr"{base_path}")
base_folder = Path(".")

import sys
sys.path.append(fr"{base_path}/Sachuriga_Python/quality_metrix/")

print(str(base_folder/fr"/Sachuriga_Python/quality_metrix/"))

from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix
from postprocess.nwbPHYnOPHYS import nwbPHYnOPHYS
from preprocess.get_path import current_path

sex = "F"
ID = "65409"
age = "P45+"
species = "Mus musculus"

#current_file_name_path = os.path.basename(folder)
vedio_search_directory = base_folder/fr"Ephys_Vedio/CR_CA1/"
path_save = base_folder/fr"nwb"
print(base_folder)

def main():
    #getting sorted files
    folder_path = base_folder/fr"Ephys_Recording/CR_CA1/{ID}/"
    sorted_files = load_data(folder_path, file_suffix='_phy_k')
    #quality_metrix and export to new phy folder

    for file in sorted_files:
        print(file)
        #qualitymetrix(file)
        #nwbPHYnOPHYS(file,
        #             sex,
        #             age,
        #             species,
        #             vedio_search_directory,
        #             path_to_save_nwbfile = path_save)
        
        #qualitymetrix(file)
        #copy_file(file, file +"_cured")

    print("completet!!!!")



if __name__== "__main__":
    main()