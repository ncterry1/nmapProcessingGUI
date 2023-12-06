import json
# Go collect the open port per IPv4 FUNCTION 1/4
global file_path
file_path = "scratch2.json"

##########################################
##########################################
##########################################
##########################################
##########################################
# ANSI escape codes for colors and separator
# This is to make the terminal printouts more readable
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
SEPARATOR = "-" * 50
# Printing functions with color and separators
# This is mainly just to make it easier to read it in the terminal
def print_colored_and_separated(data, title):
    print(SEPARATOR)
    print(f"{RED}{title}{RESET}")
    for key, value in data.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                print(f"{RED}{key} - {sub_key}{RESET}: {YELLOW}{sub_value}{RESET}")
        else:
            print(f"{RED}{key}{RESET}: {YELLOW}{value}{RESET}")

##########################################
##########################################
##########################################

def extract_hosts_and_services(data):
    results = {}
    for entry in data:
        if 'IPAddrInfo' in entry:
            ip_info = entry['IPAddrInfo']
            if 'host' in ip_info:
                host = ip_info['host']
                if 'address' in host and 'addr' in host['address']:
                    ip_addr = host['address']['addr']
                    results[ip_addr] = {'ports': []}
                    if 'ports' in host and 'port' in host['ports']:
                        ports = host['ports']['port']
                        # Ensure ports is a list
                        if not isinstance(ports, list):
                            ports = [ports]
                        for port_info in ports:
                            if isinstance(port_info, dict):
                                port = port_info.get('portid', 'unknown')
                                service = port_info.get('service', {}).get('name', 'unknown')
                                results[ip_addr]['ports'].append((port, service))
    return results

# Go collect the open port per IPv4 FUNCTION 2/4
##########################################
def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    file.close()
    return data

# Go collect the open port per IPv4 FUNCTION 3/4
##########################################
def print_formatted_results(results):
    for ip, info in results.items():
        print(f"IP Address: {ip}")
        for port, service in info['ports']:
            print(f"  Port: {port}, Service: {service}")
        print()  # Add a blank line for better separation between IP addresses

# Go collect the open port per IPv4 FUNCTION 4/4
##########################################
def get_hosts_and_associated_IPv4s():
    # Replace with your actual file path
    #file_path = 'scratch2.json'
    # Read the JSON data
    json_data = read_json(file_path)
    # Extract hosts and services
    host_services = extract_hosts_and_services(json_data)
    # Example usage
    print_formatted_results(host_services)

    '''
    IP Address: 131.138.48.65
      Port: 389, Service: ldap
    
    IP Address: 131.138.66.113
      Port: 389, Service: ldap
    
    IP Address: 131.138.57.66
      Port: 389, Service: ldap
    
    IP Address: 131.138.24.58
      Port: 389, Service: ldap
    
    IP Address: 131.138.59.2
      Port: 389, Service: ldap
    
    IP Address: 131.138.53.67
      Port: 389, Service: ldap
    '''

##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################

import json
##########################################
def extract_hosts_and_elapsed_times(data):
    host_times = {}

    for entry in data:
        ip_addr = entry.get("IPAddrInfo", {}).get("host", {}).get("address", {}).get("addr", "unknown")
        elapsed_time = entry.get("IPAddrInfo", {}).get("runstats", {}).get("finished", {}).get("elapsed", "unknown")

        if elapsed_time != "unknown":
            elapsed_time = float(elapsed_time)  # Convert to float for sorting

        host_times[ip_addr] = elapsed_time

    return host_times

##########################################
def rank_hosts_by_elapsed_time(host_times):
    # Sort hosts based on elapsed time
    ranked_hosts = sorted(host_times.items(), key=lambda x: x[1] if x[1] != "unknown" else float('inf'))
    return ranked_hosts

