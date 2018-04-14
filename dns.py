import struct
import socket
import argparse
import dnslib
import sys

class DnsPacketBuilder:

        def __init__(self):
                pass

        def build_packet(self, url):
                packet = struct.pack(">H", 12049)  # Query Ids (Just 1 for now)
                #packet = struct.pack(">H", 23000)  # Query Ids for MX
                #packet = struct.pack(">H", 1)  # Query Ids for CNAME
                #packet = struct.pack(">H", 2)  # Query Ids for IQuery
                packet += struct.pack(">H", 256)  # Flags AA RA RD TC
                #packet += struct.pack(">H", 2304)  # Flags for IQUERY
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
                packet += struct.pack(">H", 5)  # Query Type 2-NS, 15-MX, 5-CNAME, 12-PTR
                packet += struct.pack(">H", 1)  # Query Class
                print(packet)
                return packet
                

   
# Sending the packet
builder = DnsPacketBuilder()
packet = builder.build_packet("eait.uq.edu.au")
#packet = builder.build_packet("23.96.52.53")
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', 8888))
sock.settimeout(2)
sock.sendto(bytes(packet), ("192.168.1.1", 53))
print("Packet Sent")
data, addr = sock.recvfrom(1024)
result = dnslib.DNSRecord().parse(data).format()

print(result)
print(sys.argv[0])
sock.close()