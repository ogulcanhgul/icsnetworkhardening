# import paramiko
import socket
from socket import AF_INET, SOCK_STREAM, SOCK_DGRAM
import psutil
import re
			
# ip_adresi = input("IP adresi: ")
# kullanici_adi = input("Kullanıcı adı: ")
# sifre = input("Şifre: ")
# port = input("Port numarası: ")
# girdiler = [ip_adresi, kullanici_adi, sifre, port]
# print("""# Cisco ASAv 8.4.2 SSH baglantisi icin kullanici bilgileri""")
# print("IP Adresi: {0}\nKullanıcı Adı: {1}\nParola: {2}\nPort: {3}\n".format(*girdiler))			

# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(ip_adresi, port, kullanici_adi, sifre, timeout = 10) 

AD = "-"
AF_INET6 = getattr(socket, 'AF_INET6', object())
proto_map = {
    (AF_INET, SOCK_STREAM): 'tcp',
    (AF_INET6, SOCK_STREAM): 'tcp6',
    (AF_INET, SOCK_DGRAM): 'udp',
    (AF_INET6, SOCK_DGRAM): 'udp6',
}

templ = "%-5s %-30s %-30s %-13s %-6s %s"

f = open("out.txt", "x")


print(templ % (
    "Protokol", "Yerel Adres", "Uzak Adres", "Durum", "PID",
    "Program Adı"), file=f)

f.close()
    
proc_names = {}

f = open("out.txt", "a")

for p in psutil.process_iter(['pid', 'name']):
    proc_names[p.info['pid']] = p.info['name']

for c in psutil.net_connections(kind='inet'):
    laddr = "%s:%s" % (c.laddr)
    raddr = ""


    if c.raddr:
        raddr = "%s:%s" % (c.raddr)
    name = proc_names.get(c.pid, '?') or ''
    print(templ % (
        proto_map[(c.family, c.type)],
        laddr,
        raddr or AD,
        c.status,
        c.pid or AD,
        name[:15],
    ), file = f)

f.close()

f = open("ip_adresleri.txt", "x")

with open('out.txt', 'r') as file:
    fi = file.readlines()

re_ip = re.compile("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")

for line in fi:
    ip = re.findall(re_ip,line)
    print("IP: ", ip, file = f) 

f.close()
