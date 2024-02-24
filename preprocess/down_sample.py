import math
import numpy as np

def main():
    msg_cache = recording.get_times()  # Assuming this is your data source
    msg_n = lfp.get_num_samples()  # Total number of samples you want
    down_sample(msg_cache,msg_n)

def down_sample(msg_cache,msg_n):
    import math

    inc = len(msg_cache) / msg_n  # Calculate increment ratio
    inc_total = 0
    times = np.empty(msg_n)  # Initialize times dictionary
    n = 0
    
    for i in range(msg_n):
        index = math.floor(inc_total)
        if index < len(msg_cache):  # Check to avoid IndexError
            msg_downsampled = msg_cache[index]
            times[i] = msg_downsampled  # Assign to times array
            inc_total += inc
        else:
            break  # Exit loop if index exceeds msg_cache size

    return times

if __name__== "__main__":
    main()