import pandas as pd
import numpy as np

dlc_path=r"S:/Sachuriga/Ephys_Vedio/CR_CA1/65590_Open_Field_50Hz_B2024-02-252024-02-25T14_41_31DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000_sk_filtered.csv"

df = pd.read_csv(dlc_path)
#print(df)
pos = df[['DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000',
        'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.1',
        'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.12',
        'DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000.13']]
positions = np.float32(pos[3:].to_numpy())

print(positions)
print(df['DLC_dlcrnetms5_CR_implant_DLCnetNov30shuffle3_600000'].shape)