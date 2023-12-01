'''
The provided JSON file seems to be an output from an Nmap scan,
which typically includes information about network hosts, ports, and services.
Administrators might be interested in functions that extract specific details
from this data, such as host status, open ports, services running on those ports,
and any specific scripts' output.

Here are a few Python functions tailored for this purpose:

    Function to Get Host Status:
    This function retrieves the status of the host (e.g., up or down).

    Function to List Open Ports:
    This extracts a list of open ports on the host.

    Function to Get Services on Ports:
    Retrieves information about services running on open ports.

    Function to Get Script Outputs:
    Extracts outputs of any scripts that were run on the ports.

    Function to Get Scan Summary:
    Provides a summary of the Nmap scan.

Here's how these functions could be implemented:
'''
import json
import os
import platform

# Intent to clear the terminal every time a function is run, but this is goofy is is not currently set
def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

# Global variable to hold all results
# This collection will be saved to html if user picks choice 11
collected_results = []

# After each function execution, we'll add its results, title, and summary to the global variable.
# If a user pics choice 11 then this collected results will be printed to html
def add_to_collected_results(title, data, summary):
    collected_results.append({'title': title, 'data': data, 'summary': summary})

# Load JSON data
with open('scratch1.json', 'r') as file:
    data = json.load(file)

# The most important.
# While it can be called and printed to the terminal
# It will always be the first printed to the html any time a user picks choice 11
def get_host_status(data):
    """
    Extracts detailed information about the host from the provided data.
    Includes status, address, address type, hostname, scanner used, scan arguments, and start time.
    """
    # Grabs any notable host details as a summary for the user
    # so the user know what the data in the json is from
    host_info = data.get("IPAddrInfo", {}).get("host", {})
    status = host_info.get("status", {})
    address_info = host_info.get("address", {})
    hostnames_info = host_info.get("hostnames", {}).get("hostname", {})
    scanner_info = data.get("IPAddrInfo", {}).get("scanner", "")
    args = data.get("IPAddrInfo", {}).get("args", "")
    startstr = data.get("IPAddrInfo", {}).get("startstr", "")

    detailed_host_info = {
        "Status": status.get("state"),
        "Reason": status.get("reason"),
        "Address": address_info.get("addr"),
        "Address Type": address_info.get("addrtype"),
        "Hostname": hostnames_info.get("name"),
        "Scanner": scanner_info,
        "Arguments": args,
        "Start Time": startstr
    }  # ---------------------
    return detailed_host_info

# Function to display all open ports on the host.
def list_open_ports(data):
    """
    Retrieves a list of open ports from the scan data.
    """
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {})
    return [port["portid"] for port in ports_info.get("port", []) if port.get("state", {}).get("state") == "open"]

# Function to
def get_services_on_ports(data):
    """
    Gathers information about services running on each open port.
    """
    services = {}
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {}).get("port", [])
    for port in ports_info:
        port_id = port.get("portid")
        service_name = port.get("service", {}).get("name")
        services[port_id] = service_name
    return services


def get_script_outputs(data):
    """
    Extracts the outputs of scripts executed by Nmap for each service.
    """
    script_outputs = {}
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {}).get("port", [])
    for port in ports_info:
        port_id = port.get("portid")
        scripts = port.get("script", [])
        for script in scripts:
            script_id = script.get("id")
            output = script.get("output")
            script_outputs[(port_id, script_id)] = output
    return script_outputs


def list_unique_services(data):
    """
    Lists all unique services discovered during the scan.
    """
    unique_services = set()
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {}).get("port", [])
    for port in ports_info:
        service_name = port.get("service", {}).get("name")
        if service_name:
            unique_services.add(service_name)
    return unique_services


def report_closed_filtered_ports(data):
    """
    Reports on ports that are closed or filtered according to the scan results.
    """
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {})
    closed_filtered = ports_info.get("extraports", {})
    return closed_filtered


def summarize_hostnames(data):
    """
    Summarizes all hostnames associated with the scanned IP.
    """
    hostnames = data.get("IPAddrInfo", {}).get("host", {}).get("hostnames", {})
    return hostnames


def detail_service_versions(data):
    """
    Details the versions of services running on open ports.
    """
    service_versions = {}
    ports_info = data.get("IPAddrInfo", {}).get("host", {}).get("ports", {}).get("port", [])
    for port in ports_info:
        port_id = port.get("portid")
        service_info = port.get("service", {})
        if service_info.get("name"):
            service_versions[port_id] = service_info
    return service_versions


def get_scan_summary(data):
    """
    Provides a general summary of the Nmap scan.
    """
    summary = data.get("IPAddrInfo", {}).get("runstats", {}).get("finished", {}).get("summary")
    return summary


