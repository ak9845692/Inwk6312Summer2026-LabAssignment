from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.1.101",
    "username": "admin",
    "password": "cisco",
    "secret": "cisco",
}

net_connect = ConnectHandler(**device)

print(net_connect.find_prompt())

net_connect.disconnect()
