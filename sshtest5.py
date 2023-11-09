from netmiko import ConnectHandler
import time
import getpass

# Define the device information
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),  # The Username is "prne"
    'password': getpass.getpass('Enter Password: '),  # The Password is "cisco123!"
    'secret': getpass.getpass('Enter Enable Password: '),  # Enable password- "Class123!"
    'timeout': 60,
}

# Create a Netmiko SSH session
ssh_session = ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Introduce a delay for stability
time.sleep(2)

# Configure loopback interface
loopback_interface = 'Loopback0'
loopback_ip = '10.0.0.1'
loopback_subnet_mask = '255.255.255.255'
loopback_description = 'Loopback Interface'
loopback_config = [
    f'interface {loopback_interface}',
    f'ip address {loopback_ip} {loopback_subnet_mask}',
    f'description {loopback_description}',
]

ssh_session.send_config_set(loopback_config)

# Introduce a delay for stability
time.sleep(2)

# Configure another interface (e.g., GigabitEthernet1/0)
interface_name = 'GigabitEthernet1/0'
interface_ip = '192.168.1.1'
interface_subnet_mask = '255.255.255.0'
interface_description = 'Connected to LAN'
interface_config = [
    f'interface {interface_name}',
    f'ip address {interface_ip} {interface_subnet_mask}',
    f'description {interface_description}',
]

ssh_session.send_config_set(interface_config)

# Introduce a delay for stability
time.sleep(2)

# Configure OSPF 
ospf_config = [
    'router ospf 1',
    f'network {loopback_ip} 0.0.0.0 area 0',
    f'network {interface_ip} 0.0.0.0 area 0',
]

ssh_session.send_config_set(ospf_config)

# Introduce a delay for stability
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
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Enable Password'))
print('{:<20} {:<15} {:<15}'.format(device_info['ip'], device_info['username'], '********'))
print('--- Running Configuration saved to:', output_file)
print(f'--- Loopback IP and Interface IP configured with OSPF: {loopback_ip}, {interface_ip}')
print('------------------------------------------------------')
