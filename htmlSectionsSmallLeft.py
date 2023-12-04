def generate_html_with_cse_style(port_service_dict, host_status, closed_filtered_ports, script_outputs):
    """
    Generates an HTML page styled to resemble the Canadian Centre for Cyber Security theme.
    Includes a top header displaying host status, a vertical sidebar (1/3 width) with port-service
    data and closed/filtered ports data, and a main content area (2/3 width) split into three sections.
    The bottom right section displays script output data.
    """
    # Convert port:service dictionary into HTML list items
    port_service_items = ''.join(f'<li>{port}: {service}</li>' for port, service in port_service_dict.items())

    # Convert host status into a formatted string for the header
    host_status_str = ', '.join(f'{key}: {value}' for key, value in host_status.items())

    # Convert closed/filtered ports data into a formatted string for display
    closed_filtered_ports_str = ', '.join(f'{key}: {value}' for key, value in closed_filtered_ports.items())

    # Convert script outputs into a formatted string for display
    script_output_items = '<br>'.join(f'{key}: {value}' for key, value in script_outputs.items())

    # Placeholder image URLs (replace with actual image URLs or paths)
    image_url_1 = "https://via.placeholder.com/50"
    image_url_2 = "https://via.placeholder.com/50"
    image_url_3 = "https://via.placeholder.com/50"
    image_url_4 = "https://via.placeholder.com/150"
    image_url_5 = "https://via.placeholder.com/150"
    image_url_6 = "https://via.placeholder.com/150"

    # HTML content with style and layout definitions
    html = f'''
        <html>
        <head>
            <title>Cybersecurity Page Layout</title>
            <style>
                body {{ 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                    margin: 0; padding: 0; 
                    border: 5px solid #333; 
                    background: #f0f0f0; 
                }}
                .header {{ 
                    background-color: #333333; 
                    color: #e7e7e7; 
                    text-align: center; 
                    padding: 20px; 
                    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); 
                }}
                .container {{ 
                    display: flex; 
                }}
                .sidebar {{ 
                    width: 33%; 
                    background-color: #e7e7e7; 
                    padding: 10px; 
                    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); 
                }}
                .main-content {{ 
                    width: 67%; 
                    padding: 10px; 
                }}
                .section {{ 
                    border: 2px solid #ddd; 
                    padding: 20px; 
                    margin-bottom: 10px; 
                    background-color: white; 
                    border-radius: 10px; 
                    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2); 
                    text-align: center;
                }}
                .port-service-list, .script-output-list {{ 
                    list-style-type: none; 
                    padding-left: 0; 
                }}
                img {{ 
                    max-width: 100%; 
                    height: auto; 
                    border-radius: 5px; 
                    margin-bottom: 10px;
                }}
                h1, h3 {{ 
                    color: #0056b3; 
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Host Status: {host_status_str}</h1>
            </div>
            <div class="container">
                <div class="sidebar">
                    <div class="section">
                        <img src="{image_url_1}" alt="Image 1">
                        <h3>Port-Service Data</h3>
                        <ul class="port-service-list">{port_service_items}</ul>
                    </div>
                    <div class="section">
                        <img src="{image_url_2}" alt="Image 2">
                        <h3>Closed/Filtered Ports</h3>
                        <p>{closed_filtered_ports_str}</p>
                    </div>
                    <div class="section">
                        <img src="{image_url_3}" alt="Image 3">
                        <h3>Additional Info</h3>
                    </div>
                </div>
                <div class="main-content">
                    <div class="section">
                        <img src="{image_url_4}" alt="Image 4">
                        <h3>Main Content Section 1</h3>
                    </div>
                    <div class="section">
                        <img src="{image_url_5}" alt="Image 5">
                        <h3>Main Content Section 2</h3>
                    </div>
                    <div class="section">
                        <img src="{image_url_6}" alt="Image 6">
                        <h3>Script Outputs</h3>
                        <p class="script-output-list">{script_output_items}</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        '''

    return html

# Example usage of the function with dummy data
port_service_dict = {
    '80': 'HTTP',
    '443': 'HTTPS',
    '22': 'SSH',
    # ... other ports and services ...
}

host_status = {
    "Status": "up",
    "Reason": "reset",
    "Address": "172.217.13.163",
    # ... other host status details ...
}

closed_filtered_ports = {
    "1000-2000": "closed",
    "3000-4000": "filtered",
    # ... other closed/filtered port ranges ...
}

script_outputs = {
    "Port 80": "Apache server running",
    "Port 443": "Nginx server running",
    # ... other script outputs ...
}

# Generate HTML content and save to file
html_content = generate_html_with_cse_style(port_service_dict, host_status, closed_filtered_ports, script_outputs)
with open('complex_layout_page.html', 'w') as file:
    file.write(html_content)
