from opcua import Client
from opcua import Server
import time

opc_tcp = "opc.tcp://10.19.3.35:49320"
client = Client(opc_tcp)
client.connect()
node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.柜子三色灯红色停止"
node = client.get_node(node_info)
print("before modify node value: ", node.get_value())
node.set_writable()
flag = True
node.set_value(flag)
time.sleep(1)
print("after modify node value: ", node.get_value())
