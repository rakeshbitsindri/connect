from django.shortcuts import render, redirect
from django.contrib import messages
from jsonrpclib import Server
from .models import Device
from .forms import DeviceForm
import json
import requests
from django.http import HttpResponse
import ssl
from django.views.decorators.csrf import csrf_protect




ssl._create_default_https_context = ssl._create_unverified_context
session = None

# ip_address = '10.36.81.61'
# username = 'admin'
# password = 'password'

@csrf_protect
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

@csrf_protect
def user_login(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Test connection to Arista switch using eAPI
        try:
            switch = Server("https://admin:admin@10.36.81.61/command-api")
            switch.runCmds(1, ["show interfaces"], "json")
        except jsonrpclib.ProtocolError:
            messages.error(request, 'Error connecting to Arista device. Please check your login credentials and try again.')
            return redirect('login')

        request.session['ip_address'] = ip_address
        request.session['username'] = username
        request.session['password'] = password

        messages.success(request, 'Successfully connected to Arista device.')
        return redirect('arista_data')
    return render(request, 'login.html')

@csrf_protect
def user_logout(request):
    if 'ip_address' in request.session:
        del request.session['ip_address']
    if 'username' in request.session:
        del request.session['username']
    if 'password' in request.session:
        del request.session['password']
    return render(request, 'home.html')

@csrf_protect
def home(request):
    return render(request, 'home.html')

@csrf_protect
def add_device(request):
    if request.method == 'POST':
        ip_address = request.POST.get('ip_address')
        username = request.POST.get('username')
        password = request.POST.get('password')
        device = Device(ip_address=ip_address, username=username, password=password)
        device.save()
        return redirect('arista_data')
    return render(request, 'connect/add_device.html')

@csrf_protect
def delete_device(request, device_id):
    device = Device.objects.get(pk=device_id)
    device.delete()
    return redirect('arista_data')

@csrf_protect
def edit_device(request, device_id):
    device = Device.objects.get(pk=device_id)
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            return redirect('arista_data')
    else:
        form = DeviceForm(instance=device)
    return render(request, 'connect/edit_device.html', {'form': form})


# def arista_data(request):
    # if 'ip_address' not in request.session or 'username' not in request.session or 'password' not in request.session:
        # return redirect('home')

    # ip_address = request.session['ip_address']
    # username = request.session['username']
    # password = request.session['password']

    # devices = Device.objects.all()
    # device_data = []

    # for device in devices:
        # ip_address = device.ip_address
        # username = device.username
        # password = device.password
        # device_id = device.id

        # # Connect to Arista switch using eAPI
        # switch_url = f"https://{username}:{password}@{ip_address}/command-api"
        # switch = Server(switch_url)
        # response = switch.runCmds(1, ["show interfaces"], "json")
        # interfaces_list = list(response[0]['interfaces'].items())
            
        # device_data.append({
            # 'device_id': device_id,
            # 'ip_address': ip_address,
            # 'physical_table_data': physical_table_data,
            # 'vlan_data': vlan_data,
            # 'port_channel_data': port_channel_data,
        # })

    # physical_data = []
    # vlan_data = []
    # port_channel_data = []
    # for intf_name, intf_data in interfaces_list:
        # # Check if interface is up or down
        # link_status = intf_data.get('lineProtocolStatus', 'N/A')
        # if link_status == 'up':
            # status = '<span class="dot-green"></span>'
        # else:
            # status = '<span class="dot-red"></span>'
        # # Add interface data to the list
        # if intf_name.startswith('Ethernet'):
            # physical_data.append({
                # 'name': intf_name,
                # 'status': status,
                # 'speed': intf_data.get('bandwidth', 'N/A'),
                # 'description': intf_data.get('description', '')
            # })
        # elif intf_name.startswith('Vlan'):
            # vlan_data.append({
                # 'name': intf_name,
                # 'status': status,
            # })
        # elif intf_name.startswith('Port-Channel'):
            # port_channel_data.append({
                # 'name': intf_name,
                # 'status': status,
                # 'speed': intf_data.get('bandwidth', 'N/A'),
                # 'description': intf_data.get('description', '')
            # })

    # # Sort physical interfaces
    # physical_data = sorted(physical_data, key=lambda k: (int(k['name'].split('/')[0][8:]), int(k['name'].split('/')[1].split('/')[0]) if len(k['name'].split('/')) > 1 else 0, int(k['name'].split('/')[1].split('/')[1]) if len(k['name'].split('/')) > 2 else 0))

    # # Group physical interfaces by pairs for tabular representation
    # physical_table_data = []
    # for i in range(0, len(physical_data), 16):
        # row_data = []
        # for j in range(16):
            # if i+j < len(physical_data):
                # row_data.append(physical_data[i+j])
            # else:
                # row_data.append({'name': '', 'status': '', 'speed': '', 'description': ''})
        # physical_table_data.append(row_data)

    # # Sort vlan interfaces
    # vlan_data = sorted(vlan_data, key=lambda k: int(k['name'].split('Vlan')[1]))

    # # Render the webpage with response data as context
    # return render(request, 'arista_data.html', {'physical_table_data': physical_table_data, 'vlan_data': vlan_data, 'port_channel_data': port_channel_data})
    
@csrf_protect    
def generic_command(request, cmd):
    if 'ip_address' not in request.session or 'username' not in request.session or 'password' not in request.session:
        return redirect('home')

    ip_address = request.session['ip_address']
    username = request.session['username']
    password = request.session['password']

    devices = Device.objects.all()

    for device in devices:
        ip_address = device.ip_address
        username = device.username
        password = device.password
        device_id = device.id

        # Connect to Arista switch using eAPI
        switch_url = f"https://{username}:{password}@{ip_address}/command-api"
        switch = Server(switch_url)
        try:
            response = switch.runCmds(1, [cmd], "json")
            generic_command_response = response
        except jsonrpclib.ProtocolError:
            messages.error(request, 'Error executing the command on the Arista device. Please check your login credentials and try again.')
            return redirect('home')

    # Render the webpage with response data as context
    return render(request, 'generic_command_response.html', {'generic_command_response': generic_command_response})