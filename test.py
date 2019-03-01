from opcua import Client
from opcua import ua
import datetime

client = Client("ocp.tcp://10.19.3.35:49320")
client.connect()
node_info = "ns=2;s=xinsawaninihoudaoxianti.QCPU.测试M7400"
node = client.get_node(node_info)
start_time = datetime.datetime.now()
print(node.get_value())
#node.set_attribute(ua.AttributeIds.Value, ua.DataValue(variant=ua.Variant(True)))
# print(node.get_value())
# value = node.get_value()
# print(value)
end_time = datetime.datetime.now()
time = end_time - start_time
print(time)
client.disconnect()
