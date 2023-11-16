from netmiko import ConnectHandler
import time
import getpass
import difflib
                             #When running the code first time it times out then works when i run it again second time                                
# Define the device information 
                                                                   
device_info = {
    'device_type': 'cisco_ios',
    'ip': '192.168.56.101',
    'username': getpass.getpass('Enter Username: '),
    'password': getpass.getpass('Enter Password: '),
    'secret': getpass.getpass('Enter Enable Password: '),
    'timeout': 60,
}

# Create a Netmiko SSH session
ssh_session = ConnectHandler(**device_info)

# Enter enable mode
ssh_session.enable()

# Introduce a delay for stability
time.sleep(2)

# Send a command to change the hostname
new_hostname = 'R2'
config_commands = [f'hostname {new_hostname}']
ssh_session.send_config_set(config_commands)

# Introduce a delay for stability
time.sleep(2)

# Send a command to output the running configuration
running_output = ssh_session.send_command('show running-config')

# Save the running configuration to a file
running_output_file = 'running_config.txt'
with open(running_output_file, 'w') as config_file:
    config_file.write(running_output)

# Send a command to output the startup configuration
startup_output = ssh_session.send_command('show startup-config')

# Save the startup configuration to a file
startup_output_file = 'startup_config.txt'
with open(startup_output_file, 'w') as config_file:
    config_file.write(startup_output)

# Exit enable mode
ssh_session.exit_enable_mode()

# Disconnect from the device
ssh_session.disconnect()

# Display the information
print('------------------------------------------------------')
print('{:<20} {:<15} {:<15}'.format('Device IP', 'Username', 'Enable Password'))
print('{:<20} {:<15} {:<15}'.format(device_info['ip'], device_info['username'], '********'))
print('--- Running Configuration saved to:', running_output_file)
print('--- Hostname changed to:', new_hostname)
print('--- Startup Configuration saved to:', startup_output_file)
print('--- Comparison results saved to: {comparison_results_file}')
print('--- Comparison results saved to: {comparison_offline_results}')
print('------------------------------------------------------')

# Compare the running and startup configurations
with open(running_output_file, 'r') as running_file:
    running_config = running_file.readlines()

with open(startup_output_file, 'r') as startup_file:
    startup_config = startup_file.readlines()

differ = difflib.Differ()
diff = list(differ.compare(startup_config, running_config))

# Save the comparison results to a file
comparison_results_file = 'comparison_results_file.txt'
with open(comparison_results_file, 'w') as result_file:
    for line in diff:
        result_file.write(line + '\n')

differ = difflib.Differ()
diff2 = list(differ.compare('devices-12.txt', running_config))

comparison_offline_results = 'comparison_offline_results.txt'
with open(comparison_offline_results, 'w') as result_file2:
    for line in diff2:
        result_file2.write(line + '\n')