##########################################
def get_hosts_and_associated_elapsed_scantime():
    # Load JSON data from file
    with open(file_path, 'r') as file:
        data = json.load(file)
    file.close()

    # Process the data
    host_times = extract_hosts_and_elapsed_times(data)
    ranked_hosts = rank_hosts_by_elapsed_time(host_times)

    # Print results
    print("Elapsed port scan times for targeted hosts (RANKED)")
    for ip, time in ranked_hosts:
        print(f"IP Address: {ip}, Elapsed Scan Time: {time}")

    '''
    IP Address: 131.138.24.58, Elapsed Time: 4.65
    IP Address: 131.138.57.66, Elapsed Time: 4.79
    IP Address: 131.138.59.2, Elapsed Time: 5.0
    IP Address: 131.138.53.67, Elapsed Time: 5.13
    IP Address: 131.138.48.65, Elapsed Time: 6.04
    IP Address: 131.138.66.113, Elapsed Time: 8.99
    '''

##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
import json

def list_ipv4_addresses(data):
    ipv4_addresses = set()
    for entry in data:
        ip_addr = entry.get("IPAddrInfo", {}).get("host", {}).get("address", {}).get("addr", None)
        if ip_addr:
            ipv4_addresses.add(ip_addr)
    return list(ipv4_addresses)
##########################################

def get_info_for_ip(data, selected_ip):
    for entry in data:
        ip_addr = entry.get("IPAddrInfo", {}).get("host", {}).get("address", {}).get("addr", None)
        if ip_addr == selected_ip:
            return entry  # Return the entry that matches the selected IP
    return None  # Return None if no match is found
##########################################

def get_allInfo_forIPv4():
    # Load JSON data from file

    with open(file_path, 'r') as file:
        data = json.load(file)

    # List all IPv4 addresses
    ipv4_addresses = list_ipv4_addresses(data)
    print("Available IP Addresses:")
    for i, ip in enumerate(ipv4_addresses, 1):
        print(f"{i}. {ip}")

    # User selects an IP address
    choice = int(input("Enter the number of the IP address to get more info: ")) - 1
    selected_ip = ipv4_addresses[choice]

    # Retrieve and display information for the selected IP
    ip_info = get_info_for_ip(data, selected_ip)
    if ip_info:
        print(json.dumps(ip_info, indent=4))
    else:
        print("No information found for the selected IP address.")
