import sys
sys.path.append('Q:\sachuriga\Sachuriga_Python\quality_metrix')

from preprocess.copy_file import copy_file
from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix       

file = "C:\Ephys_temp/65410_2023-11-25_13-57-58_A_phy_k"
print(file)
qualitymetrix(file)