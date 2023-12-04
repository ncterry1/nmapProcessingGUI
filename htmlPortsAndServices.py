
def generate_html_for_scan_results(scan_results):
    """
    Generates HTML code for displaying scan results in a table format.
    The scan results should be a dictionary with ports as keys and services as values.
    """
    html = '''
    <html>
    <head>
        <title>Scan Results</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .scan-results-container { width: 50%; float: left; }
            .scan-results { border-collapse: collapse; width: 100%; }
            .scan-results td, .scan-results th { border: 1px solid #ddd; padding: 8px; }
            .scan-results th { padding-top: 12px; padding-bottom: 12px; text-align: left; background-color: #4CAF50; color: white; }
            .scan-results, .scan-results-container { border: 2px solid black; }
        </style>
    </head>
    <body>
        <div class="scan-results-container">
            <h2>Port Scan Results</h2>
            <table class="scan-results">
                <tr>
                    <th>Port</th>
                    <th>Service</th>
                </tr>
    '''

    for port, service in scan_results.items():
        html += f'''
            <tr>
                <td>{port}</td>
                <td>{service}</td>
            </tr>
        '''

    html += '''
            </table>
        </div>
    </body>
    </html>
    '''

    return html

# Example usage remains the same
scan_results = {
    '80': 'HTTP',
    '443': 'HTTPS',
    '22': 'SSH',
    '21': 'FTP',
    '25': 'SMTP',
    '110': 'POP3',
    '143': 'IMAP',
    '53': 'DNS',
    '3306': 'MySQL',
    '8080': 'HTTP-alt'
}
html_content = generate_html_for_scan_results(scan_results)

# Save to HTML file
with open('scan_results.html', 'w') as file:
    file.write(html_content)