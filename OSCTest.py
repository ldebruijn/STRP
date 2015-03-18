from pythonosc import osc_message_builder, udp_client

client = udp_client.UDPClient('192.168.1.25', 8000)

def send_OSC_message(address):
	msg = osc_message_builder.OscMessageBuilder(address=address)
	msg.add_arg(100)
	msg = msg.build()
	client.send(msg)

send_OSC_message('/hoi')