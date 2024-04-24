import re

def parse_trace_file(filename):
    data = {}
    with open(filename, 'r') as file:
        for line in file:
            # Match lines with initial packet info
            packet_info = re.search(r'(\d+\.\d+) IP.*? id (\d+),', line)
            if packet_info:
                data[packet_info.group(2)] = {'send_time': float(packet_info.group(1))}
            
            # Match lines with ICMP responses
            icmp_info = re.search(r'(\d+\.\d+) IP.*? > (.*?): ICMP.*?id (\d+),', line)
            if icmp_info:
                router_ip = icmp_info.group(2).split(' > ')[0]
                packet_id = icmp_info.group(3)
                if packet_id in data:
                    data[packet_id].update({
                        'router_ip': router_ip,
                        'response_time': float(icmp_info.group(1))
                    })

    return data

def compute_delays(data):
    output = []
    router_ip = set([info['router_ip'] for info in data.values() if 'router_ip' in info])
    if len(router_ip) == 1:
        router_ip = router_ip.pop()
        output.append("TTL 1")
        output.append(router_ip)
        for key, value in data.items():
            if 'response_time' in value:
                delay = (value['response_time'] - value['send_time']) * 1000
                output.append(f"{delay:.3f} ms")
    return output

def main():
    filename = "sampletcpdump.txt"
    trace_data = parse_trace_file(filename)
    results = compute_delays(trace_data)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