def run_all_functions():
    """
    Executes all the above functions in sequence and collects their results.
    This function is useful for generating a comprehensive report from a single command.
    """
    # Host Status
    host_status = get_host_status(data)
    print_colored_and_separated(host_status, "Host Status")
    # Open Ports ****************************************
    open_ports = {"Open Ports": list_open_ports(data)}
    print_colored_and_separated(open_ports, "Open Ports")
    # Services on Ports ****************************************
    services_on_ports = get_services_on_ports(data)
    print_colored_and_separated(services_on_ports, "Services on Ports")
    # Script Outputs ****************************************
    script_outputs = get_script_outputs(data)
    print_colored_and_separated(script_outputs, "Script Outputs")
    # Scan Summary ****************************************
    scan_summary = {"Scan Summary": get_scan_summary(data)}
    print_colored_and_separated(scan_summary, "Scan Summary")
    # Unique Services ****************************************
    unique_services = {"Unique Services": list_unique_services(data)}
    print_colored_and_separated(unique_services, "Unique Services")
    # Closed/Filtered Ports Report ****************************************
    closed_filtered_ports = {"Closed/Filtered Ports": report_closed_filtered_ports(data)}
    print_colored_and_separated(closed_filtered_ports, "Closed/Filtered Ports Report")
    # Hostnames Summary ****************************************
    hostnames_summary = {"Hostnames": summarize_hostnames(data)}
    print_colored_and_separated(hostnames_summary, "Hostnames Summary")
    # Service Versions Detail ****************************************
    service_versions = detail_service_versions(data)
    print_colored_and_separated(service_versions, "Service Versions Detail")


def export_to_html(file_path):
    """
    Exports the collected data to an HTML file.
    Formats the data in a structured and professional manner for easy review.
    """
    with open(file_path, 'w') as html_file:
        html_file.write('<html><head><title>Scan Results</title></head><body>')
        html_file.write('<h1>Team 3 - Digital Defenders\nNmap Vulnerability Scan Results Summary</h1>')
        # Adding CSS for styling
        html_file.write('<style>')
        html_file.write('h2 { color: navy; }')  # Example of styling headings
        html_file.write('ul { line-height: 1.6; }')  # Example of styling list items
        html_file.write('</style>')

        # Closing head and starting body
        html_file.write('</head><body>')
        # Any call to print to HTML will always include this primary host information
        # Collect and store host status information
        host_status = get_host_status(data)
        html_file.write(f'<h2>{"Host Status"}</h2>')
        html_file.write(f'<h2>{"Displays the status, address, and other details of the host."}</h2>')
        # Assuming host_status is a dictionary
        # Loop prints the host_status line by line, not as a chunk
        for key, value in host_status.items():
            html_file.write(f'{key}: {value}<br>')
        # End Collect and post to HTML
        # We just printed the host status to the HTML always to start the html
        # this now prints all other saved results to the HTML
        for result in collected_results:
            html_file.write(f'<h2>{"--------------------------------------"}</h2>')
            html_file.write(f'<h2>{result["title"]}</h2>')
            html_file.write('<ul>')
            for key, value in result["data"].items():
                html_file.write(f'<li><b>{key}</b>: {value}</li>')
            html_file.write('</ul>')
            html_file.write(f'<p><i>{result["summary"]}</i></p>')
        html_file.write('</body></html>')

# Example Usage
# Set to the target json file for this current project
with open('scratch1.json', 'r') as file:
    data = json.load(file)

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