'''
Available IP Addresses:
1. 131.138.53.67
2. 131.138.66.113
3. 131.138.24.58
4. 131.138.48.65
5. 131.138.57.66
6. 131.138.59.2
Enter the number of the IP address to get more info: 2
{
    "AAAAAClassification": "UNCLASS",
    "AAAAACollectionDate": "2023-12-05T04:57:22.480",
    "AAAAAEventTime": "2023-12-05T04:57:22.480",
    "AAAAAId": "0b1f6a0c-862a-4296-99d7-8d1ff1599bff",
    "AAAAAMa": "Non-MA (Tool Deployment) (2000/01/01-3000/01/01) [collected]",
    "AAAAAWorkload": "portray.nmap.parent",
    "IPAddrInfo": {
        "args": "nmap -T4 --host-timeout 2m -sV -oX /./portray-scan-12204773117869733105.xml 131.138.66.113",
        "debugging": {
            "level": "0"
        },
        "host": {
            "address": {
                "addr": "131.138.66.113",
                "addrtype": "ipv4"
            },
            "endtime": "1701752239",
            "hostnames": "\n",
            "ports": {
                "extraports": {
                    "count": "999",
                    "extrareasons": {
                        "count": "999",
                        "reason": "no-responses"
                    },
                    "state": "filtered"
                },
                "port": {
                    "portid": "389",
                    "protocol": "tcp",
                    "service": {
                        "conf": "3",
                        "method": "table",
                        "name": "ldap"
                    },
                    "state": {
                        "reason": "reset",
                        "reason_ttl": "230",
                        "state": "closed"
                    }
                }
            },
            "starttime": "1701752230",
            "status": {
                "reason": "reset",
                "reason_ttl": "180",
                "state": "up"
            },
            "times": {
                "rttvar": "20505",
                "srtt": "11280",
                "to": "100000"
            }
        },
        "runstats": {
            "finished": {
                "elapsed": "8.99",
                "exit": "success",
                "summary": "Nmap done at Tue Dec  5 04:57:19 2023; 1 IP address (1 host up) scanned in 8.99 seconds",
                "time": "1701752239",
                "timestr": "Tue Dec  5 04:57:19 2023"
            },
            "hosts": {
                "down": "0",
                "total": "1",
                "up": "1"
            }
        },
        "scaninfo": {
            "numservices": "1000",
            "protocol": "tcp",
            "services": "1,3-4,6-7,9,13,17,19-26,30,32-33,37,42-43,49,53,70,79-85,88-90,99-100,106,109-111,113,119,125,135,139,143-144,146,161,163,179,199,211-212,222,254-256,259,264,280,301,306,311,340,366,389,406-407,416-417,425,427,443-445,458,464-465,481,497,500,512-515,524,541,543-545,548,554-555,563,587,593,616-617,625,631,636,646,648,666-668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800-801,808,843,873,880,888,898,900-903,911-912,981,987,990,992-993,995,999-1002,1007,1009-1011,1021-1100,1102,1104-1108,1110-1114,1117,1119,1121-1124,1126,1130-1132,1137-1138,1141,1145,1147-1149,1151-1152,1154,1163-1166,1169,1174-1175,1183,1185-1187,1192,1198-1199,1201,1213,1216-1218,1233-1234,1236,1244,1247-1248,1259,1271-1272,1277,1287,1296,1300-1301,1309-1311,1322,1328,1334,1352,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666,1687-1688,1700,1717-1721,1723,1755,1761,1782-1783,1801,1805,1812,1839-1840,1862-1864,1875,1900,1914,1935,1947,1971-1972,1974,1984,1998-2010,2013,2020-2022,2030,2033-2035,2038,2040-2043,2045-2049,2065,2068,2099-2100,2103,2105-2107,2111,2119,2121,2126,2135,2144,2160-2161,2170,2179,2190-2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,2381-2383,2393-2394,2399,2401,2492,2500,2522,2525,2557,2601-2602,2604-2605,2607-2608,2638,2701-2702,2710,2717-2718,2725,2800,2809,2811,2869,2875,2909-2910,2920,2967-2968,2998,3000-3001,3003,3005-3007,3011,3013,3017,3030-3031,3052,3071,3077,3128,3168,3211,3221,3260-3261,3268-3269,3283,3300-3301,3306,3322-3325,3333,3351,3367,3369-3372,3389-3390,3404,3476,3493,3517,3527,3546,3551,3580,3659,3689-3690,3703,3737,3766,3784,3800-3801,3809,3814,3826-3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000-4006,4045,4111,4125-4126,4129,4224,4242,4279,4321,4343,4443-4446,4449,4550,4567,4662,4848,4899-4900,4998,5000-5004,5009,5030,5033,5050-5051,5054,5060-5061,5080,5087,5100-5102,5120,5190,5200,5214,5221-5222,5225-5226,5269,5280,5298,5357,5405,5414,5431-5432,5440,5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678-5679,5718,5730,5800-5802,5810-5811,5815,5822,5825,5850,5859,5862,5877,5900-5904,5906-5907,5910-5911,5915,5922,5925,5950,5952,5959-5963,5987-5989,5998-6007,6009,6025,6059,6100-6101,6106,6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565-6567,6580,6646,6666-6669,6689,6692,6699,6779,6788-6789,6792,6839,6881,6901,6969,7000-7002,7004,7007,7019,7025,7070,7100,7103,7106,7200-7201,7402,7435,7443,7496,7512,7625,7627,7676,7741,7777-7778,7800,7911,7920-7921,7937-7938,7999-8002,8007-8011,8021-8022,8031,8042,8045,8080-8090,8093,8099-8100,8180-8181,8192-8194,8200,8222,8254,8290-8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651-8652,8654,8701,8800,8873,8888,8899,8994,9000-9003,9009-9011,9040,9050,9071,9080-9081,9090-9091,9099-9103,9110-9111,9200,9207,9220,9290,9415,9418,9485,9500,9502-9503,9535,9575,9593-9595,9618,9666,9876-9878,9898,9900,9917,9929,9943-9944,9968,9998-10004,10009-10010,10012,10024-10025,10082,10180,10215,10243,10566,10616-10617,10621,10626,10628-10629,10778,11110-11111,11967,12000,12174,12265,12345,13456,13722,13782-13783,14000,14238,14441-14442,15000,15002-15004,15660,15742,16000-16001,16012,16016,16018,16080,16113,16992-16993,17877,17988,18040,18101,18988,19101,19283,19315,19350,19780,19801,19842,20000,20005,20031,20221-20222,20828,21571,22939,23502,24444,24800,25734-25735,26214,27000,27352-27353,27355-27356,27715,28201,30000,30718,30951,31038,31337,32768-32785,33354,33899,34571-34573,35500,38292,40193,40911,41511,42510,44176,44442-44443,44501,45100,48080,49152-49161,49163,49165,49167,49175-49176,49400,49999-50003,50006,50300,50389,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055-55056,55555,55600,56737-56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,64680,65000,65129,65389",
            "type": "syn"
        },
        "scanner": "nmap",
        "start": "1701752230",
        "startstr": "Tue Dec  5 04:57:10 2023",
        "verbose": {
            "level": "0"
        },
        "version": "7.80",
        "xmloutputversion": "1.04"
    },
    "dept": "DND"
}
'''
##########################################
##########################################
##########################################
##########################################
##########################################
##########################################
def list_ipv4_addresses(data):
    ipv4_addresses = set()
    for entry in data:
        ip_addr = entry.get("IPAddrInfo", {}).get("host", {}).get("address", {}).get("addr", None)
        if ip_addr:
            ipv4_addresses.add(ip_addr)
    return list(ipv4_addresses)

