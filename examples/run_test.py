import sys
sys.path.append('Q:\sachuriga\Sachuriga_Python\quality_metrix')

from preprocess.copy_file import copy_file
from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix
from postprocess.nwbPHYnOPHYS import nwbPHYnOPHYS

sex = "F"
ID = "65410"
age = "P45+"
species = "Mus musculus"
vedio_search_directory = 'S:/Sachuriga/Ephys_Vedio/CR_CA1/'

def main():
    #getting sorted files
    folder_path = fr'S:/Sachuriga/Ephys_Recording/CR_CA1/{ID}/'
    sorted_files = load_data(folder_path, file_suffix='_phy_k')

    #for file in sorted_files:
    #quality_metrix and export to new phy folder

    for file in sorted_files[-2:]:
        print(file)
        qualitymetrix(file)

        #nwbPHYnOPHYS(file,
        #             sex,
        #             age,
        #             species,
        #             vedio_search_directory)
       
        #copy_file(file, file +"_cured")

    print("completet!!!!")

if __name__== "__main__":
    main()