# Menu system
def menu():
    while True:
        print("\nChoose an option:")
        print("1. Host Status")
        print("2. Open Ports")
        print("3. Services on Ports")
        print("4. Script Outputs")
        print("5. Scan Summary")
        print("6. Unique Services")
        print("7. Closed/Filtered Ports Report")
        print("8. Hostnames Summary")
        print("9. Service Versions Detail")
        print("10. Run All Functions")
        print("11. Export Findings to HTML")
        print("0. Exit")
        # ... existing options for exiting ...
        choice = input("Enter your choice (0-10): ")

        if choice in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
            if choice == "1":
                print("\n\n\nSummary: Displays the status, address, and other details of the host.")
                print_colored_and_separated({"Host Status": get_host_status(data)}, "*************")
                input("\nPress Enter to continue...")
                # Any call to print to HTML will always include this primary host information

            elif choice == "2":
                print("\n\n\nSummary: Lists all open ports on the host.")
                print_colored_and_separated({"Open Ports": list_open_ports(data)}, "*************")
                input("\nPress Enter to continue...")
                # Collect and store information about open ports
                open_ports = {"Open Ports": list_open_ports(data)}
                add_to_collected_results(
                    "Open Ports",
                    open_ports,
                    "Lists all open ports on the host."
                )  # End Collect and post to HTML

            elif choice == "3":
                print("\n\n\nSummary: Shows services running on each open port.")
                services_on_ports = get_services_on_ports(data)
                print_colored_and_separated(services_on_ports,
                                            "*************\nServices on Ports" if services_on_ports else "No Services on Ports")
                input("\nPress Enter to continue...")
                # Collect and store information about services running on open ports
                services_on_ports = get_services_on_ports(data)
                add_to_collected_results(
                    "Services on Ports",
                    services_on_ports,
                    "Shows services running on each open port."
                )  # End Collect and post to HTML

            elif choice == "4":
                print("\n\n\nSummary: Displays the outputs of various scripts run by Nmap for each service.")
                script_outputs = get_script_outputs(data)
                print_colored_and_separated(script_outputs, "*************\nScript Outputs" if script_outputs else "No Script Outputs")
                input("\nPress Enter to continue...")
                # Collect and store outputs of scripts run by Nmap
                script_outputs = get_script_outputs(data)
                # This HTML addition messes up the file.
                #add_to_collected_results(
                #    "Script Outputs",
                #    script_outputs,
                #    "Displays the outputs of various scripts run by Nmap for each service."
                #)  # End Collect and post to HTML

            elif choice == "5":
                print("\n\n\nSummary: Provides a general summary of the Nmap scan.")
                print_colored_and_separated({"Scan Summary": get_scan_summary(data)}, "*************")
                input("\nPress Enter to continue...")
                # Collect and store a general summary of the Nmap scan
                scan_summary = {"Scan Summary": get_scan_summary(data)}
                add_to_collected_results(
                    "Scan Summary",
                    scan_summary,
                    "Provides a general summary of the Nmap scan."
                )  # End Collect and post to HTML

            elif choice == "6":
                print("\n\n\nSummary: Lists all unique services discovered during the scan.")
                print_colored_and_separated({"Unique Services": list_unique_services(data)}, "*************")
                input("\nPress Enter to continue...")
                # Collect and store a list of all unique services discovered during the scan
                unique_services = {"Unique Services": list_unique_services(data)}
                add_to_collected_results(
                    "Unique Services",
                    unique_services,
                    "Lists all unique services discovered during the scan."
                )  # End Collect and post to HTML

            elif choice == "7":
                print("\n\n\nSummary: Reports on ports that are closed or filtered.")
                print_colored_and_separated({"Closed/Filtered Ports": report_closed_filtered_ports(data)},
                                            "*************")
                input("\nPress Enter to continue...")
                # Collect and store information about closed or filtered ports
                closed_filtered_ports = {"Closed/Filtered Ports": report_closed_filtered_ports(data)}
                add_to_collected_results(
                    "Closed/Filtered Ports Report",
                    closed_filtered_ports,
                    "Reports on ports that are closed or filtered."
                )  # End Collect and post to HTML

            elif choice == "8":
                print("\n\n\nSummary: Summarizes all hostnames associated with the scanned IP.")
                print_colored_and_separated({"Hostnames": summarize_hostnames(data)}, "*************")
                input("\nPress Enter to continue...")
                # Collect and store a summary of all hostnames associated with the scanned IP
                hostnames_summary = {"Hostnames": summarize_hostnames(data)}
                add_to_collected_results(
                    "Hostnames Summary",
                    hostnames_summary,
                    "Summarizes all hostnames associated with the scanned IP."
                )  # End Collect and post to HTML

            elif choice == "9":
                print("\n\n\nSummary: Details the versions of services running on open ports.")
                print_colored_and_separated(detail_service_versions(data), "*************\nDetailed Services")
                input("\nPress Enter to continue...")
                # Collect and store detailed information about service versions on open ports
                service_versions = detail_service_versions(data)
                add_to_collected_results(
                    "Service Versions Detail",
                    service_versions,
                    "Details the versions of services running on open ports."
                )  # End Collect and post to HTML

            elif choice == "10":
                run_all_functions()
                input("\nPress Enter to continue...")

            elif choice == "11":
                # Call this function to export the data to HTML
                export_to_html('results.html')

            elif choice == "0":
                print("Exiting...")
                break
        else:
            print("Invalid choice. Please enter a number between 0 and 9.")


menu()
'''
The "Script Outputs" section in a JSON file contains the results of Nmap's 
script scans on open ports. These scripts perform various checks and gather 
additional information about the services running on these ports. In your 
provided JSON, there are script outputs for two different scripts: 
fingerprint-strings and http-server-header. explanation 
of their outputs:

    fingerprint-strings:
    This script attempts to identify the service running on an open 
    port by sending different types of requests and recording the 
    responses. The output contains the responses for various test 
    requests like GetRequest and HTTPOptions. These responses include 
    HTTP headers and other information that can be used to 
    fingerprint the web service.

    http-server-header:
    This script reports the HTTP server header (gws in this case, 
    which is short for Google Web Server).
'''