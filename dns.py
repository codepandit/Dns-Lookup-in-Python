import struct
import socket
import argparse
import dnslib

class DnsQueryBuilder:

        def __init__(self):
                self.url = ""
                self.rtype = "AA"

        def build_query_packet(self, url, rtype):
                packet = struct.pack(">H", 1)  # Query Ids (Just 1 default)
                packet += struct.pack(">H", 256)  # Flags AA RA RD TC
                packet += struct.pack(">H", 1)  # Questions
                packet += struct.pack(">H", 0)  # Answers
                packet += struct.pack(">H", 0)  # Authorities
                packet += struct.pack(">H", 0)  # Additional
                
                split_url = url.split(".")
                try:
                        #print("in try block")
                        if isinstance(int(split_url[0]), int):
                                split_url.append('in-addr')
                                split_url.append('arpa')
                                i = 3
                                while i != -1:
                                        packet += struct.pack("B", len(split_url[i]))
                                        for byte in split_url[i]:
                                                packet += struct.pack("c", byte.encode('utf-8'))
                                        i -= 1
                        packet += struct.pack("B", len(split_url[4]))
                        for byte in split_url[4]:
                                packet += struct.pack("c", byte.encode('utf-8'))
                        packet += struct.pack("B", len(split_url[5]))
                        for byte in split_url[5]:
                                packet += struct.pack("c", byte.encode('utf-8'))

                        packet += struct.pack("B", 0)  # End of String
                        packet += struct.pack(">H", 12) # Hardcoded default to inverse query because if code enters this section it would be for inverse query
                        packet += struct.pack(">H", 1)  # Query Class

                except:
                        
                        
                        for part in split_url:
                                packet += struct.pack("B", len(part))
                                for byte in part:
                                        packet += struct.pack("c", byte.encode('utf-8'))
                                
                        packet += struct.pack("B", 0)  # End of String
                        if rtype == b"CNAME" or rtype == "CNAME":
                                packet += struct.pack(">H", 5)  # Query Type 2-NS, 15-MX, 5-CNAME, 12-PTR, 28-AAAA
                        elif rtype == b"MX" or rtype == "MX":
                                packet += struct.pack(">H", 15)
                        elif rtype == b"PTR" or rtype == "PTR":
                                packet += struct.pack(">H", 12)
                        elif rtype == b"AAAA" or rtype == "AAAA":
                                packet += struct.pack(">H", 28)
                        else:
                                packet += struct.pack(">H", 1)

                        packet += struct.pack(">H", 1)  # Query Class

                return packet
                

def guiBuilder(domain, qtype, dnsIP):
        #print("running")
        url = domain
        rtype = qtype
        if dnsIP == "":
                dns = "1.1.1.1"
        else:
                dns = dnsIP
         # Sending the packet
        builder = DnsQueryBuilder()
        packet = builder.build_query_packet(url, rtype)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 4444))
        sock.settimeout(2)
        sock.sendto(bytes(packet), (dns, 53))
        data, addr = sock.recvfrom(1024)
        result = dnslib.DNSRecord().parse(data).format()
        line = result.splitlines()
        sock.close()
        return line

def main():

        #Creating an ArgumentParser object
        parser = argparse.ArgumentParser(description='Custom nslookup by Nikhil Mehral')
        #Adding Arguments into ArgumentParser object
        parser.add_argument('url', help='Enter URl for DNS Query ')
        parser.add_argument('--dns_ip', default="1.1.1.1", help='IP Adress of DNS Server, eg: --dns_ip 8.8.8.8')
        parser.add_argument('--rtype', default="AA", choices=["AA", "MX", "CNAME", "PTR", "AAAA"], help='Request Query type, eg: --rtype AA, NS, CNAME, MX, AAAA')
        args = parser.parse_args()

        url = args.url
        dns = args.dns_ip.encode('utf-8')
        rtype = args.rtype.encode('utf-8')
        #print(dns)      
        
                
        # Sending the packet
        builder = DnsQueryBuilder()
        packet = builder.build_query_packet(url, rtype)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 8888))
        sock.settimeout(2)
        sock.sendto(bytes(packet), (dns, 53))
        data, addr = sock.recvfrom(1024)
        result = dnslib.DNSRecord().parse(data).format()

        line = result.splitlines()
        for i in range(len(line)):
                #print(line[i])
                words = line[i].split(' ')
                #print(words)
                for i in range(len(words)):
                        if words[i] == 'Question:':
                                print('Host name: ' + words[i+1].strip(".'"))
                        elif words[i] == 'rtype=A' or words[i] == 'rtype=AAAA':
                                ip = words[-1][7:].strip("'>")
                                if (len(ip) > 20):
                                        print("IPv6: " + ip)
                                else:
                                        print("IPv4: " + ip)
                        elif words[i] == 'rtype=MX':
                                print("MX: " + words[-1].strip(".'>"))
                        elif words[i] == 'rtype=CNAME':
                                print("CNAME: " + words[-1][7:].strip(".'>"))
                        elif words[i] == 'rtype=PTR':
                                print("Inverse: " + words[-1][7:].strip(".'>"))
                    

        sock.close()



if __name__ == "__main__":
    main()