def get_header_info_for_ip(data, selected_ip):
    for entry in data:
        ip_addr = entry.get("IPAddrInfo", {}).get("host", {}).get("address", {}).get("addr", None)
        if ip_addr == selected_ip:
            # Extract only the header information
            header_info = {key: entry[key] for key in entry if key.startswith("AAAAA")}
            header_info['dept'] = entry.get('dept', 'Unknown')
            # Append additional information
            header_info['IP Address'] = ip_addr
            header_info['Arguments'] = entry.get("IPAddrInfo", {}).get("args", "Not available")
            runstate_summary = entry.get("IPAddrInfo", {}).get("runstats", {}).get("finished", {}).get("summary", "Not available")
            header_info['Runstate Summary'] = runstate_summary
            return header_info
    return None  # Return None if no match is found

def get_headerInfo_forIPv4():
    # Load JSON data from file
    with open(file_path, 'r') as file:
        data = json.load(file)

    # List all IPv4 addresses
    ipv4_addresses = list_ipv4_addresses(data)
    print("Available IP Addresses:")
    for i, ip in enumerate(ipv4_addresses, 1):
        print(f"{i}. {ip}")

    # User selects an IP address
    choice = int(input("Enter the number of the IP address to get more info: ")) - 1
    selected_ip = ipv4_addresses[choice]

    # Retrieve and display header information for the selected IP
    header_info = get_header_info_for_ip(data, selected_ip)
    if header_info:
        print(json.dumps(header_info, indent=4))
    else:
        print("No header information found for the selected IP address.")
'''
Available IP Addresses:
1. 131.138.48.65
2. 131.138.24.58
3. 131.138.57.66
4. 131.138.66.113
5. 131.138.53.67
6. 131.138.59.2
Enter the number of the IP address to get more info: 2
{
    "AAAAAClassification": "UNCLASS",
    "AAAAACollectionDate": "2023-12-05T04:57:47.612",
    "AAAAAEventTime": "2023-12-05T04:57:47.612",
    "AAAAAId": "62b62598-c85f-4a7a-b251-703b4e098114",
    "AAAAAMa": "Non-MA (Tool Deployment) (2000/01/01-3000/01/01) [collected]",
    "AAAAAWorkload": "portray.nmap.parent",
    "dept": "DND",
    "IP Address": "131.138.24.58",
    "Arguments": "nmap -T4 --host-timeout 2m -sV -oX /./portray-scan-16765860935950010393.xml 131.138.24.58",
    "Runstate Summary": "Nmap done at Tue Dec  5 04:57:47 2023; 1 IP address (1 host up) scanned in 4.65 seconds"

'''

##########################################
##########################################
##########################################
# RUN THE FULL #
get_hosts_and_associated_IPv4s()
get_hosts_and_associated_elapsed_scantime()
get_allInfo_forIPv4()
get_headerInfo_forIPv4()
##########################################


