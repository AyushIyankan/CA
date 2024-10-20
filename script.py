import re
import sys
from collections import defaultdict

def parse_memory_accesses(filename):
    top_mem_regions = defaultdict(int)
    region_size = 2 * 1024 * 1024  # 2MB region size
    
    try:
        with open(filename, mode='r', errors='ignore') as f:
            for line in f:
                match = re.search(r'([0-9a-fA-Fx]+)\s+anon\s+None', line)
                if match:
                    address_str = match.group(1)
                    try:
                        address = int(address_str, 16)
                        weight_match = re.search(r'\s+(\d+)\s+', line)
                        if weight_match:
                            weight = int(weight_match.group(1))
                            region = (address // region_size) * region_size
                            top_mem_regions[region] += weight
                    except ValueError:
                        print("Please make sure you have correct formatting of files.")
                        continue
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file '{filename}' does not exist.")

    return top_mem_regions

def write_top_n_regions(top_mem_regions, output_file, n):
    sorted_regions = sorted(top_mem_regions.items(), key=lambda x: x[1], reverse=True)[:n]

    with open(output_file, 'w') as f:
        for (region, tlb_misses) in sorted_regions:
            f.write(f"{region}, {tlb_misses}\n")
    print(f"Top {n} TLB miss regions saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze.py <n>")
        sys.exit(1)

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("Invalid argument: Please enter an integer.")
        sys.exit(1)
    
    memory_access_file = "memory_accesses.txt" 
    largepage_output_file = "largepages.txt" 

    top_mem_regions = parse_memory_accesses(memory_access_file)
    write_top_n_regions(top_mem_regions, largepage_output_file, n)
