import sys
sys.path.append('Q:\sachuriga\Sachuriga_Python\quality_metrix')

from preprocess.copy_file import copy_file
from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix
from postprocess.nwbPHYnOPHYS import nwbPHYnOPHYS
def main():
    #getting sorted files
    folder_path = r'S:/Sachuriga/Ephys_Recording/CR_CA1/65410'
    sorted_files = load_data(folder_path, file_suffix='_phy_k')


    #for file in sorted_files:
    #quality_metrix and export to new phy folder

    for file in sorted_files:
        print(file)
        nwbPHYnOPHYS(file)
    #    print(file)
        
    #    qualitymetrix(file)
    #    #copy_file(file, file +"_cured")

    #print("completet!!!!")

if __name__== "__main__":
    main()