from django.shortcuts import render
from jsonrpclib import Server
import jsonrpclib
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def arista_data(request):
    # Connect to Arista switch using eAPI
    switch = Server("https://admin:admin@10.36.81.61/command-api")
    response = switch.runCmds(1, ["show interfaces"], "json")
    interfaces_list = list(response[0]['interfaces'].items())
    data = []
    for intf_name, intf_data in interfaces_list:
        # Check if interface is up or down
        link_status = intf_data.get('lineProtocolStatus', 'N/A')
        if link_status == 'up':
            status = '<span class="dot-green"></span>'
        else:
            status = '<span class="dot-red"></span>'
        # Add interface data to the list
        data.append({
            'name': intf_name,
            'status': status,
        })
    # Group interfaces by pairs for tabular representation
    table_data = []
    for i in range(0, len(data), 2):
        row_data = []
        for j in range(2):
            if i+j < len(data):
                row_data.append(data[i+j])
            else:
                row_data.append({'name': '', 'status': ''})
        table_data.append(row_data)
    # Render the webpage with response data as context
    return render(request, 'arista_data.html', {'table_data': table_data})
