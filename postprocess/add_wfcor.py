import pandas as pd
import numpy as np
from pathlib import Path
def main():
    path = r"S:/Sachuriga/Ephys_Recording/CR_CA1/65409/65409_2023-12-08_16-39-36_A_phy_k_manual"
    add_wf_cor(path)

def add_wf_cor(path):

    path_cluster_group = Path(fr"{path}/cluster_group.tsv")
    path_cluster_metrix = Path(fr"{path}/waveforms/template_metrics/metrics.csv")
    path_ulocation = Path(fr"{path}/waveforms/unit_locations/unit_locations.npy")
    df0 = pd.read_csv(path_cluster_group, index_col=0, sep='\t')
    df1 = pd.read_csv(path_cluster_metrix)
    df2 = pd.DataFrame(np.load(path_ulocation),columns=['x', 'y','z'])
    df3 = pd.merge(df0, df1,left_index=True,right_index=True)
    df4 = pd.merge(df3, df2,left_index=True,right_index=True)


    print(df4)
    df4.to_csv(Path(fr"{path}/cluster_group.tsv"), 
               sep="\t", header=True, 
               index=True)
if __name__== "__main__":
    main()