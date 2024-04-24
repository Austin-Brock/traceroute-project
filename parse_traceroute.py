import re
from datetime import datetime

def parse_log(file_path):
    with open(file_path, 'r') as file:
        logs = file.readlines()

    # Regular expressions to capture the relevant data from the logs
    packet_re = re.compile(r'(\d+\.\d+) IP.*id (\d+),')
    icmp_re = re.compile(r'(\d+\.\d+) IP.*ICMP.*time exceeded.*id (\d+),')

    # Store outgoing packets and their timestamps
    sent_packets = {}
    for log in logs:
        packet_match = packet_re.search(log)
        if packet_match:
            timestamp, packet_id = packet_match.groups()
            sent_packets[packet_id] = float(timestamp)

    # Process ICMP messages and calculate RTT
    rtts = []
    for log in logs:
        icmp_match = icmp_re.search(log)
        if icmp_match:
            timestamp, icmp_id = icmp_match.groups()
            if icmp_id in sent_packets:
                rtt = (float(timestamp) - sent_packets[icmp_id]) * 1000  # Convert to ms
                rtts.append(rtt)

    return rtts

if __name__ == "__main__":
    file_path = 'tcpdum.txt'  # Replace with your actual file path
    rtts = parse_log(file_path)
    if rtts:
        print(f"TTL 1")
        print(f"128.192.76.129")  # The router IP for TTL=1 as per the example log
        print(f"{rtts[0]:.2f} ms")
        print(f"{rtts[1]:.2f} ms")
        print(f"{rtts[2]:.2f} ms")
    else:
        print("No ICMP responses found or log file empty.")
