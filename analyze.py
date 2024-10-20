import re
import sys

def parse_memory_log(file_path, page_size):
    region_access_count = {}

    try:
        with open(file_path, 'r', errors='ignore') as log_file:
            for entry in log_file:
                mem_address, tlb_miss_count = parse_log_entry(entry)
                if mem_address is not None and tlb_miss_count is not None:
                    page_start = (mem_address // page_size) * page_size
                    if page_start in region_access_count:
                        region_access_count[page_start] += tlb_miss_count
                    else:
                        region_access_count[page_start] = tlb_miss_count
    except OSError as error:
        raise RuntimeError(f"Could not open or process file: {file_path}") from error

    return region_access_count

def parse_log_entry(entry):
    address_match = re.search(r'([0-9a-fA-Fx]+)\s+anon\s+None', entry)
    miss_count_match = re.search(r'\s+(\d+)\s+', entry)

    if address_match and miss_count_match:
        try:
            address_value = int(address_match.group(1), 16)
            miss_count_value = int(miss_count_match.group(1))
            return address_value, miss_count_value
        except (ValueError, TypeError):
            return None, None
    return None, None

def save_top_pages_to_file(access_data, output_file, max_pages):
    sorted_access_data = sorted(access_data.items(), key=lambda item: item[1], reverse=True)[:max_pages]

    try:
        with open(output_file, 'w') as output:
            for page_start, _ in sorted_access_data:
                output.write(f"{page_start}\n")
    except OSError as error:
        raise RuntimeError(f"Error writing to file: {output_file}") from error

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analyze.py <max_pages>")
        sys.exit(1)

    try:
        max_pages = int(sys.argv[1])
    except ValueError:
        print("Error: Argument must be an integer.")
        sys.exit(1)

    log_file_path = "memory_accesses.txt"
    output_file_path = "largepages.txt"
    page_size = 2 * 1024 * 1024

    access_data = parse_memory_log(log_file_path, page_size)
    save_top_pages_to_file(access_data, output_file_path, max_pages)
