from netmiko import ConnectHandler
import getpass

cihaz_puan = 100


def getpasswd():
    password = getpass.getpass()
    return password

def getusername():
    username = input("SSH Kullanici Adiniz : ")
    return username


def getip():
    ip_add = input("IP Adresi : ")
    return ip_add

username = getusername()

iosv_l2 = {
    'device_type': 'cisco_ios',
    'ip': getip(),
    'username': username,
    'password': getpasswd()
}

net_connect = ConnectHandler(**iosv_l2)

def aaarulescheck():

    tacacs = False
    radius = False
    localssh = False

    output = net_connect.send_command('show run tacacs')
    if(str.__contains__(output,"Invalid")):
        tacacs = False
    else:
        tacacs = True

    output = net_connect.send_command('sho running-config radius')

    if(str.__contains__(output,"radius-server host")):
        radius = True
    else:
        radius = False

    output = net_connect.send_command('sho run | i sshkey')
    if(str.__contains__(output,"username "+username)):
        localssh = True
    else:
        localssh = False

    if(tacacs==False):
        a = input("Cihaz üzerinde tacacs+ konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_tacacs_config()

    if(radius==False):
        a = input("Cihaz üzerinde radius konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_radius_config()
    if(localssh==False):
        a = input("Cihaz üzerinde yerel ssh anahtarı konfigurasyonu bulunmamaktadır. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_localssh_config()

def do_localssh_config():
    ssh_public_key = input("SSH public anahtarinizi giriniz : ")
    config_commands = ['username '+username+" sshkey "+ssh_public_key]
    net_connect.send_config_set(config_commands)

def do_radius_config():
    a = input("Kaç adet radius server kullanacaksiniz?")

    for i in range(0,int(a)):
        radius_serv_ip = input("RADIUS server "+str(i+1)+" ip adresi : ")
        radius_group_name=input("RADIUS server grup adi : ")
        radius_serv_pass = input("RADIUS server şifresi  : ")
        config_commands = ['radius-server host '+str(radius_serv_ip)+" key " + radius_serv_pass + " authentication accounting"]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa group server radius '+radius_group_name,'server '+radius_serv_ip]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa authentication login default group '+radius_group_name,'aaa authentication login console group '+radius_group_name]
        net_connect.send_config_set(config_commands)
def do_tacacs_config():

    a = input("Kaç adet tacacs+ server kullanacaksiniz?")

    for i in range(0,int(a)):
        tacacs_serv_ip = input("TACACS server "+str(i+1)+" ip adresi : ")
        tacacs_group_name=input("TACACS server grup adi : ")
        tacacs_serv_pass = input("TACACS server şifresi  : ")
        config_commands = ['feature tacacs+','tacacs-server host '+str(tacacs_serv_ip)+" key "+tacacs_serv_pass]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa group server tacacs+ '+tacacs_group_name,'server '+tacacs_serv_ip]
        net_connect.send_config_set(config_commands)
        config_commands = ['aaa authentication login default group '+tacacs_group_name,'aaa authentication login console group '+tacacs_group_name]
        net_connect.send_config_set(config_commands)


aaarulescheck()


#config_commands = ['int loop 0', 'ip address 1.1.1.1 255.255.255.0']
#output = net_connect.send_config_set(config_commands)
#print (output)
