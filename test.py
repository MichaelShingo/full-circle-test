from opcua import Client;
import time

server_endpoint = 'opc.tcp://31.21.225.234:4840'
username = 'Testcase'
password = 'FullCircle'


client = Client(server_endpoint)
client.set_user(username)
client.set_password(password)
# client.set_security_string("Basic256Sha256,Sign,cert.der,key.pem")
client.connect()
print('client connected')
node_id = 'ns=2;s=NACELLEM/Variables/fCPUUsage_var'
while True:
    FCPUUsage = client.get_node(node_id)
    cpu = FCPUUsage.get_value()
    print(cpu)
    
    time.sleep(1)