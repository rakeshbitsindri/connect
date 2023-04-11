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

    physical_data = []
    vlan_data = []
    port_channel_data = []
    for intf_name, intf_data in interfaces_list:
        # Check if interface is up or down
        link_status = intf_data.get('lineProtocolStatus', 'N/A')
        if link_status == 'up':
            status = '<span class="dot-green"></span>'
        else:
            status = '<span class="dot-red"></span>'
        # Add interface data to the list
        if intf_name.startswith('Ethernet'):
            physical_data.append({
                'name': intf_name,
                'status': status,
                'speed': intf_data.get('bandwidth', 'N/A'),
                'description': intf_data.get('description', '')
            })
        elif intf_name.startswith('Vlan'):
            vlan_data.append({
                'name': intf_name,
                'status': status,
            })
        elif intf_name.startswith('Port-Channel'):
            port_channel_data.append({
                'name': intf_name,
                'status': status,
                'speed': intf_data.get('bandwidth', 'N/A'),
                'description': intf_data.get('description', '')
            })

    # Sort physical interfaces
    physical_data = sorted(physical_data, key=lambda k: (int(k['name'].split('/')[0][8:]), int(k['name'].split('/')[1].split('/')[0]) if len(k['name'].split('/')) > 1 else 0, int(k['name'].split('/')[1].split('/')[1]) if len(k['name'].split('/')) > 2 else 0))

    # Group physical interfaces by pairs for tabular representation
    physical_table_data = []
    for i in range(0, len(physical_data), 16):
        row_data = []
        for j in range(16):
            if i+j < len(physical_data):
                row_data.append(physical_data[i+j])
            else:
                row_data.append({'name': '', 'status': '', 'speed': '', 'description': ''})
        physical_table_data.append(row_data)

    # Sort vlan interfaces
    vlan_data = sorted(vlan_data, key=lambda k: int(k['name'].split('Vlan')[1]))

    # Render the webpage with response data as context
    return render(request, 'arista_data.html', {'physical_table_data': physical_table_data, 'vlan_data': vlan_data, 'port_channel_data': port_channel_data})
