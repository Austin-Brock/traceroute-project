import re
import random

# Function to parse the network trace dump
def parse_network_trace(dump_lines):
    data = {}
    for line in dump_lines:
        if 'IP' in line:
            parts = line.split()
            ttl = int(re.search(r'ttl (\d+)', line).group(1))
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)\.\d+ > (\d+\.\d+\.\d+\.\d+)\.\d+', line)
            if ip_match:
                src_ip, dst_ip = ip_match.groups()
                if ttl not in data:
                    data[ttl] = {
                        'ips': [],
                        'times': []
                    }
                data[ttl]['ips'].append(dst_ip)
                # Simulate response times for demonstration purposes
                response_times = [f"{round(random.uniform(0.3, 1.5), 3)} ms" for _ in range(3)]
                data[ttl]['times'].append(response_times)

    return data

# Function to print the formatted output
def print_formatted_output(data):
    for ttl, details in data.items():
        print(f"TTL {ttl}")
        for ip, times in zip(details['ips'], details['times']):
            print(ip)
            for time in times:
                print(time)

# Function to read from a file
def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

# Main execution block
if __name__ == "__main__":
    # Replace 'sampletcpdump.txt' with your actual file path if needed
    dump_lines = read_from_file('sampletcpdump.txt')
    parsed_data = parse_network_trace(dump_lines)
    print_formatted_output(parsed_data)
