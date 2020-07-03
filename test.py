import nmap
import os

scanner = nmap.PortScanner()

ip_addr = '192.168.253.253'


# print(os.system('sudo nmap www.google.com'))


# print("Nmap Version: ", scanner.nmap_version())
# scanner.scan(ip_addr, '1-1024', '-v -sV -sC -A')  # -sS -O
# print(scanner.scaninfo())
# print("Ip Status: ", scanner[ip_addr].state())
# print(scanner[ip_addr].all_protocols())
# print("Open Ports: ", scanner[ip_addr]['tcp'].keys())


# scan localhost for ports in range 21-443
