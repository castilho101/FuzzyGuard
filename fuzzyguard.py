import sys
import math
import requests
import argparse
import concurrent.futures

from collections import Counter

# Global Variables
SILENT_MODE = 1
FFUF_EXTRA_FLAG = ""
RANDOM_ENDPOINT = "THIS_ENDPOINT_DOES_NOT_EXIST"

# Class for Colors (obviously)
class Color:
    def red(message): return f"\033[91m{message}\033[0m"
    def bold(message): return f"\033[1m{message}\033[0m"
    def green(message): return f"\033[92m{message}\033[0m"
    def yellow(message): return f"\033[93m{message}\033[0m"

# Function for ASCII Art
def logo():
    
    print(Color.bold("""
             ,         _____                 
        _.-"` `'-.    |   __|_ _ ___ ___ _ _
        '._ __{}_(    |   __| | |- _|- _| | |
        |'--.__\\      |__|  |___|___|___|_  |
        (   =_\ =      _____            |___|
         |   _ |      |   __|_ _ ___ ___ _| |
         )\___/       |  |  | | | .'|  _| . |
     .--'`:._]        |_____|___|__,|_| |___|
    /  \      '-.              Made By: @castilho101
"""))

# Generate the ffuf command string for the target 
def generate_ffuf_commands(target, ffuf_filter_flags):
    
    prefix = ""
    ffuf_command = f"ffuf -u {target}/FUZZ -w WORDLIST {ffuf_filter_flags[1:]} {FFUF_EXTRA_FLAG}"
    
    if not SILENT_MODE:
        prefix = f"{Color.bold('[')}{Color.green('+')}{Color.bold(']')} "
    
    print(prefix + ffuf_command)

# Calculate the range of values
def get_ranges_from_value(value):
    
    # Determine the divisor based on the number of digits in the value
    divisor = 10 ** (len(str(value)) - 2)

    # Calculate the minimum and maximum range values
    min_range = math.floor(value / divisor) * divisor
    max_range = min_range + divisor

    return f"{min_range}-{max_range}"


# Validate the results of the target analysis
def validate_results(target, target_num_lines, target_num_words, target_size_bytes):
    
    # Variables
    ffuf_filter_flags = ""

    # Create a list of tuples with the flag identifier and the Counter object
    counters = [
        ('-fl', Counter(target_num_lines)),
        ('-fw', Counter(target_num_words)),
        ('-fs', Counter(target_size_bytes)),
    ]

    # Iterate over the counters
    for flag, counter in counters:
        
        # Get the most common values
        most_common = counter.most_common()

        # If there is only one most common value, add the corresponding filter flag and value
        if len(most_common) == 1:
            flag_value = most_common[0][0]
            ffuf_filter_flags += f" {flag} {flag_value}"
        else:
            # Create a list of values from the most_common tuples
            values_list = []
            for tuple_value in most_common:
                values_list.append(tuple_value[0])

            # Get the range for the filter flag
            ranges = get_ranges_from_value(min(values_list))
            ffuf_filter_flags += f" {flag} {ranges}"

    # Generate ffuf command for target
    generate_ffuf_commands(target, ffuf_filter_flags)

# Main Function
def analyze_targets(target):
    
    # variables
    target_num_lines = set()
    target_num_words = set()
    target_size_bytes = set()
    
    # Request 15 times to get values to analyze
    for i in range(15):
        
        # Make GET request
        target_endpoint = target + f"/{RANDOM_ENDPOINT}"
        response = requests.get(target_endpoint)
        
        # Check response
        if response.status_code != 200:
            generate_ffuf_commands(target, "")
            break
        
        content = response.text
        
        # Get values for analyzies
        num_words  = len(content.split(" "))
        num_lines  = len(content.split('\n'))
        size_bytes = len(content.encode('utf-8'))
        
        target_num_lines.add(num_lines)
        target_num_words.add(num_words)
        target_size_bytes.add(size_bytes)

    # Validate Results
    if len(target_num_lines):
        validate_results(target, target_num_lines, target_num_words, target_size_bytes)    

# Main function
def main():
    
    global FFUF_EXTRA_FLAG, SILENT_MODE
    
     # Script Arguments
    parser = argparse.ArgumentParser(description='FuzzyGuard for Automatic FFUF Fuzzing!')
    parser.add_argument('--ffuf-flags', dest='ffuf_flags', type=str, help='Extra FFUF flags, ex: --ffuf-extra "-mc all -fc 404"')
    parser.add_argument('--silent', dest='silent', action="store_true", help='Silent mode')

    # Parse and check Arguments
    args = parser.parse_args()
    
    if not args.silent: 
        logo()
        SILENT_MODE = 0
           
    if args.ffuf_flags: FFUF_EXTRA_FLAG = args.ffuf_flags

    # See if we have data to analyze
    if not sys.stdin.isatty():
        
        # List for each of the targets
        user_input = sys.stdin.read().split("\n")
        targets = list(filter(None, user_input))

        # Create a thread for each URL
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(analyze_targets, targets)

    else:
        # Exit if there's no STDIN
        print(f"{Color.bold('[')}{Color.red('!')}{Color.bold('] Please send me some targets!')}")
        exit()

# yeah
if __name__ == '__main__':
    main()
