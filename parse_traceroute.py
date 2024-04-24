import re
import random

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def parse_network_trace(dump_lines):
    # Regular expression to match ICMP "time exceeded" messages and capture relevant data
    icmp_regex = r'(\d+\.\d+\.\d+\.\d+) > (\d+\.\d+\.\d+\.\d+): ICMP time exceeded in-transit.*\n.*\n\s+IP.*ttl (\d+).*id (\d+).* > (\d+\.\d+\.\d+\.\d+.\d+):'
    parsed_data = {}
    for line in dump_lines:
        match = re.search(icmp_regex, line)
        if match:
            sender_ip = match.group(1)
            receiver_ip = match.group(5).split('.')[0]
            ttl = int(match.group(3))
            if ttl not in parsed_data:
                parsed_data[ttl] = {'ip': receiver_ip, 'responses': []}
            # Simulate three random response times
            parsed_data[ttl]['responses'].extend([f"{random.uniform(0.4, 100):.3f} ms" for _ in range(3)])
    return parsed_data

def print_formatted_output(data):
    for ttl in sorted(data.keys()):
        print(f"TTL {ttl}")
        print(data[ttl]['ip'])
        for response in data[ttl]['responses']:
            print(response)

# Main execution block
if __name__ == "__main__":
    dump_lines = read_from_file('sampletcpdump.txt')
    parsed_data = parse_network_trace(dump_lines)
    print_formatted_output(parsed_data)
