import json

def print_yellow(text):
    print("\033[93m" + text + "\033[0m")

def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

def list_all_hosts(data):
    print_yellow("\n--- All Hosts ---")
    for host in data['nmaprun']['hosts']:
        print_yellow(f"Host: {host['address']}, Hostnames: {', '.join(host.get('hostnames', []))}")
    print_yellow("\n--- End of Hosts List ---\n")

def find_hosts_by_service(data, service_name):
    print_yellow(f"\n--- Hosts Running {service_name} ---")
    for host in data['nmaprun']['hosts']:
        for port in host.get('ports', []):
            if port['state'] == 'open' and port['service']['name'] == service_name:
                print_yellow(f"Host: {host['address']} is running {service_name} on port {port['portid']}")
    print_yellow("\n--- End of Service Search ---\n")

def summarize_open_ports(data):
    print_yellow("\n--- Open Ports Summary ---")
    for host in data['nmaprun']['hosts']:
        print_yellow(f"\nHost: {host['address']}")
        open_ports = [port['portid'] for port in host.get('ports', []) if port['state'] == 'open']
        if open_ports:
            print_yellow("  Open Ports: " + ", ".join(open_ports))
        else:
            print_yellow("  No open ports")
    print_yellow("\n--- End of Open Ports Summary ---\n")

def list_all_services(data):
    print_yellow("\n--- Services Running on Each Host ---")
    for host in data['nmaprun']['hosts']:
        print_yellow(f"\nHost: {host['address']}")
        services_found = False
        for port in host.get('ports', []):
            service = port.get('service')
            if service and port['state'] == 'open':
                print_yellow(f"  Service: {service['name']} on Port {port['portid']}")
                services_found = True
        if not services_found:
            print_yellow("  No services found")
    print_yellow("\n--- End of Services List ---\n")

def list_all_operating_systems(data):
    print_yellow("\n--- Operating Systems and Their Hosts ---")
    os_dict = {}
    for host in data['nmaprun']['hosts']:
        os_name = host.get('os')
        if os_name:
            if os_name not in os_dict:
                os_dict[os_name] = []
            os_dict[os_name].append(host['address'])

    for os_name, hosts in os_dict.items():
        print_yellow(f"\nOperating System: {os_name}")
        for host in hosts:
            print_yellow(f"  - Host: {host}")
    print_yellow("\n--- End of Operating Systems List ---\n")

def identify_hosts_with_port(data, portid):
    print_yellow(f"\n--- Hosts with Port {portid} Open ---")
    for host in data['nmaprun']['hosts']:
        if any(port['portid'] == portid and port['state'] == 'open' for port in host.get('ports', [])):
            print_yellow(f"Host: {host['address']} has port {portid} open")
    print_yellow("\n--- End of Port Search ---\n")

def display_host_details(data, host_address):
    print_yellow(f"\n--- Details for Host: {host_address} ---")
    for host in data['nmaprun']['hosts']:
        if host['address'] == host_address:
            print_yellow(json.dumps(host, indent=4))
    print_yellow("\n--- End of Host Details ---\n")

def find_services_with_versions(data):
    print_yellow("\n--- Services with Version Information ---")
    for host in data['nmaprun']['hosts']:
        for port in host.get('ports', []):
            service = port.get('service')
            if service and 'version' in service:
                print_yellow(f"Host: {host['address']} runs {service['name']} version {service['version']} on port {port['portid']}")
    print_yellow("\n--- End of Services with Versions ---\n")

# Main function remains the same
# Main function to run the program
def main():
    filename = input("Enter the path to the JSON file: ")
    data = load_json_data(filename)

    while True:
        print("\nChoose an option:")
        print("1. List all hosts")
        print("2. Find hosts by service")
        print("3. Summarize open ports for each host")
        print("4. List host-services on specific ports")
        print("5. List hosts by operating system")
        print("6. Identify hosts with a specific open port")
        print("7. Display full details of a specific host")
        print("8. Find services with version information")
        print("9. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_all_hosts(data)
        elif choice == '2':
            service = input("Enter service name: ")
            find_hosts_by_service(data, service)
        elif choice == '3':
            summarize_open_ports(data)
        elif choice == '4':
            list_all_services(data)
        elif choice == '5':
            list_all_operating_systems(data)
        elif choice == '6':
            port = input("Enter port number: ")
            identify_hosts_with_port(data, port)
        elif choice == '7':
            host_address = input("Enter host address: ")
            display_host_details(data, host_address)
        elif choice == '8':
            find_services_with_versions(data)
        elif choice == '9':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
