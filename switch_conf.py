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

# ************************************************************AAA RULES START*****************************************************************************

def aaarulescheck():

    tacacs = False
    radius = False
    localssh = False

    output = net_connect.send_command('show run tacacs')
    if str.__contains__(output, "Invalid"):
        tacacs = False
    else:
        tacacs = True

    output = net_connect.send_command('sho running-config radius')

    if str.__contains__(output, "radius-server host"):
        radius = True
    else:
        radius = False

    output = net_connect.send_command('sho run | i sshkey')
    if(str.__contains__(output,"username "+username)):
        localssh = True
    else:
        localssh = False

    if tacacs == False:
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

    try:
        ssh_public_key = input("SSH public anahtarinizi giriniz : ")
        config_commands = ['username '+str(username)+" sshkey "+str(ssh_public_key)]
        net_connect.send_config_set(config_commands)

    except:
        print("SSH anahtar yapılandırılması başarılı")


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
    print("RADIUS server yapılandırılması başarılı.")
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
    print("TACACS server yapılandırılması başarılı")

# ************************************************************AAA RULES END************************************************************************************


# ************************************************************TIMEOUT CONTROL START****************************************************************************

def do_console_timeout():
    a = input("Konsol zaman aşımını kaç dakikaya ayarlamak istersiniz? (5-10 dakika önerilir)")
    b = int(a)*60
    config_commands = ['line console', 'exec-timeout '+str(b)]
    net_connect.send_config_set(config_commands)

def do_ssh_timeout():
    a = input("Uzak oturumlar için zaman aşımını kaç dakikaya ayarlamak istersiniz? (5-10 dakika önerilir)")
    config_commands = ['line vty', 'exec-timeout '+str(a)]
    net_connect.send_config_set(config_commands)


def audit_for_lines():
    console = False
    sshses = False
    output = net_connect.send_command('sho run | section console')
    if(str.__contains__(output,"exec-timeout")):
        console = True

    output = net_connect.send_command('sho run | section vty')
    if(str.__contains__(output,"exec-timeout")):
        sshses = True

    if(console==False):
        a = input("Cihaz üzerinde konsol bağlantıları için zaman aşımı konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_console_timeout()

    if(sshses==False):
        a = input("Cihaz üzerinde uzak bağlantılar için zaman aşımı konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_ssh_timeout()


# ************************************************************TIMEOUT CONTROL END*****************************************************************************


# ************************************************************VTY ACCESS RESTRICTION START********************************************************************

def do_vty_acl():
    name = input("Oluşturulacak acl için isim giriniz : ")
    remark= input("Oluşturulacak acl için açıklama giriniz : ")
    permitted_hosts = input("Izin vereceginiz adresi [IP]/[MASK] şeklinde giriniz. (192.168.122.13/24) : ")
    config_commands = ['ip access-list '+str(name),'remark access-class '+str(remark),'permit ip '+str(permitted_hosts)+" any",'deny ip any any log']
    net_connect.send_config_set(config_commands)
    config_commands = ['line vty','access-class '+name+" in"]
    net_connect.send_config_set(config_commands)



def audit_for_vty_acl():

    acl_conf = False
    output = net_connect.send_command('sho run | section vty')
    if(str.__contains__(output,"access-class")):
        acl_conf = True

    if acl_conf == False:
        a = input("Uzak terminal oturumları için access list konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_vty_acl()


# ************************************************************VTY ACCESS RESTRICTION END***********************************************************************


# ************************************************************PASSWORD RULES START*****************************************************************************

def do_password_strength():
    config_commands = ['password strength-check']
    net_connect.send_config_set(config_commands)
    print("Güçlü şifre gereksinimleri etkinlestirildi.")

def audit_password_strenght():

    pass_strength = False
    output = net_connect.send_command('show password strength-check')
    if(str.__contains__(output,"enabled")):
        pass_strength=True

    if pass_strength==False:
        a = input("Güçlü şifre gereksinimleri konfigüre edilmemiş. Konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
        if a==str(1):
            do_password_strength()


# def do_password_encryption():
#
#     passw = input("16-64 karakter sayisinda bir master key girin : ")
#     config_commands = ['key config-key ascii',passw,passw]
#     net_connect.send_config_set(config_commands)
#     config_commands = ['feature password encryption aes']
#     net_connect.send_config_set(config_commands)
#
#
# def audit_password_encryption():
#
#     pass_encryption = False
#     output = net_connect.send_command('show encryption service stat')
#     if(str.__contains__(output,"not being used")):
#         a = input("Şifreler clear-text formatında tutuluyor. AES şifrelemeyi konfigüre etmek ister misiniz? EVET[1] HAYIR[2]")
#         if a==str(1):
#             do_password_encryption()


# ************************************************************PASSWORD RULES END*******************************************************************************




