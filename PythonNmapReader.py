
#filename = "/Users/nct/Desktop/scan_results.json"
import json
import webbrowser
from pathlib import Path

# Global dataset to store results
results_dataset = []


# Function to add results to the dataset
def add_to_dataset(entry):
    results_dataset.append(entry)


# Function to load data from JSON file
def load_json_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)


# Function to list services by host
def list_services_by_host(data):
    output = ""
    for host in data.get('hosts', []):
        # Bold and red for HTML, red for terminal
        host_info_html = f"<strong>Host: {host['address']} ({', '.join(host.get('hostnames', []))})</strong>"
        host_info_terminal = f"\033[91mHost: {host['address']} ({', '.join(host.get('hostnames', []))})\033[0m"
        print(host_info_terminal)
        output += host_info_html + "<br>"

        for port in host.get('ports', []):
            service = port.get('service')
            if service:
                # Yellow for terminal
                service_info = f"  Service: {service.get('name')} on Port {port['portid']}"
                print(f"\033[93m{service_info}\033[0m")
                output += service_info + "<br>"

        output += "<br>"  # Extra line break for spacing
    add_to_dataset(output)


# Function to find a specific service across all hosts
def find_specific_service(data, service_name):
    output = f"Hosts with {service_name}:\n"
    print(f"\033[91m{output.strip()}\033[0m")  # Yellow text
    for host in data.get('hosts', []):
        for port in host.get('ports', []):
            service = port.get('service')
            if service and service.get('name') == service_name:
                host_info = f"  Host: {host['address']} on Port {port['portid']}"
                print(f"\033[93m{host_info}\033[0m")  # Yellow text
                output += host_info + "\n"
    add_to_dataset(output)


# Function to summarize open ports by protocol
def summarize_ports_by_protocol(data):
    tcp_count, udp_count = 0, 0
    for host in data.get('hosts', []):
        for port in host.get('ports', []):
            if port.get('state') == 'open':
                if port.get('protocol') == 'tcp':
                    tcp_count += 1
                elif port.get('protocol') == 'udp':
                    udp_count += 1
    output = f"Open TCP Ports: {tcp_count}\nOpen UDP Ports: {udp_count}"
    print(f"\033[91m{output.strip()}\033[0m")  # Yellow text
    add_to_dataset(output)


# Function to identify operating systems
def identify_operating_systems(data):
    os_dict = {}
    for host in data.get('hosts', []):
        os = host.get('os')
        if os:
            os_dict.setdefault(os, []).append(host['address'])

    output = ""
    for os, hosts in os_dict.items():
        os_info = f"OS: {os}, Hosts: {', '.join(hosts)}"
        print(f"\033[93m{os_info}\033[0m")  # Yellow text
        output += os_info + "\n"
    add_to_dataset(output)


def list_open_ports_by_ipv4(data):
    output = ""
    for host in data.get('hosts', []):
        ip_address = host['address']
        ip_address_html = f"<strong>{ip_address}</strong>"
        ip_address_terminal = f"\033[91m{ip_address}\033[0m"
        print(ip_address_terminal)
        output += ip_address_html + "<br>"

        open_ports = [port for port in host.get('ports', []) if port.get('state') == 'open']
        for port in open_ports:
            port_info = f"  Open Port: {port['portid']}"
            print(f"\033[93m{port_info}\033[0m")
            output += port_info + "<br>"

        output += "<br>"  # Extra line break for spacing
    add_to_dataset(output)


# Function to print the entire JSON file
def print_json(data):
    print(json.dumps(data, indent=4))


# Function to save results to an HTML file and open in browser
def export_results_to_html(filename='results.html'):
    html_content = "<html><head><title>Nmap Scan Results</title></head><body><h1>BigDig Vulnerabilities \nNmap Scan Results</h1>"
    for entry in results_dataset:
        # Split the entry into lines and add <br> tags
        lines = entry.split('\n')
        for line in lines:
            html_content += f"{line}<br>"
        html_content += "<br>"  # Additional line break between sections

    html_content += "</body></html>"

    with open(filename, 'w') as file:
        file.write(html_content)

    # Open the HTML file in the default browser
    webbrowser.open(f'file://{Path(filename).resolve()}')


# Main function to run the program
def main():
    filename = input("Enter the path to the JSON file: ")
    data = load_json_data(filename)

    while True:
        print("\nChoose an option:")
        print("1. List services by host")
        print("2. Find a specific service across all hosts")
        print("3. Summarize open ports by protocol")
        print("4. Identify operating systems")
        print("5. List open ports by IP")
        print("6. Print entire JSON file")
        print("7. Export results to HTML and open in browser")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_services_by_host(data)
        elif choice == '2':
            service_name = input("Enter the service name to search: ")
            find_specific_service(data, service_name)
        elif choice == '3':
            summarize_ports_by_protocol(data)
        elif choice == '4':
            identify_operating_systems(data)
        elif choice == '5':
            list_open_ports_by_ipv4(data)
        elif choice == '6':
            print_json(data)
        elif choice == '7':
            export_results_to_html()
        elif choice == '8':
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
