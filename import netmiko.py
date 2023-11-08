from netmiko import ConnectHandler
import time

# Define the device information
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': input('Enter Username: '),  # The Username is "prne"
    'password': input('Enter Password: '),  # The Password is "cisco123!"
    'secret': 'class123!',  # Enable password
    'timeout': 60,  # Set a longer timeout value (adjust as needed)
}

# Loopback interfaces and their IP addresses/subnet masks
loopback_interfaces = {
    'Loopback0': {'ip_address': '192.168.1.1', 'subnet_mask': '255.255.255.0'},
    'Loopback1': {'ip_address': '192.168.1.2', 'subnet_mask': '255.255.255.0'},
    'Loopback2': {'ip_address': '192.168.1.3', 'subnet_mask': '255.255.255.0'}
}

# Create a Netmiko SSH session
ssh_session = ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Introduce a delay for stability (optional)
time.sleep(2)

# Send a command to change the hostname
new_hostname = 'R2'
config_commands = [f'hostname {new_hostname}']
ssh_session.send_config_set(config_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure loopback interfaces with IP addresses and subnet masks
for interface, details in loopback_interfaces.items():
    loopback_commands = [
        f'interface {interface}',
        f'ip address {details["ip_address"]} {details["subnet_mask"]}',
    ]

    ssh_session.send_config_set(loopback_commands)
    time.sleep(2)

# Configure EIGRP to advertise the loopback interfaces
eigrp_commands = [
    'router eigrp 1',  # Assuming you are configuring EIGRP process ID 1
]

for interface, details in loopback_interfaces.items():
    eigrp_commands.append(f'network {details["ip_address"]} 0.0.0.0')

ssh_session.send_config_set(eigrp_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure RIP to advertise the loopback interfaces
rip_commands = [
    'router rip',
]

for interface, details in loopback_interfaces.items():
    rip_commands.append(f'network {details["ip_address"]}')

ssh_session.send_config_set(rip_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Configure OSPF to advertise the loopback interfaces
ospf_commands = [
    'router ospf 1',  # Assuming you are configuring OSPF process ID 1
]

for interface, details in loopback_interfaces.items():
    ospf_commands.append(f'network {details["ip_address"]} 0.0.0.0 area 0')

ssh_session.send_config_set(ospf_commands)

# Introduce a delay for stability (optional)
time.sleep(2)

# Send a command to output the running configuration
output = ssh_session.send_command('show running-config')

# Save the running configuration to a file
output_file = 'running_config.txt'
with open(output_file, 'w') as config_file:
    config_file.write(output)

# Exit enable mode
ssh_session.exit_enable_mode()

# Disconnect from the device
ssh_session.disconnect()

# Display the information
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Password'))
print('{:<20} {:<15} {:<15}'.format(device_info['ip'], device_info['username'], device_info['password']))
print('--- Running Configuration saved to:', output_file)
print('--- Hostname changed to:', new_hostname)
for interface, details in loopback_interfaces.items():
    print(f'--- {interface} configured with IP address: {details["ip_address"]} and Subnet Mask: {details["subnet_mask"]}')
print('--- EIGRP, RIP, and OSPF configurations applied for Loopback interfaces')
print('------------------------------------------------------')
