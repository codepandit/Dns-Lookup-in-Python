import struct
import socket
import argparse
import dnslib

#@author Patrick Mathieu / @pathetiq
# This code is an update from: 
# DNS packet struct packet taken from: http://stackoverflow.com/questions/24814044/having-trouble-building-a-dns-packet-in-python 
# User: http://stackoverflow.com/users/3850901/monkeyba
#

class DnsPacketBuilder:
        def __init__(self):
                pass

        def build_packet(self, url):
                packet = struct.pack(">H", 12049)  # Query Ids (Just 1 for now)
                packet += struct.pack(">H", 256)  # Flags
                packet += struct.pack(">H", 1)  # Questions
                packet += struct.pack(">H", 0)  # Answers
                packet += struct.pack(">H", 0)  # Authorities
                packet += struct.pack(">H", 0)  # Additional
                
		#@TODO all message should be in the form of a IP address with padding and translation to 1 to 255
                split_url = url.split(".")
                for part in split_url:
                        #parts = part.encode('utf-8')
                        packet += struct.pack("B", len(part))
                        for byte in part:
                            packet += struct.pack("c", byte.encode('utf-8'))
                
                packet += struct.pack("B", 0)  # End of String
                packet += struct.pack(">H", 1)  # Query Type
                packet += struct.pack(">H", 1)  # Query Class
                return packet
                

   
# Sending the packet
builder = DnsPacketBuilder()
packet = builder.build_packet("apple.com.au")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8888))
sock.settimeout(2)
sock.sendto(bytes(packet), ("208.67.222.222", 53))
print("Packet Sent")
data, addr = sock.recvfrom(1024)
result = dnslib.DNSRecord().parse(data).format()

print(result)
sock.close()