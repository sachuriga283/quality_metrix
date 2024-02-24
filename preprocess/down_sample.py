import math

def main():
    down_sample(msg_cache,msg_n)

def down_sample(msg_cache,msg_n):
    import math

    msg_cache = recording.get_times()  # Assuming this is your data source
    msg_n = lfp.get_num_samples()  # Total number of samples you want
    inc = len(msg_cache) / msg_n  # Calculate increment ratio
    inc_total = 0
    times = []  # Initialize times dictionary
    n = 0

    for _ in range(msg_n):
        index = math.floor(inc_total)
        if index < len(msg_cache):  # Check to avoid IndexError
            msg_downsampled = msg_cache[index]
            times.append(msg_downsampled)  # Store in times
            inc_total += inc
            n += 1
        else:
            break  # Exit loop if index exceeds msg_cache size
    
    return times
if __name__== "__main__":
    main()