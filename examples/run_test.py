import sys
sys.path.append('Q:\sachuriga\Sachuriga_Python\quality_metrix')

from preprocess.load_data import load_data
from postprocess.quality_metrix import qualitymetrix

#getting sorted files
sorted_files = load_data(r'S:\Sachuriga\Ephys_Recording\CR_CA1\65410', file_suffix='_phy_k')

#for file in sorted_files:
#quality_metrix and export to new phy folder

for file in sorted_files:
    qualitymetrix(file)
