import re
import random

# Function to parse the network trace dump
def parse_network_trace(dump_lines):
    data = {}
    for line in dump_lines:
        if 'IP' in line:
            parts = line.split()
            timestamp = parts[0]
            ttl = int(re.search(r'ttl (\d+)', line).group(1))
            if ttl not in data:
                data[ttl] = {
                    'timestamp': timestamp,
                    'ips': [],
                    'times': []
                }
        else:
            ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)\.\d+ > (\d+\.\d+\.\d+\.\d+)\.\d+', line)
            if ip_match:
                src_ip, dst_ip = ip_match.groups()
                # Simulate response times for demonstration purposes
                response_times = [f"{round(random.uniform(3, 100), 3)} ms" for _ in range(3)]
                data[ttl]['ips'].append(dst_ip)
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

# Sample input from the network trace dump
sample_dump_lines = [
    '1296184417.509580 IP (tos 0x0, ttl 1, id 30632, offset 0, flags [none], proto TCP (6), length 60)',
    '    128.192.76.178.35952 > 212.58.244.68.80: Flags [SEW], cksum 0xc2c4 (correct), seq 1857692485, win 5840, options [mss 1460,sackOK,TS val 1090680828 ecr 0,nop,wscale 2], length 0',
    # Additional sample lines for demonstration
    '1296184417.509599 IP (tos 0x0, ttl 2, id 30633, offset 0, flags [none], proto TCP (6), length 60)',
    '    128.192.76.178.38611 > 212.58.244.68.80: Flags [SEW], cksum 0x97a4 (correct), seq 3741111231, win 5840, options [mss 1460,sackOK,TS val 1090680828 ecr 0,nop,wscale 2], length 0',
]

# Parsing the dump and preparing the formatted output
parsed_data = parse_network_trace(sample_dump_lines)
print_formatted_output(parsed_data)


